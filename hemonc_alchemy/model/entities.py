from __future__ import annotations

from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, foreign, mapped_column
from sqlalchemy.orm import relationship as sa_relationship

from .base import Base, EntityBase


from .enums import (
    Authors_RoleEnum,
    Authors_Site_typeEnum,
    Canonicaltriples_Class_1Enum,
    Conditions_Age_focusEnum,
    Conditions_Condition_typeEnum,
    Conditions_Map_type_icd10cmEnum,
    Conditions_Map_type_icd9cmEnum,
    Conditions_Map_type_icdo3Enum,
    Conditions_Map_type_icdo3_morphEnum,
    Conditions_Map_type_ncitEnum,
    Conditions_Map_type_oncotreeEnum,
    Conditions_SectionEnum,
    Contexttable_IntentEnum,
    Contexttable_PhaseEnum,
    Contexttable_Risk_stratificationEnum,
    Contexttable_Therapy_typeEnum,
    Drugs_Class_typeEnum,
    Exclusions_Rev1Enum,
    HemoncClasses_Class_typeEnum,
    HemoncClasses_Omopdomain_idEnum,
    HemoncClasses_Omopstandard_conceptEnum,
    Inclusions_ReasonEnum,
    Inclusions_Ref_typeEnum,
    Indications_Age_unitEnum,
    Indications_Biomarker2Enum,
    Indications_Biomarker2_findingEnum,
    Indications_Biomarker2_typeEnum,
    Indications_Biomarker3_findingEnum,
    Indications_Biomarker3_typeEnum,
    Indications_Biomarker4Enum,
    Indications_Biomarker4_findingEnum,
    Indications_Biomarker4_typeEnum,
    Indications_Biomarker_findingEnum,
    Indications_Biomarker_typeEnum,
    Indications_NoteEnum,
    Indications_RegulatorEnum,
    Indications_SexEnum,
    Persons_GenderEnum,
    Persons_Hyphen_typeEnum,
    Persons_Vital_statusEnum,
    Refs_Ref_typeEnum,
    Sigs_Class_fieldEnum,
    Sigs_Component_roleEnum,
    Sigs_Cycle_length_unitEnum,
    Sigs_DosecapunitEnum,
    Sigs_DoseunitEnum,
    Sigs_DurationunitEnum,
    Sigs_FrequencyEnum,
    Sigs_PhaseEnum,
    Sigs_RouteEnum,
    Sigs_Step_numberEnum,
    Sigs_TargetleveltypeEnum,
    Sigs_TargetlevelunitEnum,
    Studies_RegistryEnum,
    Studies_Sponsor_typeEnum,
    Studies_Study_designEnum,
    StudyResults_Arm_typeEnum,
    StudyResults_Endpoint_classEnum,
    StudyResults_Endpoint_typeEnum,
    StudyResults_MetricunitEnum,
    StudyResults_StatisticEnum,
    Units_Unit_typeEnum,
    Variantblob_BlockEnum,
    Variantblob_Chunk_typeEnum,
)







