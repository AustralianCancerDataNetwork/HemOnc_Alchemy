from datetime import datetime, date
from typing import Optional, List
from itertools import chain
import sqlalchemy as sa
import sqlalchemy.orm as so
from .hemonc_enums import DrugClassType, ComponentRole, TimingUnit, Intent, Phase, \
                          BranchType, Setting, Risk, Phenotype, PriorTherapy, TherapyType, \
                          DrugClassRelationshipType, StudyDesign, SponsorType, BranchConditionalType


from omop_alchemy.db import Base
from omop_alchemy.model.vocabulary import Concept, Concept_Relationship

from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy

### N-M Association Tables ###

"""
Table to provide n-m mapping between regimen and studies

Used to create the 'was studied in' relationship (list) for each regimen object,
as well as the 'studies' relationship (list) for each study object
"""

variant_study_map = sa.Table(
    "variant_study_map",
    Base.metadata,
    sa.Column("study_code", sa.ForeignKey('hemonc_study.study_code'), primary_key=True),
    sa.Column("variant_cui", sa.ForeignKey('hemonc_variant.variant_cui'), primary_key=True)
)

"""
Table to provide n-m mapping between regimen parts and their containing regimen.

This allows regimen parts to be reused in multiple containing regimens, e.g. AC gets defined once and then 
is used as a regimen part in AC-TH, AC-THL etc. 

"""

component_to_class_map = sa.Table(
    "component_to_class_map",
    Base.metadata,
    sa.Column("component_code", sa.ForeignKey('hemonc_component.component_code'), primary_key=True),
    sa.Column("component_class_code", sa.ForeignKey('hemonc_component_class.component_class_code'), primary_key=True)
)


regimen_to_modality_map = sa.Table(
    "regimen_to_modality_map",
    Base.metadata,
    sa.Column("regimen_cui", sa.ForeignKey('hemonc_regimen.regimen_cui'), primary_key=True),
    sa.Column("modality_code", sa.ForeignKey('hemonc_modality.modality_code'), primary_key=True)
)


### Primary Object Models ###

class Hemonc_Ref(Base):
    __tablename__ = 'hemonc_ref'

    reference: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)    
    condition_code: so.Mapped[str] = so.mapped_column(sa.ForeignKey('hemonc_condition.condition_code'), primary_key=True)
    pmid: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)  
    study: so.Mapped[str] = so.mapped_column(sa.ForeignKey('hemonc_study.study_code'))
    title: so.Mapped[str] = so.mapped_column(sa.String(600))  
    pmcid: so.Mapped[str] = so.mapped_column(sa.String(100))  
    doi: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)  
    url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), nullable=True)  
    journal: so.Mapped[str] = so.mapped_column(sa.String(50))  
    biblio: so.Mapped[str] = so.mapped_column(sa.String(700))  
    pub_date: so.Mapped[date] = so.mapped_column(sa.Date)
    order: so.Mapped[int] = so.mapped_column(sa.Integer)
    update: so.Mapped[int] = so.mapped_column(sa.Integer)
    ref_type: so.Mapped[str] = so.mapped_column(sa.String(50))  

