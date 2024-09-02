import enum

class DrugClassType(enum.Enum):
    mechanistic = 0
    biochemical = 1
    nonspecific = 2
    functional = 3

class ComponentRole(enum.Enum):
    primary_systemic = 0
    secondary_systemic = 1
    locoregional = 2

class TherapyType(enum.Enum):
    local = 0
    systemic = 1
    tbd = 2

class TimingUnit(enum.Enum):
    cycle = 0
    course = 1
    week = 2
    day = 3
    month = 4

class Intent(enum.Enum):
    non_curative = 0
    curative = 1
    unspecified = 2
    not_applicable = 3
    prevention = 4
    tbd = 5

class Setting(enum.Enum):
    any = 0
    first_line = 1
    second_line = 2
    third_line = 3
    fourth_line = 4
    second_or_third_line = 5
    upfront = 6
    subsequent_line = 7
    exposed = 8
    unexposed = 9
    salvage = 10
    unspecified = 11
    tbd = 12

class Phase(enum.Enum):
    consolidation = 0
    adjuvant = 1
    maintenance = 2
    early_intensification = 3
    perioperative = 4
    pre_phase = 5
    neoadjuvant = 6
    late_intensification = 7
    delayed_intensification = 8
    tbd = 9
    intensification = 10
    interim_maintenance = 11
    induction = 12
    definitive = 13    
    
class BranchConditionalType(enum.Enum):
    stage = 0
    size = 1
    age = 2
    lab = 3
    fact = 4
    other = 7

class BranchType(enum.Enum):
    renal_function = 0
    complex = 1
    donor = 2
    histology = 3
    site = 4
    other = 5
    risk = 6
    route = 7
    mutation = 8
    imaging = 9
    race = 10
    exposure = 11
    comorbidity = 12
    study = 13
    stage = 14
    undefined = 15
    specific = 16
    bmi = 17
    bsa = 18
    weight = 19
    symptom = 20
    laboratory = 21
    performance = 22
    response = 23
    age = 24

class Risk(enum.Enum):
    favorable = 0
    low_risk = 1
    intermediate_risk = 2
    high_risk = 3
    unfavorable = 4
    unstratified = 5
    tbd = 6

class Phenotype(enum.Enum):
    platinum_eligible = 0
    platinum_sensitive = 1
    platinum_refractory = 2
    platinum_ineligible = 3
    fu_refractory = 4
    gemcitabine_refractory = 5
    younger_children = 6
    older_children = 7
    standard = 8
    premenopausal = 9
    postmenopausal = 10
    older_fit = 11
    older_or_unfit = 2
    elderly = 13
    elderly_or_poor_performance_status = 4
    transplant_ineligible_or_progressed_after_transplant = 15
    castrate_sensitive = 16
    castrate_resistant = 17
    tbd = 18

class PriorTherapy(enum.Enum):
    platinum_and_or_ici = 0
    castration = 1
    radioactive_iodine = 2
    ros1_inhibitor = 3
    fu = 4
    braf_inhibitor = 5
    tki = 6
    platinum = 7
    gemcitabine = 8
    egfr_inhibitor = 9
    alk_inhibitor = 10
    surgery = 11
    none = 12
    tbd = 13
    
class DrugClassRelationshipType(enum.Enum):
    major = 0
    canmed_major = 1
    canmed_minor = 2

class StudyDesign(enum.Enum):
    non_randomized = 0
    cbd = 1
    escalation = 2
    in_class_switch = 3
    out_of_class_switch = 4
    de_escalation = 5
    mixed = 6
    not_stated = 7
    randomized = 8

class SponsorType(enum.Enum):
    cooperative_group = 0
    pharmaceutical_industry = 1
    academic_medical_center = 2
    government = 3
    community_practice = 4
    academic_consortium = 5

class Modality(enum.Enum):
    antibiotic_therapy = 0
    anticoagulation = 1
    chemotherapy = 2
    endocrine_therapy = 3
    glucocorticoid_therapy = 4
    immunosuppressive_therapy = 5
    immunotherapy = 6
    growth_factor_therapy = 7
    null_therapy = 8
    radiotherapy = 9
    supportive_therapy = 10
    targeted_therapy = 11
    tumor_treating_fields = 12
    radioconjugate_therapy = 13
    antibody_drug_conjugate_therapy = 14
    immunotoxin_therapy = 15
    peptide_drug_conjugate_therapy = 16