class Authors(EntityBase, Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'authors.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = []
    derived_columns = []

    enum_lookup = {
        'role': Authors_RoleEnum,
        'site_type': Authors_Site_typeEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('pmid', 'sequence', 'aff_no', name='uq_authors_natural_key'),
    )

    aff_no: Mapped[int] = mapped_column(BigInteger, nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    flag: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    forename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    fullname_europmc: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    imputed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    initials: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    lastname: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    orcid: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    person_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pmid: Mapped[int] = mapped_column(BigInteger, nullable=False)
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Optional[Authors_RoleEnum]] = mapped_column(Enum(Authors_RoleEnum), nullable=True)
    sequence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    site: Mapped[str] = mapped_column(String(255), nullable=False)
    site_type: Mapped[Optional[Authors_Site_typeEnum]] = mapped_column(Enum(Authors_Site_typeEnum), nullable=True)
    suffix: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    tforename: Mapped[str] = mapped_column(String(255), nullable=False)
    tfullname: Mapped[str] = mapped_column(String(255), nullable=False)
    tlastname: Mapped[str] = mapped_column(String(255), nullable=False)

    normalisation_groups = [
    ]
    pmid_exclusions_obj: Mapped[Optional['Exclusions']] = sa_relationship(
        'Exclusions',
        primaryjoin="Authors.pmid == foreign(Exclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )

    pmid_inclusions_obj: Mapped[Optional['Inclusions']] = sa_relationship(
        'Inclusions',
        primaryjoin="Authors.pmid == foreign(Inclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )

    person_cui_obj: Mapped[Optional['Persons']] = sa_relationship(
        'Persons',
        primaryjoin="Authors.person_cui == foreign(Persons.person_cui)",
        lazy='selectin',
        viewonly=True,
    )


class Conditions(EntityBase, Base):
    __tablename__ = 'conditions'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'conditions.csv'
    pk_columns = ['id']
    source_defined_keys = ['condition', 'condition_cui']
    identity_keys = []
    denormalised_columns = ['map_icd10cm', 'map_icd9cm', 'map_icdo3', 'map_icdo3_morph', 'map_oncotree', 'map_type_icdo3_morph']
    derived_columns = []

    enum_lookup = {
        'condition_type': Conditions_Condition_typeEnum,
        'section': Conditions_SectionEnum,
        'age_focus': Conditions_Age_focusEnum,
        'map_type_ncit': Conditions_Map_type_ncitEnum,
        'map_type_oncotree': Conditions_Map_type_oncotreeEnum,
        'map_type_icd9cm': Conditions_Map_type_icd9cmEnum,
        'map_type_icd10cm': Conditions_Map_type_icd10cmEnum,
        'map_type_icdo3': Conditions_Map_type_icdo3Enum,
        'map_type_icdo3_morph': Conditions_Map_type_icdo3_morphEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('condition', 'condition_cui', name='uq_conditions_natural_key'),
    )

    age_focus: Mapped[Conditions_Age_focusEnum] = mapped_column(Enum(Conditions_Age_focusEnum), nullable=False)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    condition_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    condition_type: Mapped[Conditions_Condition_typeEnum] = mapped_column(Enum(Conditions_Condition_typeEnum), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    map_ncit: Mapped[str] = mapped_column(String(255), nullable=False)
    map_type_icd10cm: Mapped[str] = mapped_column(String(255), nullable=False)
    map_type_icd9cm: Mapped[str] = mapped_column(String(255), nullable=False)
    map_type_icdo3: Mapped[str] = mapped_column(String(255), nullable=False)
    map_type_ncit: Mapped[Conditions_Map_type_ncitEnum] = mapped_column(Enum(Conditions_Map_type_ncitEnum), nullable=False)
    map_type_oncotree: Mapped[Optional[Conditions_Map_type_oncotreeEnum]] = mapped_column(Enum(Conditions_Map_type_oncotreeEnum), nullable=True)
    regimenscount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    section: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    variantscount: Mapped[int] = mapped_column(BigInteger, nullable=False)

    normalisation_groups = [
        ['map_icd10cm', 'map_icd10cm'],
        ['map_icd9cm', 'map_icd9cm'],
        ['map_icdo3', 'map_icdo3'],
        ['map_icdo3_morph', 'map_icdo3_morph'],
        ['map_oncotree', 'map_oncotree'],
    ]
    map_icd10cm_items: Mapped[list['conditions_Map_icd10cmMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    map_icd9cm_items: Mapped[list['conditions_Map_icd9cmMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    map_icdo3_items: Mapped[list['conditions_Map_icdo3Map']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    map_icdo3_morph_items: Mapped[list['conditions_Map_icdo3_morphMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    map_oncotree_items: Mapped[list['conditions_Map_oncotreeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    map_type_icdo3_morph_items: Mapped[list['conditions_Map_type_icdo3_morphMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class conditions_Map_icd10cmMap(EntityBase, Base):
    __tablename__ = 'conditions_map_icd10cm'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('conditions.id'), primary_key=True)
    map_icd10cm: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Conditions'] = sa_relationship(back_populates='map_icd10cm_items')

class conditions_Map_icd9cmMap(EntityBase, Base):
    __tablename__ = 'conditions_map_icd9cm'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('conditions.id'), primary_key=True)
    map_icd9cm: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Conditions'] = sa_relationship(back_populates='map_icd9cm_items')

class conditions_Map_icdo3Map(EntityBase, Base):
    __tablename__ = 'conditions_map_icdo3'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('conditions.id'), primary_key=True)
    map_icdo3: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Conditions'] = sa_relationship(back_populates='map_icdo3_items')

class conditions_Map_icdo3_morphMap(EntityBase, Base):
    __tablename__ = 'conditions_map_icdo3_morph'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('conditions.id'), primary_key=True)
    map_icdo3_morph: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Conditions'] = sa_relationship(back_populates='map_icdo3_morph_items')

class conditions_Map_oncotreeMap(EntityBase, Base):
    __tablename__ = 'conditions_map_oncotree'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('conditions.id'), primary_key=True)
    map_oncotree: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Conditions'] = sa_relationship(back_populates='map_oncotree_items')

class conditions_Map_type_icdo3_morphMap(EntityBase, Base):
    __tablename__ = 'conditions_map_type_icdo3_morph'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('conditions.id'), primary_key=True)
    map_type_icdo3_morph: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Conditions'] = sa_relationship(back_populates='map_type_icdo3_morph_items')

class Drugs(EntityBase, Base):
    __tablename__ = 'drugs'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'drugs.csv'
    pk_columns = ['id']
    source_defined_keys = ['drug', 'drug_cui']
    identity_keys = []
    denormalised_columns = ['atc', 'canmed_major_class', 'canmed_major_class_cui', 'canmed_minor_class', 'canmed_minor_class_cui']
    derived_columns = []

    enum_lookup = {
        'class_type': Drugs_Class_typeEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('drug', 'drug_cui', name='uq_drugs_natural_key'),
    )

    class_type: Mapped[Optional[Drugs_Class_typeEnum]] = mapped_column(Enum(Drugs_Class_typeEnum), nullable=True)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    drug: Mapped[str] = mapped_column(String(255), nullable=False)
    drug_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    drug_inn: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    investigational: Mapped[bool] = mapped_column(Boolean, nullable=False)
    main_class: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    multiagent: Mapped[bool] = mapped_column(Boolean, nullable=False)

    normalisation_groups = [
        ['atc', 'atc'],
        ['canmed_major_class', 'canmed_major_class'],
        ['canmed_major_class', 'canmed_major_class_cui'],
        ['canmed_major_class_cui', 'canmed_major_class_cui'],
        ['canmed_minor_class', 'canmed_minor_class'],
        ['canmed_minor_class', 'canmed_minor_class_cui'],
        ['canmed_minor_class_cui', 'canmed_minor_class_cui'],
    ]
    atc_items: Mapped[list['drugs_AtcMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    canmed_major_class_items: Mapped[list['drugs_Canmed_major_classMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    canmed_major_class_cui_items: Mapped[list['drugs_Canmed_major_class_cuiMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    canmed_minor_class_items: Mapped[list['drugs_Canmed_minor_classMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    canmed_minor_class_cui_items: Mapped[list['drugs_Canmed_minor_class_cuiMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class drugs_AtcMap(EntityBase, Base):
    __tablename__ = 'drugs_atc'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('drugs.id'), primary_key=True)
    atc: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Drugs'] = sa_relationship(back_populates='atc_items')

class drugs_Canmed_major_classMap(EntityBase, Base):
    __tablename__ = 'drugs_canmed_major_class'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('drugs.id'), primary_key=True)
    canmed_major_class: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Drugs'] = sa_relationship(back_populates='canmed_major_class_items')

class drugs_Canmed_major_class_cuiMap(EntityBase, Base):
    __tablename__ = 'drugs_canmed_major_class_cui'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('drugs.id'), primary_key=True)
    canmed_major_class_cui: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Drugs'] = sa_relationship(back_populates='canmed_major_class_cui_items')

class drugs_Canmed_minor_classMap(EntityBase, Base):
    __tablename__ = 'drugs_canmed_minor_class'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('drugs.id'), primary_key=True)
    canmed_minor_class: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Drugs'] = sa_relationship(back_populates='canmed_minor_class_items')

class drugs_Canmed_minor_class_cuiMap(EntityBase, Base):
    __tablename__ = 'drugs_canmed_minor_class_cui'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('drugs.id'), primary_key=True)
    canmed_minor_class_cui: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Drugs'] = sa_relationship(back_populates='canmed_minor_class_cui_items')

class Indications(EntityBase, Base):
    __tablename__ = 'indications'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'indications.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['biomarker', 'biomarker2', 'biomarker2_finding', 'biomarker2_type', 'biomarker3', 'biomarker3_finding', 'biomarker3_type', 'biomarker4', 'biomarker4_finding', 'biomarker4_type', 'biomarker_finding', 'biomarker_type', 'context', 'demographics', 'ineligibility', 'prior_therapy', 'prior_therapy_negation', 'prior_therapy_setting', 'regimen', 'regimen_cui', 'response_contingency', 'risk_stratification', 'stage_or_status', 'with_field']
    derived_columns = []

    enum_lookup = {
        'regulator': Indications_RegulatorEnum,
        'note': Indications_NoteEnum,
        'sex': Indications_SexEnum,
        'age_unit': Indications_Age_unitEnum,
        'biomarker_finding': Indications_Biomarker_findingEnum,
        'biomarker_type': Indications_Biomarker_typeEnum,
        'biomarker2_finding': Indications_Biomarker2_findingEnum,
        'biomarker2_type': Indications_Biomarker2_typeEnum,
        'biomarker3_finding': Indications_Biomarker3_findingEnum,
        'biomarker3_type': Indications_Biomarker3_typeEnum,
        'biomarker4_finding': Indications_Biomarker4_findingEnum,
        'biomarker4_type': Indications_Biomarker4_typeEnum,
        'biomarker2': Indications_Biomarker2Enum,
        'biomarker4': Indications_Biomarker4Enum,
    }

    __table_args__ = (
        sa.UniqueConstraint('component_cui', 'condition', 'regulator', 'study', 'string', name='uq_indications_natural_key'),
    )

    accelerated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    age: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    age_unit: Mapped[Optional[Indications_Age_unitEnum]] = mapped_column(Enum(Indications_Age_unitEnum), nullable=True)
    component: Mapped[str] = mapped_column(String(255), nullable=False)
    component_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    first_in_class: Mapped[bool] = mapped_column(Boolean, nullable=False)
    note: Mapped[Optional[Indications_NoteEnum]] = mapped_column(Enum(Indications_NoteEnum), nullable=True)
    prior_biomarker: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    regulator: Mapped[Indications_RegulatorEnum] = mapped_column(Enum(Indications_RegulatorEnum), nullable=False)
    sex: Mapped[Optional[Indications_SexEnum]] = mapped_column(Enum(Indications_SexEnum), nullable=True)
    string: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    study: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    study_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    study_yn: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    time_contingency: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    withdrawn: Mapped[str] = mapped_column(String(255), nullable=False)

    normalisation_groups = [
        ['biomarker', 'biomarker'],
        ['biomarker2', 'biomarker2_finding'],
        ['biomarker3', 'biomarker3'],
        ['biomarker4', 'biomarker4_finding'],
        ['biomarker_finding', 'biomarker_finding'],
        ['regimen', 'regimen'],
        ['regimen_cui', 'regimen_cui'],
        ['with_field', 'with_field'],
    ]
    biomarker_items: Mapped[list['indications_BiomarkerMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker2_items: Mapped[list['indications_Biomarker2Map']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker2_finding_items: Mapped[list['indications_Biomarker2_findingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker2_type_items: Mapped[list['indications_Biomarker2_typeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker3_items: Mapped[list['indications_Biomarker3Map']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker3_finding_items: Mapped[list['indications_Biomarker3_findingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker3_type_items: Mapped[list['indications_Biomarker3_typeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker4_items: Mapped[list['indications_Biomarker4Map']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker4_finding_items: Mapped[list['indications_Biomarker4_findingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker4_type_items: Mapped[list['indications_Biomarker4_typeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker_finding_items: Mapped[list['indications_Biomarker_findingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    biomarker_type_items: Mapped[list['indications_Biomarker_typeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    context_items: Mapped[list['indications_ContextMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    demographics_items: Mapped[list['indications_DemographicsMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    ineligibility_items: Mapped[list['indications_IneligibilityMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    prior_therapy_items: Mapped[list['indications_Prior_therapyMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    prior_therapy_negation_items: Mapped[list['indications_Prior_therapy_negationMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    prior_therapy_setting_items: Mapped[list['indications_Prior_therapy_settingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    regimen_items: Mapped[list['indications_RegimenMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    regimen_cui_items: Mapped[list['indications_Regimen_cuiMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    response_contingency_items: Mapped[list['indications_Response_contingencyMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    risk_stratification_items: Mapped[list['indications_Risk_stratificationMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    stage_or_status_items: Mapped[list['indications_Stage_or_statusMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    with_field_items: Mapped[list['indications_With_fieldMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    condition_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="Indications.condition == foreign(Conditions.condition)",
        lazy='selectin',
        viewonly=True,
    )


class indications_BiomarkerMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker_items')

class indications_Biomarker2Map(EntityBase, Base):
    __tablename__ = 'indications_biomarker2'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker2: Mapped[Optional[Indications_Biomarker2Enum]] = mapped_column(Enum(Indications_Biomarker2Enum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker2_items')

class indications_Biomarker2_findingMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker2_finding'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker2_finding: Mapped[Optional[Indications_Biomarker2_findingEnum]] = mapped_column(Enum(Indications_Biomarker2_findingEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker2_finding_items')

class indications_Biomarker2_typeMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker2_type'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker2_type: Mapped[Optional[Indications_Biomarker2_typeEnum]] = mapped_column(Enum(Indications_Biomarker2_typeEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker2_type_items')

class indications_Biomarker3Map(EntityBase, Base):
    __tablename__ = 'indications_biomarker3'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker3: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker3_items')

class indications_Biomarker3_findingMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker3_finding'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker3_finding: Mapped[Optional[Indications_Biomarker3_findingEnum]] = mapped_column(Enum(Indications_Biomarker3_findingEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker3_finding_items')

class indications_Biomarker3_typeMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker3_type'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker3_type: Mapped[Optional[Indications_Biomarker3_typeEnum]] = mapped_column(Enum(Indications_Biomarker3_typeEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker3_type_items')

class indications_Biomarker4Map(EntityBase, Base):
    __tablename__ = 'indications_biomarker4'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker4: Mapped[Optional[Indications_Biomarker4Enum]] = mapped_column(Enum(Indications_Biomarker4Enum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker4_items')

class indications_Biomarker4_findingMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker4_finding'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker4_finding: Mapped[Optional[Indications_Biomarker4_findingEnum]] = mapped_column(Enum(Indications_Biomarker4_findingEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker4_finding_items')

class indications_Biomarker4_typeMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker4_type'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker4_type: Mapped[Optional[Indications_Biomarker4_typeEnum]] = mapped_column(Enum(Indications_Biomarker4_typeEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker4_type_items')

class indications_Biomarker_findingMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker_finding'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker_finding: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker_finding_items')

class indications_Biomarker_typeMap(EntityBase, Base):
    __tablename__ = 'indications_biomarker_type'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    biomarker_type: Mapped[Optional[Indications_Biomarker_typeEnum]] = mapped_column(Enum(Indications_Biomarker_typeEnum), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='biomarker_type_items')

class indications_ContextMap(EntityBase, Base):
    __tablename__ = 'indications_context'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    context: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='context_items')

class indications_DemographicsMap(EntityBase, Base):
    __tablename__ = 'indications_demographics'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    demographics: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='demographics_items')

class indications_IneligibilityMap(EntityBase, Base):
    __tablename__ = 'indications_ineligibility'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    ineligibility: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='ineligibility_items')

class indications_Prior_therapyMap(EntityBase, Base):
    __tablename__ = 'indications_prior_therapy'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    prior_therapy: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='prior_therapy_items')

class indications_Prior_therapy_negationMap(EntityBase, Base):
    __tablename__ = 'indications_prior_therapy_negation'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    prior_therapy_negation: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='prior_therapy_negation_items')

class indications_Prior_therapy_settingMap(EntityBase, Base):
    __tablename__ = 'indications_prior_therapy_setting'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    prior_therapy_setting: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='prior_therapy_setting_items')

class indications_RegimenMap(EntityBase, Base):
    __tablename__ = 'indications_regimen'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    regimen: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='regimen_items')

class indications_Regimen_cuiMap(EntityBase, Base):
    __tablename__ = 'indications_regimen_cui'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    regimen_cui: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='regimen_cui_items')

class indications_Response_contingencyMap(EntityBase, Base):
    __tablename__ = 'indications_response_contingency'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    response_contingency: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='response_contingency_items')

class indications_Risk_stratificationMap(EntityBase, Base):
    __tablename__ = 'indications_risk_stratification'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    risk_stratification: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='risk_stratification_items')

class indications_Stage_or_statusMap(EntityBase, Base):
    __tablename__ = 'indications_stage_or_status'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    stage_or_status: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='stage_or_status_items')

class indications_With_fieldMap(EntityBase, Base):
    __tablename__ = 'indications_with_field'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('indications.id'), primary_key=True)
    with_field: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Indications'] = sa_relationship(back_populates='with_field_items')

class Persons(EntityBase, Base):
    __tablename__ = 'persons'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'persons.csv'
    pk_columns = ['id']
    source_defined_keys = ['name', 'person_cui']
    identity_keys = []
    denormalised_columns = ['condition_types', 'conditions', 'country', 'location', 'orcid', 'site', 'study_groups', 'study_sponsors']
    derived_columns = ['total_pubs']

    enum_lookup = {
        'hyphen_type': Persons_Hyphen_typeEnum,
        'gender': Persons_GenderEnum,
        'vital_status': Persons_Vital_statusEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('name', 'person_cui', name='uq_persons_natural_key'),
    )

    co_authors: Mapped[int] = mapped_column(BigInteger, nullable=False)
    co_authorships: Mapped[int] = mapped_column(BigInteger, nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    first_active_year: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[Persons_GenderEnum] = mapped_column(Enum(Persons_GenderEnum), nullable=False)
    guideline_pubs: Mapped[str] = mapped_column(String(255), nullable=False)
    hyphen_type: Mapped[Optional[Persons_Hyphen_typeEnum]] = mapped_column(Enum(Persons_Hyphen_typeEnum), nullable=True)
    last_active_year: Mapped[str] = mapped_column(String(255), nullable=False)
    multi_site: Mapped[bool] = mapped_column(Boolean, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    person_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ph3_studies: Mapped[str] = mapped_column(String(255), nullable=False)
    pivotal_studies: Mapped[str] = mapped_column(String(255), nullable=False)
    senior_pubs: Mapped[int] = mapped_column(BigInteger, nullable=False)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    vital_status: Mapped[int] = mapped_column(BigInteger, nullable=False)

    normalisation_groups = [
        ['condition_types', 'condition_types'],
        ['conditions', 'conditions'],
        ['country', 'country'],
        ['location', 'location'],
        ['orcid', 'orcid'],
        ['site', 'site'],
        ['study_groups', 'study_groups'],
        ['study_sponsors', 'study_sponsors'],
    ]
    condition_types_items: Mapped[list['persons_Condition_typesMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    conditions_items: Mapped[list['persons_ConditionsMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    country_items: Mapped[list['persons_CountryMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    location_items: Mapped[list['persons_LocationMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    orcid_items: Mapped[list['persons_OrcidMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    site_items: Mapped[list['persons_SiteMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    study_groups_items: Mapped[list['persons_Study_groupsMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    study_sponsors_items: Mapped[list['persons_Study_sponsorsMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class persons_Condition_typesMap(EntityBase, Base):
    __tablename__ = 'persons_condition_types'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    condition_types: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='condition_types_items')

class persons_ConditionsMap(EntityBase, Base):
    __tablename__ = 'persons_conditions'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    conditions: Mapped[str] = mapped_column(Text, primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='conditions_items')

class persons_CountryMap(EntityBase, Base):
    __tablename__ = 'persons_country'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    country: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='country_items')

class persons_LocationMap(EntityBase, Base):
    __tablename__ = 'persons_location'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    location: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='location_items')

class persons_OrcidMap(EntityBase, Base):
    __tablename__ = 'persons_orcid'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    orcid: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='orcid_items')

class persons_SiteMap(EntityBase, Base):
    __tablename__ = 'persons_site'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    site: Mapped[str] = mapped_column(Text, primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='site_items')

class persons_Study_groupsMap(EntityBase, Base):
    __tablename__ = 'persons_study_groups'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    study_groups: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='study_groups_items')

class persons_Study_sponsorsMap(EntityBase, Base):
    __tablename__ = 'persons_study_sponsors'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('persons.id'), primary_key=True)
    study_sponsors: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Persons'] = sa_relationship(back_populates='study_sponsors_items')

class Pointers(EntityBase, Base):
    __tablename__ = 'pointers'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'pointers.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['biomarker', 'context', 'notes']
    derived_columns = []

    enum_lookup = {}

    __table_args__ = (
        sa.UniqueConstraint('h2_html', 'h3_html', 'version', name='uq_pointers_natural_key'),
    )

    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    h2_html: Mapped[str] = mapped_column(String(255), nullable=False)
    h3_html: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tracer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    version: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    normalisation_groups = [
    ]
    biomarker_items: Mapped[list['pointers_BiomarkerMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    context_items: Mapped[list['pointers_ContextMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    notes_items: Mapped[list['pointers_NotesMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    condition_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="Pointers.condition == foreign(Conditions.condition)",
        lazy='selectin',
        viewonly=True,
    )


class pointers_BiomarkerMap(EntityBase, Base):
    __tablename__ = 'pointers_biomarker'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('pointers.id'), primary_key=True)
    biomarker: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Pointers'] = sa_relationship(back_populates='biomarker_items')

class pointers_ContextMap(EntityBase, Base):
    __tablename__ = 'pointers_context'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('pointers.id'), primary_key=True)
    context: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Pointers'] = sa_relationship(back_populates='context_items')

class pointers_NotesMap(EntityBase, Base):
    __tablename__ = 'pointers_notes'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('pointers.id'), primary_key=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Pointers'] = sa_relationship(back_populates='notes_items')





class Refs(EntityBase, Base):
    __tablename__ = 'refs'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'refs.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['biblio', 'doi', 'reference', 'temp', 'title']
    derived_columns = []

    enum_lookup = {
        'ref_type': Refs_Ref_typeEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('study', 'condition', 'biomarker', 'pmid', name='uq_refs_natural_key'),
    )

    biomarker: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    journal: Mapped[str] = mapped_column(String(255), nullable=False)
    pmcid: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pmid: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pubdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ref_type: Mapped[Refs_Ref_typeEnum] = mapped_column(Enum(Refs_Ref_typeEnum), nullable=False)
    study: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    normalisation_groups = [
    ]
    biblio_items: Mapped[list['refs_BiblioMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    doi_items: Mapped[list['refs_DoiMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    reference_items: Mapped[list['refs_ReferenceMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    temp_items: Mapped[list['refs_TempMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    title_items: Mapped[list['refs_TitleMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    pmid_exclusions_obj: Mapped[Optional['Exclusions']] = sa_relationship(
        'Exclusions',
        primaryjoin="Refs.pmid == foreign(Exclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )

    pmid_inclusions_obj: Mapped[Optional['Inclusions']] = sa_relationship(
        'Inclusions',
        primaryjoin="Refs.pmid == foreign(Inclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )

    condition_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="Refs.condition == foreign(Conditions.condition)",
        lazy='selectin',
        viewonly=True,
    )


class refs_BiblioMap(EntityBase, Base):
    __tablename__ = 'refs_biblio'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('refs.id'), primary_key=True)
    biblio: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Refs'] = sa_relationship(back_populates='biblio_items')

class refs_DoiMap(EntityBase, Base):
    __tablename__ = 'refs_doi'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('refs.id'), primary_key=True)
    doi: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Refs'] = sa_relationship(back_populates='doi_items')

class refs_ReferenceMap(EntityBase, Base):
    __tablename__ = 'refs_reference'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('refs.id'), primary_key=True)
    reference: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Refs'] = sa_relationship(back_populates='reference_items')

class refs_TempMap(EntityBase, Base):
    __tablename__ = 'refs_temp'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('refs.id'), primary_key=True)
    temp: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Refs'] = sa_relationship(back_populates='temp_items')

class refs_TitleMap(EntityBase, Base):
    __tablename__ = 'refs_title'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('refs.id'), primary_key=True)
    title: Mapped[str] = mapped_column(Text, primary_key=True)

    parent: Mapped['Refs'] = sa_relationship(back_populates='title_items')

class Sigs(EntityBase, Base):
    __tablename__ = 'sigs'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'sigs.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['cyclesigs_note', 'seqrel', 'seqrelwhen', 'seqrelwhenunit', 'timing']
    derived_columns = []

    enum_lookup = {
        'phase': Sigs_PhaseEnum,
        'component_role': Sigs_Component_roleEnum,
        'cycle_length_unit': Sigs_Cycle_length_unitEnum,
        'step_number': Sigs_Step_numberEnum,
        'class_field': Sigs_Class_fieldEnum,
        'doseunit': Sigs_DoseunitEnum,
        'dosecapunit': Sigs_DosecapunitEnum,
        'targetlevelunit': Sigs_TargetlevelunitEnum,
        'targetleveltype': Sigs_TargetleveltypeEnum,
        'route': Sigs_RouteEnum,
        'durationunit': Sigs_DurationunitEnum,
        'frequency': Sigs_FrequencyEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('regimen_cui', 'variant_cui', 'phase', 'portion', 'component_cui', 'doseminnum', 'route_cui', 'timing_sequence', 'step_number', 'study', 'cyclesigs', 'alldays', 'inparens', 'tail', name='uq_sigs_natural_key'),
    )

    alldays: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    class_field: Mapped[Sigs_Class_fieldEnum] = mapped_column(Enum(Sigs_Class_fieldEnum), nullable=False)
    component: Mapped[str] = mapped_column(String(255), nullable=False)
    component_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    component_role: Mapped[Sigs_Component_roleEnum] = mapped_column(Enum(Sigs_Component_roleEnum), nullable=False)
    cycle_length_lb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cycle_length_ub: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    cycle_length_unit: Mapped[Optional[Sigs_Cycle_length_unitEnum]] = mapped_column(Enum(Sigs_Cycle_length_unitEnum), nullable=True)
    cyclesigs: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    divided: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    dosecapnum: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dosecapunit: Mapped[Optional[Sigs_DosecapunitEnum]] = mapped_column(Enum(Sigs_DosecapunitEnum), nullable=True)
    dosecapunit_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dosemaxnum: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    doseminnum: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    doseunit: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    doseunit_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    durationmaxnum: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    durationminnum: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    durationunit: Mapped[Optional[Sigs_DurationunitEnum]] = mapped_column(Enum(Sigs_DurationunitEnum), nullable=True)
    durationunit_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    frequency: Mapped[Optional[Sigs_FrequencyEnum]] = mapped_column(Enum(Sigs_FrequencyEnum), nullable=True)
    frequency_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    inparens: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phase: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    portion: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    route: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    route_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    seqrelwhat: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sequence: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    step_number: Mapped[str] = mapped_column(String(255), nullable=False)
    study: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    targetlevel: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    targetleveltype: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    targetlevelunit: Mapped[Optional[Sigs_TargetlevelunitEnum]] = mapped_column(Enum(Sigs_TargetlevelunitEnum), nullable=True)
    targetlevelunit_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    timing_sequence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    variant: Mapped[str] = mapped_column(String(255), nullable=False)
    variant_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    normalisation_groups = [
        ['seqrel', 'seqrel'],
        ['seqrelwhenunit', 'seqrelwhenunit'],
    ]
    cyclesigs_note_items: Mapped[list['sigs_Cyclesigs_noteMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    seqrel_items: Mapped[list['sigs_SeqrelMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    seqrelwhen_items: Mapped[list['sigs_SeqrelwhenMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    seqrelwhenunit_items: Mapped[list['sigs_SeqrelwhenunitMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    timing_items: Mapped[list['sigs_TimingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class sigs_Cyclesigs_noteMap(EntityBase, Base):
    __tablename__ = 'sigs_cyclesigs_note'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('sigs.id'), primary_key=True)
    cyclesigs_note: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Sigs'] = sa_relationship(back_populates='cyclesigs_note_items')

class sigs_SeqrelMap(EntityBase, Base):
    __tablename__ = 'sigs_seqrel'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('sigs.id'), primary_key=True)
    seqrel: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Sigs'] = sa_relationship(back_populates='seqrel_items')

class sigs_SeqrelwhenMap(EntityBase, Base):
    __tablename__ = 'sigs_seqrelwhen'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('sigs.id'), primary_key=True)
    seqrelwhen: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Sigs'] = sa_relationship(back_populates='seqrelwhen_items')

class sigs_SeqrelwhenunitMap(EntityBase, Base):
    __tablename__ = 'sigs_seqrelwhenunit'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('sigs.id'), primary_key=True)
    seqrelwhenunit: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Sigs'] = sa_relationship(back_populates='seqrelwhenunit_items')

class sigs_TimingMap(EntityBase, Base):
    __tablename__ = 'sigs_timing'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('sigs.id'), primary_key=True)
    timing: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Sigs'] = sa_relationship(back_populates='timing_items')

class Studies(EntityBase, Base):
    __tablename__ = 'studies'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'studies.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['sponsor', 'study_group']
    derived_columns = []

    enum_lookup = {
        'registry': Studies_RegistryEnum,
        'study_design': Studies_Study_designEnum,
        'sponsor_type': Studies_Sponsor_typeEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('study', 'condition', 'biomarker', name='uq_studies_natural_key'),
    )

    biomarker: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    condition_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    enrollment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phase: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    protocol: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    pubs_in_hemonc: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reg_study: Mapped[bool] = mapped_column(Boolean, nullable=False)
    registry: Mapped[Optional[Studies_RegistryEnum]] = mapped_column(Enum(Studies_RegistryEnum), nullable=True)
    sact: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    sponsor_type: Mapped[Optional[Studies_Sponsor_typeEnum]] = mapped_column(Enum(Studies_Sponsor_typeEnum), nullable=True)
    start: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    study: Mapped[str] = mapped_column(String(255), nullable=False)
    study_design: Mapped[Studies_Study_designEnum] = mapped_column(Enum(Studies_Study_designEnum), nullable=False)
    study_design_imputed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    trial_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    unreg_study: Mapped[bool] = mapped_column(Boolean, nullable=False)

    normalisation_groups = [
        ['study_group', 'study_group'],
    ]
    sponsor_items: Mapped[list['studies_SponsorMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    study_group_items: Mapped[list['studies_Study_groupMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    condition_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="Studies.condition == foreign(Conditions.condition)",
        lazy='selectin',
        viewonly=True,
    )

    condition_cui_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="Studies.condition_cui == foreign(Conditions.condition_cui)",
        lazy='selectin',
        viewonly=True,
    )


class studies_SponsorMap(EntityBase, Base):
    __tablename__ = 'studies_sponsor'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('studies.id'), primary_key=True)
    sponsor: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Studies'] = sa_relationship(back_populates='sponsor_items')

class studies_Study_groupMap(EntityBase, Base):
    __tablename__ = 'studies_study_group'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('studies.id'), primary_key=True)
    study_group: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Studies'] = sa_relationship(back_populates='study_group_items')

class StudyEligibility(EntityBase, Base):
    __tablename__ = 'study_eligibility'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'study_eligibility beta.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['study_name']
    derived_columns = []

    enum_lookup = {}

    __table_args__ = (
        sa.UniqueConstraint('study_id', 'condition', 'biomarker', name='uq_study_eligibility_natural_key'),
    )

    age: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    age_unit: Mapped[str] = mapped_column(String(255), nullable=False)
    biomarker: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    other: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    prior_lines: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    prior_lines_exact: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    prior_lines_type: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ps: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ps_type: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    race: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[str] = mapped_column(String(255), nullable=False)
    stage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    study_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    normalisation_groups = [
    ]
    study_name_items: Mapped[list['study_eligibility_Study_nameMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    condition_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="StudyEligibility.condition == foreign(Conditions.condition)",
        lazy='selectin',
        viewonly=True,
    )


class study_eligibility_Study_nameMap(EntityBase, Base):
    __tablename__ = 'study_eligibility_study_name'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('study_eligibility.id'), primary_key=True)
    study_name: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['StudyEligibility'] = sa_relationship(back_populates='study_name_items')

class StudyResults(EntityBase, Base):
    __tablename__ = 'study_results'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'study_results.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['comparator_code', 'efficacy', 'estci', 'toxicity']
    derived_columns = []

    enum_lookup = {
        'endpoint_class': StudyResults_Endpoint_classEnum,
        'endpoint_type': StudyResults_Endpoint_typeEnum,
        'arm_type': StudyResults_Arm_typeEnum,
        'metricunit': StudyResults_MetricunitEnum,
        'statistic': StudyResults_StatisticEnum,
    }

    __table_args__ = (
        sa.UniqueConstraint('study', 'condition', 'biomarker', 'context', 'regimen', 'r_modifier', 'comparator', 'c_modifier', 'endpoint', 'metric', 'metric_version', name='uq_study_results_natural_key'),
    )

    arm_type: Mapped[Optional[StudyResults_Arm_typeEnum]] = mapped_column(Enum(StudyResults_Arm_typeEnum), nullable=True)
    biomarker: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    c_modifier: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    comparator: Mapped[str] = mapped_column(Text, nullable=False)
    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    condition_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    context: Mapped[str] = mapped_column(String(255), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    endpoint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    endpoint_class: Mapped[Optional[StudyResults_Endpoint_classEnum]] = mapped_column(Enum(StudyResults_Endpoint_classEnum), nullable=True)
    endpoint_type: Mapped[Optional[StudyResults_Endpoint_typeEnum]] = mapped_column(Enum(StudyResults_Endpoint_typeEnum), nullable=True)
    error: Mapped[bool] = mapped_column(Boolean, nullable=False)
    estimate: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    estlb: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    estub: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metric: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metric_version: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metricnumthatarm: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metricnumthisarm: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metricunit: Mapped[Optional[StudyResults_MetricunitEnum]] = mapped_column(Enum(StudyResults_MetricunitEnum), nullable=True)
    r_modifier: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen: Mapped[str] = mapped_column(String(255), nullable=False)
    statistic: Mapped[Optional[StudyResults_StatisticEnum]] = mapped_column(Enum(StudyResults_StatisticEnum), nullable=True)
    study: Mapped[str] = mapped_column(String(255), nullable=False)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    normalisation_groups = [
    ]
    comparator_code_items: Mapped[list['study_results_Comparator_codeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    efficacy_items: Mapped[list['study_results_EfficacyMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    estci_items: Mapped[list['study_results_EstciMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    toxicity_items: Mapped[list['study_results_ToxicityMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    condition_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="StudyResults.condition == foreign(Conditions.condition)",
        lazy='selectin',
        viewonly=True,
    )

    condition_cui_obj: Mapped[Optional['Conditions']] = sa_relationship(
        'Conditions',
        primaryjoin="StudyResults.condition_cui == foreign(Conditions.condition_cui)",
        lazy='selectin',
        viewonly=True,
    )


class study_results_Comparator_codeMap(EntityBase, Base):
    __tablename__ = 'study_results_comparator_code'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('study_results.id'), primary_key=True)
    comparator_code: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['StudyResults'] = sa_relationship(back_populates='comparator_code_items')

class study_results_EfficacyMap(EntityBase, Base):
    __tablename__ = 'study_results_efficacy'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('study_results.id'), primary_key=True)
    efficacy: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['StudyResults'] = sa_relationship(back_populates='efficacy_items')

class study_results_EstciMap(EntityBase, Base):
    __tablename__ = 'study_results_estci'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('study_results.id'), primary_key=True)
    estci: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['StudyResults'] = sa_relationship(back_populates='estci_items')

class study_results_ToxicityMap(EntityBase, Base):
    __tablename__ = 'study_results_toxicity'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('study_results.id'), primary_key=True)
    toxicity: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['StudyResults'] = sa_relationship(back_populates='toxicity_items')

class Variants(EntityBase, Base):
    __tablename__ = 'variants'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'variants.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['blob', 'study', 'tracer']
    derived_columns = []

    enum_lookup = {}

    __table_args__ = (
        sa.UniqueConstraint('variant_cui', 'version', name='uq_variants_natural_key'),
    )

    allsigshavecyclesigs: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshavedose: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshavedoseunit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshaveduration: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshavedurationunit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshavefrequency: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshaveroute: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshaveschedule: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allsigshavesequence: Mapped[bool] = mapped_column(Boolean, nullable=False)
    blob_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
    branches: Mapped[int] = mapped_column(BigInteger, nullable=False)
    components: Mapped[int] = mapped_column(BigInteger, nullable=False)
    cyclesigs: Mapped[int] = mapped_column(BigInteger, nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_study_modified: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    date_tracer_modified: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fullyspecified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    portions: Mapped[int] = mapped_column(BigInteger, nullable=False)
    regimen: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    routes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sigs: Mapped[int] = mapped_column(BigInteger, nullable=False)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    timings: Mapped[int] = mapped_column(BigInteger, nullable=False)
    variant: Mapped[str] = mapped_column(String(255), nullable=False)
    variant_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    version: Mapped[int] = mapped_column(BigInteger, nullable=False)

    normalisation_groups = [
        ['study', 'study'],
        ['tracer', 'tracer'],
    ]
    blob_items: Mapped[list['variants_BlobMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    study_items: Mapped[list['variants_StudyMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    tracer_items: Mapped[list['variants_TracerMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class variants_BlobMap(EntityBase, Base):
    __tablename__ = 'variants_blob'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('variants.id'), primary_key=True)
    blob: Mapped[str] = mapped_column(Text, primary_key=True)

    parent: Mapped['Variants'] = sa_relationship(back_populates='blob_items')

class variants_StudyMap(EntityBase, Base):
    __tablename__ = 'variants_study'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('variants.id'), primary_key=True)
    study: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Variants'] = sa_relationship(back_populates='study_items')

class variants_TracerMap(EntityBase, Base):
    __tablename__ = 'variants_tracer'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('variants.id'), primary_key=True)
    tracer: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Variants'] = sa_relationship(back_populates='tracer_items')

class VariantEligibility(EntityBase, Base):
    __tablename__ = 'variant_eligibility'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    filename = 'variant_eligibility.csv'
    pk_columns = ['id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['study']
    derived_columns = []

    enum_lookup = {}

    __table_args__ = (
        sa.UniqueConstraint('variant_cui', 'logic_count', name='uq_variant_eligibility_natural_key'),
    )

    date_added: Mapped[str] = mapped_column(String(255), nullable=False)
    logic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    logic_count: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen: Mapped[str] = mapped_column(String(255), nullable=False)
    regimen_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    string: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    unit_cui: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    variant_cui: Mapped[str] = mapped_column(String(255), nullable=False)

    normalisation_groups = [
        ['study', 'study'],
    ]
    study_items: Mapped[list['variant_eligibility_StudyMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    unit_obj: Mapped[Optional['Units']] = sa_relationship(
        'Units',
        primaryjoin="VariantEligibility.unit == foreign(Units.unit)",
        lazy='selectin',
        viewonly=True,
    )


class variant_eligibility_StudyMap(EntityBase, Base):
    __tablename__ = 'variant_eligibility_study'

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('variant_eligibility.id'), primary_key=True)
    study: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['VariantEligibility'] = sa_relationship(back_populates='study_items')

class Canonicaltriples(EntityBase, Base):
    __tablename__ = 'canonicaltriples'
    filename = 'canonical.triples.csv'
    pk_columns = ['class_1', 'relationship', 'class_2']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['class_1_provenance', 'class_2_provenance']
    derived_columns = []

    enum_lookup = {
        'class_1': Canonicaltriples_Class_1Enum,
    }

    class_1: Mapped[Canonicaltriples_Class_1Enum] = mapped_column(Enum(Canonicaltriples_Class_1Enum), primary_key=True, nullable=False)
    class_2: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    date_added: Mapped[str] = mapped_column(String(255), nullable=False)
    date_deprecated: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    index: Mapped[str] = mapped_column(String(255), nullable=False)
    internal: Mapped[bool] = mapped_column(Boolean, nullable=False)
    relationship: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    used_in: Mapped[str] = mapped_column(String(255), nullable=False)

    normalisation_groups = [
    ]
    class_1_provenance_items: Mapped[list['canonicaltriples_Class_1_provenanceMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    class_2_provenance_items: Mapped[list['canonicaltriples_Class_2_provenanceMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class canonicaltriples_Class_1_provenanceMap(EntityBase, Base):
    __tablename__ = 'canonicaltriples_class_1_provenance'

    class_1: Mapped[Canonicaltriples_Class_1Enum] = mapped_column(Enum(Canonicaltriples_Class_1Enum), primary_key=True)
    relationship: Mapped[str] = mapped_column(String(255), primary_key=True)
    class_2: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['class_1', 'relationship', 'class_2'], ['canonicaltriples.class_1', 'canonicaltriples.relationship', 'canonicaltriples.class_2']),
    )
    class_1_provenance: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Canonicaltriples'] = sa_relationship(back_populates='class_1_provenance_items')

class canonicaltriples_Class_2_provenanceMap(EntityBase, Base):
    __tablename__ = 'canonicaltriples_class_2_provenance'

    class_1: Mapped[Canonicaltriples_Class_1Enum] = mapped_column(Enum(Canonicaltriples_Class_1Enum), primary_key=True)
    relationship: Mapped[str] = mapped_column(String(255), primary_key=True)
    class_2: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['class_1', 'relationship', 'class_2'], ['canonicaltriples.class_1', 'canonicaltriples.relationship', 'canonicaltriples.class_2']),
    )
    class_2_provenance: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Canonicaltriples'] = sa_relationship(back_populates='class_2_provenance_items')

class HemoncClasses(EntityBase, Base):
    __tablename__ = 'hemonc_classes'
    filename = 'hemonc_classes.csv'
    pk_columns = ['concept_class_id']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['secondary_home_as_cui', 'secondary_home_as_string']
    derived_columns = []

    enum_lookup = {
        'omopdomain_id': HemoncClasses_Omopdomain_idEnum,
        'omopstandard_concept': HemoncClasses_Omopstandard_conceptEnum,
        'class_type': HemoncClasses_Class_typeEnum,
    }

    class_type: Mapped[HemoncClasses_Class_typeEnum] = mapped_column(Enum(HemoncClasses_Class_typeEnum), nullable=False)
    concept_class_id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    date_added: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    date_deprecated: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    omopdomain_id: Mapped[Optional[HemoncClasses_Omopdomain_idEnum]] = mapped_column(Enum(HemoncClasses_Omopdomain_idEnum), nullable=True)
    omopstandard_concept: Mapped[Optional[HemoncClasses_Omopstandard_conceptEnum]] = mapped_column(Enum(HemoncClasses_Omopstandard_conceptEnum), nullable=True)
    primary_field: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_table: Mapped[str] = mapped_column(String(255), nullable=False)

    normalisation_groups = [
    ]
    secondary_home_as_cui_items: Mapped[list['hemonc_classes_Secondary_home_as_cuiMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    secondary_home_as_string_items: Mapped[list['hemonc_classes_Secondary_home_as_stringMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class hemonc_classes_Secondary_home_as_cuiMap(EntityBase, Base):
    __tablename__ = 'hemonc_classes_secondary_home_as_cui'

    concept_class_id: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['concept_class_id'], ['hemonc_classes.concept_class_id']),
    )
    secondary_home_as_cui: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['HemoncClasses'] = sa_relationship(back_populates='secondary_home_as_cui_items')

class hemonc_classes_Secondary_home_as_stringMap(EntityBase, Base):
    __tablename__ = 'hemonc_classes_secondary_home_as_string'

    concept_class_id: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['concept_class_id'], ['hemonc_classes.concept_class_id']),
    )
    secondary_home_as_string: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['HemoncClasses'] = sa_relationship(back_populates='secondary_home_as_string_items')

class HemoncRels(EntityBase, Base):
    __tablename__ = 'hemonc_rels'
    filename = 'hemonc_rels.csv'
    pk_columns = ['relationship_id']
    source_defined_keys = ['relationship_id']
    identity_keys = []
    denormalised_columns = []
    derived_columns = []

    enum_lookup = {}

    date_added: Mapped[str] = mapped_column(String(255), nullable=False)
    date_deprecated: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    heritable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    relationship_id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')

    normalisation_groups = [
    ]

class Affiliations(EntityBase, Base):
    __tablename__ = 'affiliations'
    filename = 'affiliations.csv'
    pk_columns = ['pmid', 'sequence', 'aff_no']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = ['affiliation_europmc', 'affiliation_hemonc', 'affiliation_journal']
    derived_columns = []

    enum_lookup = {}

    aff_no: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, default=-1)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fullname_europmc: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    fullname_hemonc: Mapped[str] = mapped_column(String(255), nullable=False)
    person_cui: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pmid: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, default=-1)
    sequence: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, default=-1)
    temp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    valid_city: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    valid_country: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    valid_region: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    valid_site: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    normalisation_groups = [
    ]
    affiliation_europmc_items: Mapped[list['affiliations_Affiliation_europmcMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    affiliation_hemonc_items: Mapped[list['affiliations_Affiliation_hemoncMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    affiliation_journal_items: Mapped[list['affiliations_Affiliation_journalMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    pmid_exclusions_obj: Mapped[Optional['Exclusions']] = sa_relationship(
        'Exclusions',
        primaryjoin="Affiliations.pmid == foreign(Exclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )

    pmid_inclusions_obj: Mapped[Optional['Inclusions']] = sa_relationship(
        'Inclusions',
        primaryjoin="Affiliations.pmid == foreign(Inclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )

    person_cui_obj: Mapped[Optional['Persons']] = sa_relationship(
        'Persons',
        primaryjoin="Affiliations.person_cui == foreign(Persons.person_cui)",
        lazy='selectin',
        viewonly=True,
    )


class affiliations_Affiliation_europmcMap(EntityBase, Base):
    __tablename__ = 'affiliations_affiliation_europmc'

    pmid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sequence: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    aff_no: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['pmid', 'sequence', 'aff_no'], ['affiliations.pmid', 'affiliations.sequence', 'affiliations.aff_no']),
    )
    affiliation_europmc: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Affiliations'] = sa_relationship(back_populates='affiliation_europmc_items')

class affiliations_Affiliation_hemoncMap(EntityBase, Base):
    __tablename__ = 'affiliations_affiliation_hemonc'

    pmid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sequence: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    aff_no: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['pmid', 'sequence', 'aff_no'], ['affiliations.pmid', 'affiliations.sequence', 'affiliations.aff_no']),
    )
    affiliation_hemonc: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Affiliations'] = sa_relationship(back_populates='affiliation_hemonc_items')

class affiliations_Affiliation_journalMap(EntityBase, Base):
    __tablename__ = 'affiliations_affiliation_journal'

    pmid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    sequence: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    aff_no: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['pmid', 'sequence', 'aff_no'], ['affiliations.pmid', 'affiliations.sequence', 'affiliations.aff_no']),
    )
    affiliation_journal: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Affiliations'] = sa_relationship(back_populates='affiliation_journal_items')





class Contexttable(EntityBase, Base):
    __tablename__ = 'contexttable'
    filename = 'context.table.csv'
    pk_columns = ['contextraw']
    source_defined_keys = ['contextraw']
    identity_keys = []
    denormalised_columns = ['contextpretty', 'phenotype', 'setting', 'stage_or_status']
    derived_columns = []

    enum_lookup = {
        'intent': Contexttable_IntentEnum,
        'phase': Contexttable_PhaseEnum,
        'risk_stratification': Contexttable_Risk_stratificationEnum,
        'therapy_type': Contexttable_Therapy_typeEnum,
    }

    contextraw: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    intent: Mapped[Contexttable_IntentEnum] = mapped_column(Enum(Contexttable_IntentEnum), nullable=False)
    phase: Mapped[Optional[Contexttable_PhaseEnum]] = mapped_column(Enum(Contexttable_PhaseEnum), nullable=True)
    prior_therapy: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    prior_therapy_negation: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    risk_stratification: Mapped[Optional[Contexttable_Risk_stratificationEnum]] = mapped_column(Enum(Contexttable_Risk_stratificationEnum), nullable=True)
    therapy_type: Mapped[Optional[Contexttable_Therapy_typeEnum]] = mapped_column(Enum(Contexttable_Therapy_typeEnum), nullable=True)

    normalisation_groups = [
    ]
    contextpretty_items: Mapped[list['contexttable_ContextprettyMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    phenotype_items: Mapped[list['contexttable_PhenotypeMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    setting_items: Mapped[list['contexttable_SettingMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    stage_or_status_items: Mapped[list['contexttable_Stage_or_statusMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class contexttable_ContextprettyMap(EntityBase, Base):
    __tablename__ = 'contexttable_contextpretty'

    contextraw: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['contextraw'], ['contexttable.contextraw']),
    )
    contextpretty: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Contexttable'] = sa_relationship(back_populates='contextpretty_items')

class contexttable_PhenotypeMap(EntityBase, Base):
    __tablename__ = 'contexttable_phenotype'

    contextraw: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['contextraw'], ['contexttable.contextraw']),
    )
    phenotype: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Contexttable'] = sa_relationship(back_populates='phenotype_items')

class contexttable_SettingMap(EntityBase, Base):
    __tablename__ = 'contexttable_setting'

    contextraw: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['contextraw'], ['contexttable.contextraw']),
    )
    setting: Mapped[str] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Contexttable'] = sa_relationship(back_populates='setting_items')

class contexttable_Stage_or_statusMap(EntityBase, Base):
    __tablename__ = 'contexttable_stage_or_status'

    contextraw: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['contextraw'], ['contexttable.contextraw']),
    )
    stage_or_status: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['Contexttable'] = sa_relationship(back_populates='stage_or_status_items')

class Exclusions(EntityBase, Base):
    __tablename__ = 'exclusions'
    filename = 'exclusions.csv'
    pk_columns = ['pmid']
    source_defined_keys = ['pmid']
    identity_keys = []
    denormalised_columns = ['title']
    derived_columns = []

    enum_lookup = {
        'rev1': Exclusions_Rev1Enum,
    }

    date_added: Mapped[str] = mapped_column(String(255), nullable=False)
    pmid: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    rev1: Mapped[Exclusions_Rev1Enum] = mapped_column(Enum(Exclusions_Rev1Enum), nullable=False)
    rev2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rev3: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    year: Mapped[str] = mapped_column(String(255), nullable=False)

    normalisation_groups = [
    ]
    title_items: Mapped[list['exclusions_TitleMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    pmid_obj: Mapped[Optional['Inclusions']] = sa_relationship(
        'Inclusions',
        primaryjoin="Exclusions.pmid == foreign(Inclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )


class exclusions_TitleMap(EntityBase, Base):
    __tablename__ = 'exclusions_title'

    pmid: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['pmid'], ['exclusions.pmid']),
    )
    title: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Exclusions'] = sa_relationship(back_populates='title_items')



class Inclusions(EntityBase, Base):
    __tablename__ = 'inclusions'
    filename = 'inclusions.csv'
    pk_columns = ['pmid']
    source_defined_keys = ['pmid']
    identity_keys = []
    denormalised_columns = ['reason_note']
    derived_columns = []

    enum_lookup = {
        'ref_type': Inclusions_Ref_typeEnum,
        'reason': Inclusions_ReasonEnum,
    }

    date_added: Mapped[str] = mapped_column(String(255), nullable=False)
    pmid: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, default=-1)
    reason: Mapped[Inclusions_ReasonEnum] = mapped_column(Enum(Inclusions_ReasonEnum), nullable=False)
    ref_type: Mapped[Inclusions_Ref_typeEnum] = mapped_column(Enum(Inclusions_Ref_typeEnum), nullable=False)

    normalisation_groups = [
    ]
    reason_note_items: Mapped[list['inclusions_Reason_noteMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')
    pmid_obj: Mapped[Optional['Exclusions']] = sa_relationship(
        'Exclusions',
        primaryjoin="Inclusions.pmid == foreign(Exclusions.pmid)",
        lazy='selectin',
        viewonly=True,
    )


class inclusions_Reason_noteMap(EntityBase, Base):
    __tablename__ = 'inclusions_reason_note'

    pmid: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['pmid'], ['inclusions.pmid']),
    )
    reason_note: Mapped[Optional[str]] = mapped_column(Text, primary_key=True)

    parent: Mapped['Inclusions'] = sa_relationship(back_populates='reason_note_items')









class SigBranchTypes(EntityBase, Base):
    __tablename__ = 'sig_branch_types'
    filename = 'sig_branch_types.csv'
    pk_columns = ['value']
    source_defined_keys = ['value']
    identity_keys = []
    denormalised_columns = ['description']
    derived_columns = []

    enum_lookup = {}

    value: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')

    normalisation_groups = [
    ]
    description_items: Mapped[list['sig_branch_types_DescriptionMap']] = sa_relationship(back_populates='parent', lazy='selectin', cascade='all, delete-orphan')

class sig_branch_types_DescriptionMap(EntityBase, Base):
    __tablename__ = 'sig_branch_types_description'

    value: Mapped[str] = mapped_column(String(255), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['value'], ['sig_branch_types.value']),
    )
    description: Mapped[Optional[str]] = mapped_column(String(255), primary_key=True)

    parent: Mapped['SigBranchTypes'] = sa_relationship(back_populates='description_items')



class Units(EntityBase, Base):
    __tablename__ = 'units'
    filename = 'units.csv'
    pk_columns = ['unit']
    source_defined_keys = ['unit']
    identity_keys = []
    denormalised_columns = []
    derived_columns = []

    enum_lookup = {
        'unit_type': Units_Unit_typeEnum,
    }

    concept_code: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    date_added: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    unit_type: Mapped[Units_Unit_typeEnum] = mapped_column(Enum(Units_Unit_typeEnum), nullable=False)

    normalisation_groups = [
    ]

class Variantblob(EntityBase, Base):
    __tablename__ = 'variantblob'
    filename = 'variant.blob.csv'
    pk_columns = ['version', 'chunk']
    source_defined_keys = []
    identity_keys = []
    denormalised_columns = []
    derived_columns = []

    enum_lookup = {
        'block': Variantblob_BlockEnum,
        'chunk_type': Variantblob_Chunk_typeEnum,
    }

    block: Mapped[Variantblob_BlockEnum] = mapped_column(Enum(Variantblob_BlockEnum), nullable=False)
    chunk: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, default='')
    chunk_type: Mapped[Variantblob_Chunk_typeEnum] = mapped_column(Enum(Variantblob_Chunk_typeEnum), nullable=False)
    date_created: Mapped[str] = mapped_column(String(255), nullable=False)
    date_retired: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    order: Mapped[int] = mapped_column(BigInteger, nullable=False)
    version: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False, default=-1)

    normalisation_groups = [
    ]