class Hemonc_Study(Base):

    __tablename__ = 'hemonc_study'
    study_code: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)    
    trial_id: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)
    condition_code: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_condition.condition_code'), primary_key=True)
    registry: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    enrollment_from: so.Mapped[Optional[date]] = so.mapped_column(sa.Date, nullable=True)
    enrollment_to: so.Mapped[Optional[date]] = so.mapped_column(sa.Date, nullable=True)
    phase: so.Mapped[str] = so.mapped_column(sa.String(100))
    study_design: so.Mapped[int] = so.mapped_column(sa.Enum(StudyDesign))
    study_design_imputed: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    sact: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, nullable=True)
    protocol: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    fda_reg_study: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    fda_unreg_study: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    start: so.Mapped[Optional[date]]  = so.mapped_column(sa.Date, nullable=True)
    end: so.Mapped[Optional[date]]  = so.mapped_column(sa.Date, nullable=True)
    study_group: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    sponsor: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    sponsor_type: so.Mapped[Optional[int]] = so.mapped_column(sa.Enum(SponsorType), nullable=True)
    date_added: so.Mapped[date]  = so.mapped_column(sa.Date)
    date_modified: so.Mapped[Optional[date]]  = so.mapped_column(sa.Date, nullable=True)

    studies: so.Mapped[List['Hemonc_Variant']] = so.relationship(secondary=variant_study_map, back_populates='studied_in')

    def condition_filter(self, other):
        try:
            return other.lower() in self.condition.condition_concept_code.lower()
        except AttributeError:
            return False

    def __init__(self, 
                 *args, 
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.studies=[]


class Hemonc_Regimen(Base):
    __tablename__ = 'hemonc_regimen'
    regimen_cui : so.Mapped[int] = so.mapped_column(primary_key=True)
    regimen_concept_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('concept.concept_id'), nullable=True)
    regimen_name: so.Mapped[str] = so.mapped_column(sa.String(200))
    regimen_concept: so.Mapped['Concept'] = so.relationship(foreign_keys=[regimen_concept_id])

    modalities: so.Mapped[List['Hemonc_Modality']] = so.relationship(secondary=regimen_to_modality_map,  back_populates='regimens')
    variants: so.Mapped[List['Hemonc_Variant']] = so.relationship(back_populates='variant_of')
    studied_in: AssociationProxy[List["Hemonc_Study"]] = association_proxy("variants", "studied_in")

    component_roles: so.Mapped[List['Hemonc_Component_Role']] = so.relationship(back_populates='regimen')
    components: AssociationProxy[List["Hemonc_Component"]] = association_proxy("component_roles", "component")
    component_classes: AssociationProxy[List["Hemonc_Component_Class"]] = association_proxy("component_roles", "component_class")

    @property
    def concept_ids(self):
        return list(set([h.concept_id for h in self.component_roles]))
    
    @property
    def supportive_concept_ids(self):
        return list(set([h.concept_id for h in self.component_roles if h.relationship_id in ['Has steroid tx', 'Has supportive med']]))

    @property
    def satc_concept_ids(self):
        # note the difference between filtering on relationship_id directly vs. filtering on those that appear as 
        # supportive or steroid anywhere in this regimen - this is to stop for e.g. prednisone appearing due to 'has immunosuppressor' 
        # relationship where is is actually there as a steroid. 
        return list(set([h.concept_id for h in self.component_roles if h.concept_id not in self.supportive_concept_ids]))
        
    @property
    def condition_ids(self):
        return list(set(chain.from_iterable([[condition.condition_concept_id for condition in study.condition] for study in self.studied_in])))
    
    @property
    def studied_in(self):
        return list(set(chain.from_iterable([v.studied_in for v in self.variants])))

    @property
    def studied_conditions(self):
        return list(set(chain.from_iterable([s.condition for s in self.studied_in])))

    @hybrid_method
    def condition_filter(self, other):
        """
            for most use-cases, the better option is:
            
            with so.Session(engine) as session:
                regimens = session.query(
                    Hemonc_Regimen
                ).all()

                filtered_regimens = [r for r in regimens if r.condition_filter('C25')]

        """
        return any([other in condition.condition_string_filter for condition in self.studied_conditions])
    
    @condition_filter.expression
    def condition_filter(cls, other):
        """
            this works and is convenient for filtering, but is crazy slow, so should only be used very minimally, as it runs the joins on a per-regimen level

            usage:
                with so.Session(engine) as session:
                    filtered_regimens = session.query(
                        Hemonc_Regimen
                    ).filter(Hemonc_Regimen.condition_filter('C25%')).all()
        """
        subquery = (
            sa.select(sa.literal(1))
            .join(Hemonc_Study, Hemonc_Variant.studied_in)
            .join(Hemonc_Condition, Hemonc_Study.condition)
            .join(Condition_Map, Condition_Map.condition_concept_id==Hemonc_Condition.condition_concept_id)
            .where(Hemonc_Variant.regimen_cui == cls.regimen_cui)
            .where(Condition_Map.standard_concept_code.like(other))
            .limit(1)
        )
        return subquery.scalar_subquery() == 1


class Hemonc_Variant(Base):
    __tablename__ = 'hemonc_variant'
    variant_cui: so.Mapped[int] = so.mapped_column(primary_key=True)
    variant_name: so.Mapped[str] = so.mapped_column(sa.String(200))
    regimen_cui: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('hemonc_regimen.regimen_cui'), nullable=True)
    variant_of: so.Mapped['Hemonc_Regimen'] = so.relationship(foreign_keys=[regimen_cui])
    studied_in: so.Mapped[List['Hemonc_Study']] = so.relationship(secondary=variant_study_map, back_populates='studies')
    has_parts: so.Mapped[List['Hemonc_Regimen_Part']] = so.relationship(back_populates='part_of', lazy='selectin')
    
    component_sigs: AssociationProxy[List["Hemonc_Cycle_Sig"]] = association_proxy("has_parts", "component_sigs")

    @property
    def IV_agents(self):
        return list(set(chain.from_iterable([[cs.component_id for cs in part.component_sigs if cs.route == 'IV'] for part in self.has_parts])))

    @property
    def PO_agents(self):
        return list(set(chain.from_iterable([[cs.component_id for cs in part.component_sigs if cs.route == 'PO'] for part in self.has_parts])))

    def condition_filter(self, other):
        return any([s.condition_filter(other) for s in self.studied_in])
    
class Part_Phase(Base):
    __tablename__  = "part_phase"
    regimen_part_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_regimen_part.regimen_part_id'), primary_key=True)
    variant_cui: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_variant.variant_cui'), primary_key=True)
    phase: so.Mapped[int] = so.mapped_column(sa.Enum(Phase), primary_key=True)

class Hemonc_Regimen_Part(Base):
    """
    If a regimen contains only one regimen part, the regimen part covering the whole regimen is still defined. 
    """
    __tablename__ = 'hemonc_regimen_part'
    regimen_part_id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    variant_cui: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_variant.variant_cui'), primary_key=True)
    timing_unit: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    timing: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    portion: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)
    
    cycle_sig_id: so.Mapped[Optional[str]] = so.mapped_column(sa.ForeignKey('hemonc_cycle_sig.cycle_sig_id'), nullable=True)
    part_of: so.Mapped['Hemonc_Variant'] = so.relationship(foreign_keys=[variant_cui])
    cycle_sig: so.Mapped['Hemonc_Cycle_Sig'] = so.relationship(foreign_keys=[cycle_sig_id])    

    component_sigs: so.Mapped[List['Hemonc_Sig']] = so.relationship(back_populates='regimen_part')


# TODO: consider re-working a 1:n map with timing for cycles / weeks etc?
# timing: so.Mapped[List['Part_Timing']] = so.relationship(back_populates="timing_of", lazy="selectin")


class Hemonc_Sig(Base):
    __tablename__ = 'hemonc_sig'
    sig_id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    # regimen_part_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_regimen_part.regimen_part_id'), primary_key=True)
    # variant_cui: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_variant.variant_cui'), primary_key=True)
    regimen_part_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    variant_cui: so.Mapped[int] = so.mapped_column(primary_key=True)
    component_code: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('hemonc_component.component_code'), nullable=True)

    __table_args__ = (sa.ForeignKeyConstraint([regimen_part_id, variant_cui],
                                              [Hemonc_Regimen_Part.regimen_part_id, Hemonc_Regimen_Part.variant_cui])
                                           ,{})
    component_role: so.Mapped[int] = so.mapped_column(sa.Enum(ComponentRole))
    component_name: so.Mapped[str] = so.mapped_column(sa.String(50))
    step_number: so.Mapped[str] = so.mapped_column(sa.String(10))
    component_class: so.Mapped[str] = so.mapped_column(sa.String(20))
    tail: so.Mapped[Optional[str]] = so.mapped_column(sa.String(250))
    route: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    # put the additional dosing details here
    doseMinNum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    doseMaxNum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    doseUnit: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    doseCapNum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    doseCapUnit: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    durationMinNum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    durationMaxNum: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    durationUnit: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    frequency: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    inParens: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), nullable=True)
    sequence: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    seq_rel: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    seq_rel_what: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    
    regimen_part: so.Mapped['Hemonc_Regimen_Part'] = so.relationship(foreign_keys=[regimen_part_id, variant_cui])
    component: so.Mapped['Hemonc_Component'] = so.relationship(foreign_keys=[component_code])

    component_id: AssociationProxy[int] = association_proxy("component", "component_concept_id")



class Sig_Days(Base):
    __tablename__ = 'sig_days'
    sig_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_sig.sig_id'), primary_key=True)
    regimen_part_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_regimen_part.regimen_part_id'), primary_key=True)
    variant_cui: so.Mapped[int] = so.mapped_column(sa.ForeignKey('hemonc_variant.variant_cui'), primary_key=True)
    day: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)

class Hemonc_Cycle_Sig(Base):
    __tablename__ = 'hemonc_cycle_sig'
    cycle_sig_id: so.Mapped[str] = so.mapped_column(sa.String(250), primary_key=True)
    cycle_len_min: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True, primary_key=True)
    cycle_len_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True, primary_key=True)
    cycle_len_units: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True, primary_key=True)
    duration_min: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    duration_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    duration_units: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    frequency_min: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    frequency_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    frequency_units: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    repeats_min: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    repeats_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    repeats_units: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    residual: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), nullable=True)

class Hemonc_Component(Base):
    __tablename__ = 'hemonc_component'
    component_code: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True) 
    component_name: so.Mapped[str] = so.mapped_column(sa.String(100))    
    component_classes: so.Mapped[List['Hemonc_Component_Class']] = so.relationship(secondary=component_to_class_map, 
                                                                                   back_populates='components')
    component_concept_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('concept.concept_id'), nullable=True)


class Hemonc_Component_Class(Base):
    __tablename__ = 'hemonc_component_class'
    component_class_code: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)
    component_class_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    component_class_concept_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('concept.concept_id'), nullable=True)

    components: so.Mapped[List['Hemonc_Component']] = so.relationship(secondary=component_to_class_map, 
                                                                      back_populates='component_classes')

class Hemonc_Component_Role(Base):
    __tablename__ = 'hemonc_component_role' 
    # because a role can have either component or component class as the included member, we create an ID specific to this table to allow nullable fields
    role_id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    regimen_cui: so.Mapped[str] = so.mapped_column(sa.ForeignKey('hemonc_regimen.regimen_cui'))
    component_code: so.Mapped[Optional[str]] = so.mapped_column(sa.ForeignKey('hemonc_component.component_code'), nullable=True) 
    component_class_code: so.Mapped[Optional[str]] = so.mapped_column(sa.ForeignKey('hemonc_component_class.component_class_code'), nullable=True) 
    relationship_id: so.Mapped[str] = so.mapped_column(sa.String(50)) 

    regimen: so.Mapped['Hemonc_Regimen'] = so.relationship(foreign_keys=[regimen_cui])
    component: so.Mapped['Hemonc_Component'] = so.relationship(foreign_keys=[component_code])
    component_class: so.Mapped['Hemonc_Component_Class'] = so.relationship(foreign_keys=[component_class_code])

    component_name: AssociationProxy[str] = association_proxy("component", "component_name")
    component_class_name: AssociationProxy[str] = association_proxy("component_class", "component_class_name")

    @property
    def concept_id(self):
        if self.component:
            return self.component.component_concept_id
        elif self.component_class:
            return self.component_class.component_class_concept_id

    
class Hemonc_Modality(Base):
    __tablename__ = 'hemonc_modality'
    modality_code: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)
    modality_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    regimens: so.Mapped[List['Hemonc_Regimen']] = so.relationship(secondary=regimen_to_modality_map, 
                                                                  back_populates='modalities')
    modality_concept_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey('concept.concept_id'), nullable=True)
    modality_concept: so.Mapped['Concept'] = so.relationship(foreign_keys=[modality_concept_id])    


hemonc = so.aliased(Concept, name='hemonc')
standard = so.aliased(Concept, name='standard')

condition_map_filter = (
    sa.select(
        hemonc.concept_id.label('condition_concept_id'),
        hemonc.concept_code.label('condition_concept_code'),
        hemonc.concept_name.label('condition_concept_name'),
        Concept_Relationship.relationship_id,
        standard.concept_id.label('standard_concept_id'),
        standard.concept_code.label('standard_concept_code'),
        standard.concept_name.label('standard_concept_name'),
        standard.vocabulary_id.label('standard_vocabulary_id'),

    )
    .join(Concept_Relationship, hemonc.concept_id==Concept_Relationship.concept_id_1, isouter=True)
    .join(standard, standard.concept_id==Concept_Relationship.concept_id_2, isouter=True)
    .filter(
        sa.and_(
            hemonc.vocabulary_id=='HemOnc',
            hemonc.concept_class_id=='Condition',
            sa.or_(
                Concept_Relationship.relationship_id=='Maps to',
                Concept_Relationship.relationship_id==None
            )
        )
    )
    .subquery()
)

class Condition_Map(Base):
    __table__ = condition_map_filter
    condition_concept_id = condition_map_filter.c.condition_concept_id
    condition_concept_code = condition_map_filter.c.condition_concept_code
    condition_concept_name = condition_map_filter.c.condition_concept_name
    standard_concept_id = condition_map_filter.c.standard_concept_id
    standard_concept_code = condition_map_filter.c.standard_concept_code
    standard_concept_name = condition_map_filter.c.standard_concept_name

class Hemonc_Condition(Base):
    __tablename__ = 'hemonc_condition'
    condition_code: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)
    condition_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    condition_concept_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey('Condition_Map.condition_concept_id'), nullable=True)

    @property
    def standard_condition_codes(self):
        return 

# this has to be added once both dependencies created - the subquery relationship 
# pushes addition of Hemonc_Condition too late in the registry population otherwise

Hemonc_Study.condition = so.relationship(
    Hemonc_Condition,
    primaryjoin=Hemonc_Study.condition_code == so.foreign(Hemonc_Condition.condition_code)
)

Hemonc_Condition.condition_concept = so.relationship(
    Condition_Map,
    primaryjoin=Hemonc_Condition.condition_concept_id == so.foreign(Condition_Map.condition_concept_id)
)

def add_condition_string_filter_property():
    @property
    def condition_string_filter(self):
        return (
            ','.join([cm.standard_concept_code for cm in self.condition_concept])
        )
    
    Hemonc_Condition.condition_string_filter = condition_string_filter

add_condition_string_filter_property()

# end of section for post-hoc property creation
class Hemonc_Context(Base):
    __tablename__ = 'hemonc_context'
    context_code: so.Mapped[str] = so.mapped_column(sa.String(200), primary_key=True)
    context_name: so.Mapped[str] = so.mapped_column(sa.String(200))
    intent: so.Mapped[int] = so.mapped_column(sa.Enum(Intent))
    setting: so.Mapped[Optional[int]] = so.mapped_column(sa.Enum(Setting), nullable=True)
    phase: so.Mapped[Optional[int]] = so.mapped_column(sa.Enum(Phase), nullable=True)
    risk_stratification: so.Mapped[Optional[int]] = so.mapped_column(sa.Enum(Risk), nullable=True)
    phenotype: so.Mapped[Optional[int]] = so.mapped_column(sa.Enum(Phenotype), nullable=True)
    prior_therapy: so.Mapped[Optional[int]] = so.mapped_column(sa.Enum(PriorTherapy), nullable=True)
    date_added: so.Mapped[date]  = so.mapped_column(sa.Date)
    # do biomarker and condition belong directly in the context or is it a multi-way n-m relationship?

class Hemonc_Branch_Conditional(Base):
    __tablename__ = 'hemonc_branch_conditional'
    branch_name: so.Mapped[str] = so.mapped_column(sa.String(100), primary_key=True)
    branch_type: so.Mapped[int] = so.mapped_column(sa.Enum(BranchConditionalType))
    numeric_min: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    numeric_max: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    value: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100), nullable=True)



