from .entity_base import *

class Authors_RoleEnum(enum.Enum):
    FIRST_AUTHOR = 'First author'
    CO_TO_FIRST_AUTHOR = 'co-First author'
    SECOND_AUTHOR = 'Second author'
    MIDDLE_AUTHOR = 'Middle author'
    CO_TO_LAST_AUTHOR = 'co-Last author'
    LAST_AUTHOR = 'Last author'

class Authors_Site_typeEnum(enum.Enum):
    ACADEMIC_MEDICAL_CENTER = 'Academic medical center'
    GOVERNMENT = 'Government'
    NCI_TO_CC = 'NCI-CC'
    NCI_TO_CCC = 'NCI-CCC'
    PHARMACEUTICAL_INDUSTRY = 'Pharmaceutical industry'
    NO_DATA_DEFAULT_ = 'No data (default)'

class CanonicalTriples_Class_1Enum(enum.Enum):
    PROCEDURE = 'Procedure'
    REGIMEN = 'Regimen'
    ANY_CONCEPT = 'Any concept'
    COMPONENT = 'Component'
    STUDY = 'Study'
    SYNTHETIC_REGIMEN = 'Synthetic Regimen'
    REGIMEN_CLASS = 'Regimen Class'
    REFERENCE = 'Reference'
    COMPONENT_CLASS = 'Component Class'
    CONDITION = 'Condition'
    CONTEXT = 'Context'
    REGIMEN_STUB = 'Regimen Stub'
    REGIMEN_VARIANT = 'Regimen Variant'

class Conditions_Age_focusEnum(enum.Enum):
    ADULT = 'Adult'
    PEDIATRIC = 'Pediatric'
    UNDEFINED = 'Undefined'

class Conditions_Condition_typeEnum(enum.Enum):
    BREAST = 'Breast'
    CLASSICAL_HEMATOLOGY = 'Classical hematology'
    CNS = 'CNS'
    DERMATOLOGIC = 'Dermatologic'
    ENDOCRINE = 'Endocrine'
    GASTROINTESTINAL = 'Gastrointestinal'
    GENITOURINARY = 'Genitourinary'
    GYNECOLOGIC = 'Gynecologic'
    HEAD_NECK = 'Head & Neck'
    LYMPHOID = 'Lymphoid'
    MYELOID = 'Myeloid'
    NET = 'NET'
    OTHER = 'Other'
    OTHER_HEMATOLOGIC_NEOPLASM = 'Other hematologic neoplasm'
    OTHER_NEOPLASM = 'Other neoplasm'
    OTHER_SOLID_NEOPLASM = 'Other solid neoplasm'
    PLASMA_CELL = 'Plasma cell'
    SARCOMA = 'Sarcoma'
    THORACIC = 'Thoracic'

class Conditions_Map_type_icd10cmEnum(enum.Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR_ = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR_ = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT_ = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_icd9cmEnum(enum.Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR_ = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR_ = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT_ = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_icdo3Enum(enum.Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR_ = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR_ = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT_ = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_icdo3_morphEnum(enum.Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR_ = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR_ = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT_ = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_ncitEnum(enum.Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR_ = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR_ = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT_ = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_oncotreeEnum(enum.Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR_ = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR_ = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT_ = 'sideways (semantic equivalence but not exact)'

class Conditions_SectionEnum(enum.Enum):
    ACUTE_LEUKEMIA = 'Acute leukemia'
    AGGRESSIVE_LYMPHOMA = 'Aggressive lymphoma'
    BREAST_ONCOLOGY = 'Breast Oncology'
    CYTOPENIAS = 'Cytopenias'
    DERMATOLOGIC_ONCOLOGY = 'Dermatologic Oncology'
    DISEASE_TO_AGNOSTIC = 'Disease-agnostic'
    ENDOCRINE_ONCOLOGY = 'Endocrine Oncology'
    GENITORURINARY_ONCOLOGY = 'Genitorurinary Oncology'
    GI_ONCOLOGY_EXTRAINTESTINAL = 'GI Oncology, extraintestinal'
    GI_ONCOLOGY_INTESTINAL = 'GI Oncology, intestinal'
    GYNECOLOGIC_ONCOLOGY = 'Gynecologic Oncology'
    HEAD_NECK_ONCOLOGY = 'Head & Neck Oncology'
    HEMOGLOBINOPATHIES = 'Hemoglobinopathies'
    HEMOLYTIC_DISORDERS = 'Hemolytic disorders'
    HEMOSTASIS_AND_THROMBOSIS = 'Hemostasis and thrombosis'
    HISTIOCYTE_DISORDERS = 'Histiocyte disorders'
    INDOLENT_LYMPHOMA = 'Indolent lymphoma'
    LYMPHOPROLIFERATIVE_DISORDERS = 'Lymphoproliferative disorders'
    MESOTHELIOMA = 'Mesothelioma'
    MYELOPROLIFERATIVE_NEOPLASMS_AND_MYELODYSPLASTIC_SYNDROMES = 'Myeloproliferative neoplasms and myelodysplastic syndromes'
    NEURO_TO_ONCOLOGY = 'Neuro-Oncology'
    PEDIATRIC_CNS_MALIGNANCIES = 'Pediatric CNS malignancies'
    PEDIATRIC_HEMATOLOGIC_NEOPLASMS = 'Pediatric hematologic neoplasms'
    PEDIATRIC_SOLID_TUMORS = 'Pediatric solid tumors'
    PLASMA_CELL_DYSCRASIAS = 'Plasma cell dyscrasias'
    SARCOMA = 'Sarcoma'
    T_TO_CELL_AND_NK_TO_CELL_NEOPLASMS = 'T-cell and NK-cell neoplasms'
    THORACIC_ONCOLOGY = 'Thoracic Oncology'
    TRANSPLANT_AND_IEC = 'Transplant and IEC'
    BLANK_NO_EDITORIAL_BOARD_MAPPING_ = 'blank (no editorial board mapping)'

class ContextTable_IntentEnum(enum.Enum):
    NON_TO_CURATIVE = 'non-curative'
    NOT_APPLICABLE = 'not applicable'
    CURATIVE = 'curative'
    UNSPECIFIED = 'unspecified'
    PREVENTION = 'prevention'

class ContextTable_PhaseEnum(enum.Enum):
    ADJUVANT = 'Adjuvant'
    CONSOLIDATION = 'Consolidation'
    DEFINITIVE = 'Definitive'
    DELAYED_INTENSIFICATION = 'Delayed intensification'
    EARLY_INTENSIFICATION = 'Early Intensification'
    INDUCTION = 'Induction'
    MAINTENANCE = 'Maintenance'
    INTENSIFICATION = 'Intensification'
    PRE_TO_PHASE = 'Pre-phase'
    INTERIM_MAINTENANCE = 'Interim Maintenance'
    LATE_INTENSIFICATION = 'Late Intensification'
    NEOADJUVANT = 'Neoadjuvant'
    PERIOPERATIVE = 'Perioperative'

class ContextTable_Risk_stratificationEnum(enum.Enum):
    HIGH_TO_RISK = 'high-risk'
    INTERMEDIATE_TO_RISK = 'intermediate-risk'
    LOW_TO_RISK = 'low-risk'
    UNSTRATIFIED = 'unstratified'
    FAVORABLE = 'favorable'
    UNFAVORABLE = 'unfavorable'
    STANDARD_TO_RISK = 'standard-risk'
    VERY_HIGH_TO_RISK = 'very high-risk'

class ContextTable_Therapy_typeEnum(enum.Enum):
    CHEMORADIOTHERAPY = 'chemoradiotherapy'
    CHEMOTHERAPY = 'chemotherapy'
    ANTICOAGULATION = 'anticoagulation'
    LOCAL = 'local'
    SYSTEMIC = 'systemic'
    RADIOTHERAPY = 'radiotherapy'
    ENDOCRINE_THERAPY = 'endocrine therapy'
    REPLACEMENT_PRODUCTS = 'Replacement products'
    IMMUNOTHERAPY = 'immunotherapy'
    INTRAPERITONEAL = 'Intraperitoneal'
    ANTIBIOTIC = 'antibiotic'
    ADT_AND_RADIOTHERAPY = 'ADT and Radiotherapy'
    PERIOPERATIVE_THERAPY_AND_HYPERTHERMIC_INTRA_TO_PERITONEAL_CHEMOTHERAPY = 'perioperative therapy and hyperthermic intra-peritoneal chemotherapy'

class Drugs_Class_typeEnum(enum.Enum):
    BIOCHEMICAL = 'biochemical'
    FUNCTIONAL = 'functional'
    MECHANISTIC = 'mechanistic'
    NONSPECIFIC = 'nonspecific'

class Exclusions_Rev1Enum(enum.Enum):
    JEREMY = 'Jeremy'
    ALEENAH = 'Aleenah'

class HemoncClasses_Class_typeEnum(enum.Enum):
    CORE = 'core'
    EXTENSION = 'extension'
    INTERMEDIATE = 'intermediate'
    NUMERIC = 'numeric'
    READY_FOR_CORE = 'ready for core'

class HemoncClasses_Omopdomain_idEnum(enum.Enum):
    DRUG = 'drug'
    CONDITION = 'condition'
    PROCEDURE = 'procedure'
    MEASUREMENT = 'measurement'
    REGIMEN = 'regimen'

class HemoncClasses_Omopstandard_conceptEnum(enum.Enum):
    RXNORM = 'RxNorm'
    C = 'C'
    HEMONC = 'HemOnc'
    N_A_TO_NATIVELY_ENCODED = 'N/A - Natively encoded'

class Inclusions_ReasonEnum(enum.Enum):
    NON_TO_PHASE_3_WITH_PRIMARY_PUBLICATION_IN_HIGH_TO_IMPACT_JOURNAL = 'non-Phase 3 with primary publication in high-impact journal'
    PHASE_3_SACT = 'Phase 3 SACT'
    EXCEPTION = 'Exception'
    NON_TO_PHASE_3_PIVOTAL_STUDY = 'non-Phase 3 pivotal study'
    PHASE_3_CLASSICAL_HEMATOLOGY = 'Phase 3 classical hematology'
    NON_TO_PHASE_3_WITH_UPDATE_IN_HIGH_TO_IMPACT_JOURNAL = 'non-Phase 3 with update in high-impact journal'
    CLINICAL_PRACTICE_GUIDELINE = 'Clinical practice guideline'
    PHASE_3_GVHD = 'Phase 3 GVHD'

class Inclusions_Ref_typeEnum(enum.Enum):
    PRIMARY = 'Primary'
    EFFICACY_UPDATE = 'Efficacy update'
    UNDETERMINED = 'Undetermined'
    SAFETY_UPDATE = 'Safety update'
    OTHER_UPDATE = 'Other update'

class Indications_Age_unitEnum(enum.Enum):
    MONTH = 'month'
    YEAR = 'year'
    UNSPECIFIED = 'unspecified'

class Indications_Biomarker2Enum(enum.Enum):
    HER2 = 'HER2'
    MAGE_TO_A4_ANTIGEN = 'MAGE-A4 antigen'
    EGFR = 'EGFR'
    PR = 'PR'
    ALK = 'ALK'
    CD19 = 'CD19'
    KRAS = 'KRAS'
    PD_TO_L1 = 'PD-L1'
    CLDN18_2 = 'CLDN18.2'

class Indications_Biomarker2_findingEnum(enum.Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    _MORE_TO_COME_ = '[more to come]'

class Indications_Biomarker2_typeEnum(enum.Enum):
    CHROMOSOME = 'Chromosome'
    GENE = 'Gene'
    PROTEIN_SEE_NOTE_3_ = 'Protein [see note 3]'
    TRACER = 'Tracer'
    VIRUS = 'Virus'

class Indications_Biomarker3_findingEnum(enum.Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    _MORE_TO_COME_ = '[more to come]'

class Indications_Biomarker3_typeEnum(enum.Enum):
    CHROMOSOME = 'Chromosome'
    GENE = 'Gene'
    PROTEIN_SEE_NOTE_3_ = 'Protein [see note 3]'
    TRACER = 'Tracer'
    VIRUS = 'Virus'

class Indications_Biomarker4Enum(enum.Enum):
    PD_TO_L1 = 'PD-L1'
    ROS1 = 'ROS1'

class Indications_Biomarker4_findingEnum(enum.Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    _MORE_TO_COME_ = '[more to come]'

class Indications_Biomarker4_typeEnum(enum.Enum):
    CHROMOSOME = 'Chromosome'
    GENE = 'Gene'
    PROTEIN_SEE_NOTE_3_ = 'Protein [see note 3]'
    TRACER = 'Tracer'
    VIRUS = 'Virus'

class Indications_Biomarker_findingEnum(enum.Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    _MORE_TO_COME_ = '[more to come]'

class Indications_Biomarker_typeEnum(enum.Enum):
    CHROMOSOME = 'Chromosome'
    GENE = 'Gene'
    PROTEIN_SEE_NOTE_3_ = 'Protein [see note 3]'
    TRACER = 'Tracer'
    VIRUS = 'Virus'

class Indications_DateEnum(enum.Enum):
    YYYY_TO_MM_TO_DD_ISO_8601_ = 'YYYY-MM-DD (ISO 8601)'
    UNCERTAIN_DATE_BLANK_ = 'Uncertain date, (blank)'

class Indications_NoteEnum(enum.Enum):
    NO_LINKED_CONDITION = 'No linked condition'
    NO_MONTH_YEAR_INFORMATION = 'No month/year information'
    TO_BE_DISSECTED = 'To be dissected'

class Indications_RegulatorEnum(enum.Enum):
    FDA = 'FDA'
    EMA = 'EMA'
    HC = 'HC'
    KFDA = 'KFDA'
    NMPA = 'NMPA'
    PMDA_BLANK_ = 'PMDA, (blank)'

class Indications_SexEnum(enum.Enum):
    MEN = 'men'
    WOMEN = 'women'

class Indications_WithdrawnEnum(enum.Enum):
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    DATE_OF_INDICATION_THAT_WAS_WITHDRAWN = 'Date of indication that was withdrawn'

class Persons_GenderEnum(enum.Enum):
    MAN = 'Man'
    WOMAN = 'Woman'
    UNKNOWN = 'Unknown'
    COULD_NOT_BE_DETERMINED = 'Could not be determined'
    NOT_YET_DETERMINED = 'Not yet determined'

class Persons_Hyphen_typeEnum(enum.Enum):
    EASTERN = 'Eastern'
    WESTERN = 'Western'
    MENA = 'MENA'
    UNKNOWN = 'UNKNOWN'

class Persons_Vital_statusEnum(enum.Enum):
    _1_ALIVE_NOT_KNOWN_TO_BE_DECEASED_ = '1 = Alive (not known to be deceased)'
    _0_DECEASED_IF_YEAR_UNKNOWN_ = '0 = Deceased (if year unknown)'
    YYYY_YEAR_DECEASED = 'YYYY = Year deceased'

class Refs_BiblioEnum(enum.Enum):
    YYYY_MON = 'YYYY Mon'
    ISSUE_VOLUME_FIRST_PAGE_TO_LAST_PAGE_EPUB_YYYY_MON_DD = 'Issue(Volume):first page-last page. Epub YYYY Mon DD'

class Refs_Ref_typeEnum(enum.Enum):
    BIOMARKER_ANALYSIS = 'Biomarker analysis'
    GUIDELINE = 'Guideline'
    HRQOL_ANALYSIS = 'HRQoL analysis'
    POOLED_SUBGROUP_ANALYSIS = 'Pooled subgroup analysis'
    POOLED_UPDATE = 'Pooled update'
    PRIMARY = 'Primary'
    PRO_ANALYSIS = 'PRO analysis'
    Q_TO_TWIST_ANALYSIS = 'Q-TWiST analysis'
    SAFETY_ANALYSIS = 'Safety analysis'
    SAFETY_UPDATE = 'Safety update'
    SUBGROUP_ANALYSIS = 'Subgroup analysis'
    TWIST_ANALYSIS = 'TWiST analysis'
    UPDATE = 'Update'

class Sigs_AlldaysEnum(enum.Enum):
    STANDARD_FORMAT_1_8_15_22_ETC_ = 'Standard format: 1,8,15,22 etc.'
    ALTERNATIVE_FORMAT_FOR_LONG_SEQUENCES_FROM_TO_BY_ = 'Alternative format for long sequences: [from, to, by]'

class Sigs_Class_fieldEnum(enum.Enum):
    NON_TO_CANONICAL_SIG = 'Non-canonical Sig'
    NON_TO_IV_CANONICAL_SIG = 'Non-IV canonical Sig'
    IV_INTERMITTENT_CANONICAL_SIG = 'IV intermittent canonical Sig'
    IV_CONTINUOUS_CANONICAL_SIG = 'IV continuous canonical Sig'
    RAD_SIG = 'Rad Sig'

class Sigs_Component_roleEnum(enum.Enum):
    LOCOREGIONAL = 'locoregional'
    PRIMARY_SYSTEMIC = 'primary systemic'
    SECONDARY_SYSTEMIC = 'secondary systemic'

class Sigs_Cycle_length_ubEnum(enum.Enum):
    _1_2_3_ETC = '1, 2, 3, etc'
    NUB_NO_UPPER_BOUND_ = 'NUB (no upper bound)'
    _C_TO_CONDITIONAL_UPPER_BOUND = '(+c) - conditional upper bound'

class Sigs_Cycle_length_unitEnum(enum.Enum):
    DAYS = 'days'
    WEEKS = 'weeks'
    MONTHS = 'months'
    YEARS = 'years'
    INDETERMINATE = 'indeterminate'

class Sigs_DosecapunitEnum(enum.Enum):
    GBQ = 'GBq'
    MBQ = 'MBq'
    MCI = 'mCi'
    MG = 'mg'
    MG_DAY = 'mg/day'
    MG_M_2 = 'mg/m^2'

class Sigs_DoseunitEnum(enum.Enum):
    AUC = 'AUC'
    G_KG = 'g/kg'
    GBQ = 'GBq'
    GY = 'Gy'
    IU = 'IU'
    IU_KG = 'IU/kg'
    IU_M_2 = 'IU/m^2'
    IU_M_2_DAY = 'IU/m^2/day'
    KBQ_KG = 'kBq/kg'
    MBQ_KG = 'MBq/kg'
    MCG = 'mcg'
    MCG_DAY = 'mcg/day'
    MCG_KG = 'mcg/kg'
    MCG_M_2 = 'mcg/m^2'
    MCG_M_2_DAY = 'mcg/m^2/day'
    MCI_KG = 'mCi/kg'
    MG = 'mg'
    MG_DAY = 'mg/day'
    MG_KG = 'mg/kg'
    MG_KG_DAY = 'mg/kg/day'
    MG_M_2 = 'mg/m^2'
    MG_M_2_DAY = 'mg/m^2/day'
    MG_M_2_HR = 'mg/m^2/hr'
    PFU_ML = 'pfu/mL'
    UNITS = 'units'
    UNITS_KG = 'units/kg'
    UNITS_M_2 = 'units/m^2'
    UNITS_M_2_DAY = 'units/m^2/day'

class Sigs_DurationmaxnumEnum(enum.Enum):
    BLANK_DEFAULT_ = 'blank (default)'
    _1_23 = '1.23'

class Sigs_DurationminnumEnum(enum.Enum):
    BLANK_DEFAULT_ = 'blank (default)'
    _1_23 = '1.23'

class Sigs_DurationunitEnum(enum.Enum):
    SECOND = 'second'
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    ERROR_ = 'ERROR!'

class Sigs_FrequencyEnum(enum.Enum):
    CONTINUOUS = 'continuous'
    DAILY_NOS_EVERY_12_HOURS = 'daily NOS, every 12 hours'
    EVERY_4_HOURS = 'every 4 hours'
    EVERY_6_HOURS = 'every 6 hours'
    EVERY_8_HOURS = 'every 8 hours'
    FOUR_TIMES_PER_DAY = 'four times per day'
    ONCE = 'once'
    ONCE_EVERY_MORNING = 'once every morning'
    ONCE_EVERY_EVENING = 'once every evening'
    ONCE_PER_DAY = 'once per day'
    THREE_TIMES_PER_DAY = 'three times per day'
    TWICE = 'twice'
    TWICE_PER_DAY = 'twice per day'

class Sigs_PhaseEnum(enum.Enum):
    CONSOLIDATION = 'Consolidation'
    CONTINUATION = 'Continuation'
    DELAYED_INTENSIFICATION = 'Delayed Intensification'
    INDUCTION = 'Induction'
    INTENSIFICATION = 'Intensification'
    INTERIM_MAINTENANCE = 'Interim Maintenance'
    MAINTENANCE = 'Maintenance'
    PRE_TO_PHASE = 'Pre-phase'
    POST_TO_CONSOLIDATION = 'Post-consolidation'
    LT_MORE_TO_BE_ADDEDGT_ = '<more to be added>'
    UNSPECIFIED_DEFAULT_ = 'unspecified (default)'

class Sigs_RouteEnum(enum.Enum):
    IA = 'IA'
    IM = 'IM'
    INHALED = 'inhaled'
    INTRAVESICULARLY = 'intravesicularly'
    IP = 'IP'
    IT = 'IT'
    IV = 'IV'
    NEBULIZED = 'nebulized'
    NOT_SPECIFIED = 'Not specified'
    PO = 'PO'
    SC = 'SC'

class Sigs_SeqrelwhenunitEnum(enum.Enum):
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'

class Sigs_Step_numberEnum(enum.Enum):
    _1_OF_1_DEFAULT_ = '1  of  1 (default)'
    _1_OF_2 = '1  of  2'
    _1_OF_3 = '1  of  3'
    _1_OF_4 = '1  of  4'
    _1_OF_5 = '1  of  5'
    _2_OF_2 = '2  of  2'
    _2_OF_3 = '2  of  3'
    _2_OF_4 = '2  of  4'
    _2_OF_5 = '2  of  5'
    _3_OF_3 = '3  of  3'
    _3_OF_4 = '3  of  4'
    _3_OF_5 = '3  of  5'
    _4_OF_4 = '4  of  4'
    _4_OF_5 = '4  of  5'
    _5_OF_5 = '5  of  5'

class Sigs_TargetlevelEnum(enum.Enum):
    LB_TO_UB = 'LB to UB'
    LB_AT_LEAST_ = 'LB+ (at least)'
    UB_TO_AT_MOST_ = 'UB- (at most)'

class Sigs_TargetleveltypeEnum(enum.Enum):
    PEAK = 'peak'
    TROUGH = 'trough'

class Sigs_TargetlevelunitEnum(enum.Enum):
    MCG_L = 'mcg/L'
    MG_L = 'mg/L'

class Studies_EndEnum(enum.Enum):
    _BLANK_ = '(blank)'
    YYYY = 'YYYY'
    YYYY_TO_MM_TO_DD = 'YYYY-MM-DD'
    ONGOING = 'ongoing'
    NR = 'NR'

class Studies_EnrollmentEnum(enum.Enum):
    START_OF_ENROLLMENT_TO_END_OF_ENROLLMENT = 'Start of enrollment to end of enrollment'
    EITHER_BOUND_CAN_ALSO_BE_NOT_REPORTED_ = 'either bound can also be "not reported"'
    NOT_REPORTED = 'Not reported'

class Studies_RegistryEnum(enum.Enum):
    CLINICALTRIALS_GOV = 'ClinicalTrials.gov'
    ISRCTN = 'ISRCTN'
    EUDRACT = 'EudraCT'
    UMIN_INCOMPLETE_LIST_ = 'UMIN (incomplete list)'

class Studies_Sponsor_typeEnum(enum.Enum):
    ACADEMIC_MEDICAL_CENTER = 'Academic medical center'
    ACADEMIC_CONSORTIUM = 'Academic consortium'
    COMMUNITY_PRACTICE = 'Community practice'
    COOPERATIVE_GROUP = 'Cooperative Group'
    GOVERNMENT = 'Government'
    PHARMACEUTICAL_INDUSTRY = 'Pharmaceutical industry'
    _BLANK_ = '(blank)'

class Studies_StartEnum(enum.Enum):
    _BLANK_ = '(blank)'
    YYYY = 'YYYY'
    YYYY_TO_MM_TO_DD = 'YYYY-MM-DD'
    NR = 'NR'

class Studies_Study_designEnum(enum.Enum):
    NON_TO_RANDOMIZED = 'Non-randomized'
    DE_TO_ESCALATION = 'De-escalation'
    ESCALATION = 'Escalation'
    IN_TO_CLASS_SWITCH = 'In-class switch'
    OUT_TO_OF_TO_CLASS_SWITCH = 'Out-of-class switch'
    MIXED = 'Mixed'
    CBD = 'CBD'

class StudyResults_Arm_typeEnum(enum.Enum):
    _BLANK_ = '(blank)'
    CONTROL = 'Control'
    DE_TO_ESCALATION = 'De-escalation'
    ESCALATION = 'Escalation'
    IN_TO_CLASS_SWITCH = 'In-class switch'
    OUT_TO_OF_TO_CLASS_SWITCH = 'Out-of-class switch'

class StudyResults_Endpoint_classEnum(enum.Enum):
    EVENT_AT_FIXED_TIME = 'event at fixed time'
    RATE = 'rate'
    RATE_AT_FIXED_TIME = 'rate at fixed time'
    TIME_TO_TO_TO_EVENT = 'time-to-event'
    TIME_TO_TO_TO_MEDIAN_EVENT = 'time-to-median event'
    OTHER = 'other'
    COULD_NOT_BE_DETERMINED = 'could not be determined'
    _BLANK_ = '(blank)'

class StudyResults_Endpoint_typeEnum(enum.Enum):
    PRIMARY = 'Primary'
    SECONDARY = 'Secondary'
    CO_TO_PRIMARY = 'Co-primary'
    UNDESIGNATED = 'Undesignated'
    _BLANK_ = '(blank)'

class StudyResults_EstciEnum(enum.Enum):
    XX_XX_ = 'XX.XX%'
    NOT_APPLICABLE_FOR_NON_TO_RANDOMIZED_STUDIES_ = 'Not applicable (for non-randomized studies)'

class StudyResults_EstimateEnum(enum.Enum):
    _1_23 = '1.23'
    NOT_APPLICABLE_FOR_NON_TO_RANDOMIZED_STUDIES_ = 'Not applicable (for non-randomized studies)'

class StudyResults_EstlbEnum(enum.Enum):
    _1_23 = '1.23'
    NOT_APPLICABLE_FOR_NON_TO_RANDOMIZED_STUDIES_ = 'Not applicable (for non-randomized studies)'

class StudyResults_EstubEnum(enum.Enum):
    _1_23 = '1.23'
    NOT_APPLICABLE_FOR_NON_TO_RANDOMIZED_STUDIES_ = 'Not applicable (for non-randomized studies)'

class StudyResults_MetricnumthatarmEnum(enum.Enum):
    _1_23_OR_1_23_ = '1.23 or 1.23%'
    NOT_APPLICABLE_FOR_NON_TO_RANDOMIZED_STUDIES_ = 'Not applicable (for non-randomized studies)'

class StudyResults_MetricunitEnum(enum.Enum):
    DAYS = 'days'
    WEEKS = 'weeks'
    MONTHS = 'months'
    YEARS = 'years'
    TIMED_RATE = 'timed rate'
    UNTIMED_RATE = 'untimed rate'
    _BLANK_ = '(blank)'

class StudyResults_StatisticEnum(enum.Enum):
    HR = 'HR'
    SHR = 'sHR'
    AHR = 'aHR'
    RR = 'RR'
    OR = 'OR'
    _BLANK_ = '(blank)'
    NOT_APPLICABLE_FOR_NON_TO_RANDOMIZED_STUDIES_ = 'Not applicable (for non-randomized studies)'

class Units_Unit_typeEnum(enum.Enum):
    UNITS_PER_VOLUME = 'units per volume'
    CALCULATED_DOSE = 'calculated dose'
    TIME = 'time'
    UNITS_PER_WEIGHT = 'units per weight'
    RADIATION_UNITS = 'radiation units'
    UNITLESS_QUANTITY = 'unitless quantity'
    UNITLESS_QUANTITY_PER_WEIGHT = 'unitless quantity per weight'
    UNITLESS_QUANTITY_PER_BSA = 'unitless quantity per BSA'
    WEIGHT = 'weight'
    WEIGHT_PER_SURFACE_AREA_USED_IN_BMI_ = 'weight per surface area (used in BMI)'
    BSA_BODY_SURFACE_AREA_ = 'BSA (body surface area)'
    UNITS_PER_TIME = 'units per time'
    WEIGHT_PER_VOLUME = 'weight per volume'
    UNITS_PER_BSA = 'units per BSA'
    UNITS_PER_BSA_PER_TIME = 'units per BSA per time'
    UNITS_PER_WEIGHT_PER_TIME = 'units per weight per time'
    WEIGHT_PER_VOLUME_USED_IN_CERTAIN_LABORATORY_TESTS_E_G_CREATININE = 'weight per volume used in certain laboratory tests, e.g., creatinine'
    CREATININE_CLEARANCE = 'creatinine clearance'
    UNITLESS_QUANTITY_PER_BSA_PER_TIME = 'unitless quantity per BSA per time'

class VariantBlob_BlockEnum(enum.Enum):
    HEADER = 'header'
    BODY_TOP = 'body.top'
    BODY = 'body'
    BODY_BOTTOM = 'body.bottom'

class VariantBlob_Chunk_typeEnum(enum.Enum):
    STRING = 'string'
    NUMERIC = 'numeric'
    CUI = 'CUI'


class Affiliations(Base):
    __tablename__ = 'affiliations'
    filename = 'affiliations.csv'

    aff_no: Mapped[Optional[int]] = mapped_column(Integer)
    affiliation_europmc: Mapped[Optional[str]] = mapped_column(Text)
    affiliation_hemonc: Mapped[Optional[str]] = mapped_column(Text)
    affiliation_journal: Mapped[Optional[str]] = mapped_column(Text)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    fullname_europmc: Mapped[Optional[str]] = mapped_column(String)
    fullname_hemonc: Mapped[Optional[str]] = mapped_column(String)
    person_cui: Mapped[Optional[int]] = mapped_column(Integer)
    pmid: Mapped[Optional[int]] = mapped_column(Integer)
    sequence: Mapped[Optional[int]] = mapped_column(Integer)

class Authors(Base):
    __tablename__ = 'authors'
    filename = 'authors.csv'

    aff_no: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    city: Mapped[Optional[str]] = mapped_column(String)
    country: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    department: Mapped[Optional[str]] = mapped_column(String)
    flag: Mapped[Optional[str]] = mapped_column(String)
    forename: Mapped[Optional[str]] = mapped_column(String)
    fullname_europmc: Mapped[Optional[str]] = mapped_column(String)
    imputed: Mapped[Optional[bool]] = mapped_column(Boolean)
    initials: Mapped[Optional[str]] = mapped_column(String)
    lastname: Mapped[Optional[str]] = mapped_column(String)
    nat: Mapped[Optional[str]] = mapped_column(String)
    orcid: Mapped[Optional[str]] = mapped_column(String)
    person_cui: Mapped[Optional[int]] = mapped_column(Integer)
    pmid: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    region: Mapped[Optional[str]] = mapped_column(String)
    role: Mapped[Optional[Authors_RoleEnum]] = mapped_column(Enum(Authors_RoleEnum))
    sequence: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    site: Mapped[Optional[str]] = mapped_column(String)
    site_type: Mapped[Optional[Authors_Site_typeEnum]] = mapped_column(Enum(Authors_Site_typeEnum))
    suffix: Mapped[Optional[str]] = mapped_column(String)
    tforename: Mapped[Optional[str]] = mapped_column(String)
    tfullname: Mapped[Optional[str]] = mapped_column(String)
    tlastname: Mapped[Optional[str]] = mapped_column(String)

class CanonicalTriples(Base):
    __tablename__ = 'canonicaltriples'
    filename = 'canonical.triples.csv'

    class_1: Mapped[Optional[CanonicalTriples_Class_1Enum]] = mapped_column(Enum(CanonicalTriples_Class_1Enum))
    class_1_provenance: Mapped[Optional[str]] = mapped_column(String)
    class_2: Mapped[Optional[str]] = mapped_column(String)
    class_2_provenance: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[str]] = mapped_column(String)
    date_deprecated: Mapped[Optional[str]] = mapped_column(String)
    index: Mapped[Optional[str]] = mapped_column(String)
    internal: Mapped[Optional[bool]] = mapped_column(Boolean)
    relationship: Mapped[Optional[str]] = mapped_column(String)
    used_in: Mapped[Optional[str]] = mapped_column(String)

class ChangeLog(Base):
    __tablename__ = 'changelog'
    filename = 'change.log.csv'


class Cities(Base):
    __tablename__ = 'cities'
    filename = 'cities.csv'


class ConceptRelationshipStage(Base):
    __tablename__ = 'concept_relationship_stage'
    filename = 'concept_relationship_stage.csv'


class ConceptStage(Base):
    __tablename__ = 'concept_stage'
    filename = 'concept_stage.csv'


class ConceptSynonymStage(Base):
    __tablename__ = 'concept_synonym_stage'
    filename = 'concept_synonym_stage.csv'


class Conditions(Base):
    __tablename__ = 'conditions'
    filename = 'conditions.csv'

    age_focus: Mapped[Optional[Conditions_Age_focusEnum]] = mapped_column(Enum(Conditions_Age_focusEnum))
    condition: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    condition_cui: Mapped[Optional[str]] = mapped_column(String)
    condition_type: Mapped[Optional[Conditions_Condition_typeEnum]] = mapped_column(Enum(Conditions_Condition_typeEnum))
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    map_icd10cm: Mapped[Optional[str]] = mapped_column(String)
    map_icd9cm: Mapped[Optional[str]] = mapped_column(String)
    map_icdo3: Mapped[Optional[str]] = mapped_column(String)
    map_icdo3_morph: Mapped[Optional[str]] = mapped_column(String)
    map_ncit: Mapped[Optional[str]] = mapped_column(String)
    map_oncotree: Mapped[Optional[str]] = mapped_column(String)
    map_type_icd10cm: Mapped[Optional[Conditions_Map_type_icd10cmEnum]] = mapped_column(Enum(Conditions_Map_type_icd10cmEnum))
    map_type_icd9cm: Mapped[Optional[Conditions_Map_type_icd9cmEnum]] = mapped_column(Enum(Conditions_Map_type_icd9cmEnum))
    map_type_icdo3: Mapped[Optional[Conditions_Map_type_icdo3Enum]] = mapped_column(Enum(Conditions_Map_type_icdo3Enum))
    map_type_icdo3_morph: Mapped[Optional[Conditions_Map_type_icdo3_morphEnum]] = mapped_column(Enum(Conditions_Map_type_icdo3_morphEnum))
    map_type_ncit: Mapped[Optional[Conditions_Map_type_ncitEnum]] = mapped_column(Enum(Conditions_Map_type_ncitEnum))
    map_type_oncotree: Mapped[Optional[Conditions_Map_type_oncotreeEnum]] = mapped_column(Enum(Conditions_Map_type_oncotreeEnum))
    regimenscount: Mapped[Optional[int]] = mapped_column(Integer)
    section: Mapped[Optional[Conditions_SectionEnum]] = mapped_column(Enum(Conditions_SectionEnum))
    variantscount: Mapped[Optional[int]] = mapped_column(Integer)

class ContextTable(Base):
    __tablename__ = 'contexttable'
    filename = 'context.table.csv'

    contextpretty: Mapped[Optional[str]] = mapped_column(String)
    contextraw: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    intent: Mapped[Optional[ContextTable_IntentEnum]] = mapped_column(Enum(ContextTable_IntentEnum))
    phase: Mapped[Optional[ContextTable_PhaseEnum]] = mapped_column(Enum(ContextTable_PhaseEnum))
    phenotype: Mapped[Optional[str]] = mapped_column(String)
    prior_therapy: Mapped[Optional[str]] = mapped_column(String)
    prior_therapy_negation: Mapped[Optional[bool]] = mapped_column(Boolean)
    risk_stratification: Mapped[Optional[ContextTable_Risk_stratificationEnum]] = mapped_column(Enum(ContextTable_Risk_stratificationEnum))
    setting: Mapped[Optional[str]] = mapped_column(String)
    stage_or_status: Mapped[Optional[str]] = mapped_column(String)
    therapy_type: Mapped[Optional[ContextTable_Therapy_typeEnum]] = mapped_column(Enum(ContextTable_Therapy_typeEnum))

class Drugs(Base):
    __tablename__ = 'drugs'
    filename = 'drugs.csv'

    atc: Mapped[Optional[str]] = mapped_column(String)
    canmed_major_class: Mapped[Optional[str]] = mapped_column(String)
    canmed_major_class_cui: Mapped[Optional[int]] = mapped_column(Integer)
    canmed_minor_class: Mapped[Optional[str]] = mapped_column(String)
    canmed_minor_class_cui: Mapped[Optional[int]] = mapped_column(Integer)
    class_type: Mapped[Optional[Drugs_Class_typeEnum]] = mapped_column(Enum(Drugs_Class_typeEnum))
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    drug: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    drug_cui: Mapped[Optional[int]] = mapped_column(Integer)
    drug_inn: Mapped[Optional[str]] = mapped_column(String)
    investigational: Mapped[Optional[bool]] = mapped_column(Boolean)
    main_class: Mapped[Optional[str]] = mapped_column(String)
    multiagent: Mapped[Optional[bool]] = mapped_column(Boolean)

class Exclusions(Base):
    __tablename__ = 'exclusions'
    filename = 'exclusions.csv'

    date_added: Mapped[Optional[str]] = mapped_column(String)
    pmid: Mapped[Optional[str]] = mapped_column(String)
    reason: Mapped[Optional[str]] = mapped_column(String)
    rev1: Mapped[Optional[Exclusions_Rev1Enum]] = mapped_column(Enum(Exclusions_Rev1Enum))
    rev2: Mapped[Optional[str]] = mapped_column(String)
    rev3: Mapped[Optional[float]] = mapped_column(Float)
    title: Mapped[Optional[str]] = mapped_column(Text)
    year: Mapped[Optional[datetime]] = mapped_column(DateTime)

class H4Types(Base):
    __tablename__ = 'h4types'
    filename = 'h4.types.csv'


class HemoncClasses(Base):
    __tablename__ = 'hemonc_classes'
    filename = 'hemonc_classes.csv'

    class_type: Mapped[Optional[HemoncClasses_Class_typeEnum]] = mapped_column(Enum(HemoncClasses_Class_typeEnum))
    concept_class_id: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[str]] = mapped_column(String)
    date_deprecated: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String)
    omopdomain_id: Mapped[Optional[HemoncClasses_Omopdomain_idEnum]] = mapped_column(Enum(HemoncClasses_Omopdomain_idEnum))
    omopstandard_concept: Mapped[Optional[HemoncClasses_Omopstandard_conceptEnum]] = mapped_column(Enum(HemoncClasses_Omopstandard_conceptEnum))
    primary_field: Mapped[Optional[str]] = mapped_column(String)
    primary_table: Mapped[Optional[str]] = mapped_column(String)
    secondary_home_as_cui: Mapped[Optional[str]] = mapped_column(String)
    secondary_home_as_string: Mapped[Optional[str]] = mapped_column(Text)

class HemoncRels(Base):
    __tablename__ = 'hemonc_rels'
    filename = 'hemonc_rels.csv'

    date_added: Mapped[Optional[str]] = mapped_column(String)
    date_deprecated: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String)
    heritable: Mapped[Optional[bool]] = mapped_column(Boolean)
    relationship_id: Mapped[Optional[str]] = mapped_column(String)

class Inclusions(Base):
    __tablename__ = 'inclusions'
    filename = 'inclusions.csv'

    date_added: Mapped[Optional[str]] = mapped_column(String)
    pmid: Mapped[Optional[int]] = mapped_column(Integer)
    reason: Mapped[Optional[Inclusions_ReasonEnum]] = mapped_column(Enum(Inclusions_ReasonEnum))
    reason_note: Mapped[Optional[str]] = mapped_column(Text)
    ref_type: Mapped[Optional[Inclusions_Ref_typeEnum]] = mapped_column(Enum(Inclusions_Ref_typeEnum))

class Indications(Base):
    __tablename__ = 'indications'
    filename = 'indications.csv'

    accelerated: Mapped[Optional[bool]] = mapped_column(Boolean)
    age: Mapped[Optional[str]] = mapped_column(String)
    age_unit: Mapped[Optional[Indications_Age_unitEnum]] = mapped_column(Enum(Indications_Age_unitEnum))
    biomarker: Mapped[Optional[str]] = mapped_column(String)
    biomarker2: Mapped[Optional[Indications_Biomarker2Enum]] = mapped_column(Enum(Indications_Biomarker2Enum))
    biomarker2_finding: Mapped[Optional[Indications_Biomarker2_findingEnum]] = mapped_column(Enum(Indications_Biomarker2_findingEnum))
    biomarker2_type: Mapped[Optional[Indications_Biomarker2_typeEnum]] = mapped_column(Enum(Indications_Biomarker2_typeEnum))
    biomarker3: Mapped[Optional[str]] = mapped_column(String)
    biomarker3_finding: Mapped[Optional[Indications_Biomarker3_findingEnum]] = mapped_column(Enum(Indications_Biomarker3_findingEnum))
    biomarker3_type: Mapped[Optional[Indications_Biomarker3_typeEnum]] = mapped_column(Enum(Indications_Biomarker3_typeEnum))
    biomarker4: Mapped[Optional[Indications_Biomarker4Enum]] = mapped_column(Enum(Indications_Biomarker4Enum))
    biomarker4_finding: Mapped[Optional[Indications_Biomarker4_findingEnum]] = mapped_column(Enum(Indications_Biomarker4_findingEnum))
    biomarker4_type: Mapped[Optional[Indications_Biomarker4_typeEnum]] = mapped_column(Enum(Indications_Biomarker4_typeEnum))
    biomarker_finding: Mapped[Optional[Indications_Biomarker_findingEnum]] = mapped_column(Enum(Indications_Biomarker_findingEnum))
    biomarker_type: Mapped[Optional[Indications_Biomarker_typeEnum]] = mapped_column(Enum(Indications_Biomarker_typeEnum))
    component: Mapped[Optional[str]] = mapped_column(String)
    component_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    condition: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    context: Mapped[Optional[str]] = mapped_column(String)
    date: Mapped[Optional[Indications_DateEnum]] = mapped_column(Enum(Indications_DateEnum))
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    demographics: Mapped[Optional[str]] = mapped_column(String)
    first_in_class: Mapped[Optional[bool]] = mapped_column(Boolean)
    ineligibility: Mapped[Optional[str]] = mapped_column(String)
    nat: Mapped[Optional[str]] = mapped_column(String)
    note: Mapped[Optional[Indications_NoteEnum]] = mapped_column(Enum(Indications_NoteEnum))
    prior_biomarker: Mapped[Optional[str]] = mapped_column(String)
    prior_therapy: Mapped[Optional[str]] = mapped_column(String)
    prior_therapy_negation: Mapped[Optional[bool]] = mapped_column(Boolean)
    prior_therapy_setting: Mapped[Optional[str]] = mapped_column(String)
    regimen: Mapped[Optional[str]] = mapped_column(String)
    regimen_cui: Mapped[Optional[str]] = mapped_column(String)
    regulator: Mapped[Optional[Indications_RegulatorEnum]] = mapped_column(Enum(Indications_RegulatorEnum), primary_key=True)
    response_contingency: Mapped[Optional[str]] = mapped_column(String)
    risk_stratification: Mapped[Optional[str]] = mapped_column(String)
    sex: Mapped[Optional[Indications_SexEnum]] = mapped_column(Enum(Indications_SexEnum))
    stage_or_status: Mapped[Optional[str]] = mapped_column(String)
    string: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    study: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    study_cui: Mapped[Optional[str]] = mapped_column(String)
    study_yn: Mapped[Optional[bool]] = mapped_column(Boolean)
    time_contingency: Mapped[Optional[str]] = mapped_column(String)
    with_field: Mapped[Optional[str]] = mapped_column(String)
    withdrawn: Mapped[Optional[Indications_WithdrawnEnum]] = mapped_column(Enum(Indications_WithdrawnEnum))

class PageLookup(Base):
    __tablename__ = 'pagelookup'
    filename = 'page.lookup.csv'


class PageTable(Base):
    __tablename__ = 'pagetable'
    filename = 'page.table.csv'


class Persons(Base):
    __tablename__ = 'persons'
    filename = 'persons.csv'

    co_authors: Mapped[Optional[int]] = mapped_column(Integer)
    co_authorships: Mapped[Optional[int]] = mapped_column(Integer)
    condition_types: Mapped[Optional[str]] = mapped_column(String)
    conditions: Mapped[Optional[str]] = mapped_column(String)
    country: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    first_active_year: Mapped[Optional[datetime]] = mapped_column(DateTime)
    gender: Mapped[Optional[Persons_GenderEnum]] = mapped_column(Enum(Persons_GenderEnum))
    guideline_pubs: Mapped[Optional[int]] = mapped_column(Integer)
    hyphen_type: Mapped[Optional[Persons_Hyphen_typeEnum]] = mapped_column(Enum(Persons_Hyphen_typeEnum))
    last_active_year: Mapped[Optional[datetime]] = mapped_column(DateTime)
    location: Mapped[Optional[str]] = mapped_column(String)
    multi_site: Mapped[Optional[bool]] = mapped_column(Boolean)
    name: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    nat: Mapped[Optional[str]] = mapped_column(String)
    orcid: Mapped[Optional[str]] = mapped_column(String)
    person_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    ph3_studies: Mapped[Optional[int]] = mapped_column(Integer)
    pivotal_studies: Mapped[Optional[int]] = mapped_column(Integer)
    senior_pubs: Mapped[Optional[int]] = mapped_column(Integer)
    site: Mapped[Optional[str]] = mapped_column(String)
    study_groups: Mapped[Optional[str]] = mapped_column(String)
    study_sponsors: Mapped[Optional[str]] = mapped_column(String)
    vital_status: Mapped[Optional[Persons_Vital_statusEnum]] = mapped_column(Enum(Persons_Vital_statusEnum))

class Pointers(Base):
    __tablename__ = 'pointers'
    filename = 'pointers.csv'

    biomarker: Mapped[Optional[str]] = mapped_column(String)
    condition: Mapped[Optional[str]] = mapped_column(String)
    context: Mapped[Optional[str]] = mapped_column(String)
    h2_html: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    h3_html: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    regimen: Mapped[Optional[str]] = mapped_column(String)
    regimen_cui: Mapped[Optional[str]] = mapped_column(String)
    tracer: Mapped[Optional[str]] = mapped_column(String)
    version: Mapped[Optional[datetime]] = mapped_column(DateTime, primary_key=True)

class Protocols(Base):
    __tablename__ = 'protocols'
    filename = 'protocols.csv'


class RctDesign(Base):
    __tablename__ = 'rct_design'
    filename = 'rct_design.csv'


class Refs(Base):
    __tablename__ = 'refs'
    filename = 'refs.csv'

    biblio: Mapped[Optional[Refs_BiblioEnum]] = mapped_column(Enum(Refs_BiblioEnum))
    biomarker: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    condition: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    doi: Mapped[Optional[str]] = mapped_column(String)
    journal: Mapped[Optional[str]] = mapped_column(String)
    pmcid: Mapped[Optional[str]] = mapped_column(String)
    pmid: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    pubdate: Mapped[Optional[datetime]] = mapped_column(DateTime)
    ref_type: Mapped[Optional[Refs_Ref_typeEnum]] = mapped_column(Enum(Refs_Ref_typeEnum))
    reference: Mapped[Optional[str]] = mapped_column(String)
    study: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String)
    url: Mapped[Optional[str]] = mapped_column(String)

class RxnormMap(Base):
    __tablename__ = 'rxnorm_map'
    filename = 'rxnorm_map.csv'


class SequenceTable(Base):
    __tablename__ = 'sequencetable'
    filename = 'sequence.table.csv'


class SigBranchTypes(Base):
    __tablename__ = 'sig_branch_types'
    filename = 'sig_branch_types.csv'

    description: Mapped[Optional[str]] = mapped_column(String)
    value: Mapped[Optional[str]] = mapped_column(String)

class Sigs(Base):
    __tablename__ = 'sigs'
    filename = 'sigs.csv'

    alldays: Mapped[Optional[Sigs_AlldaysEnum]] = mapped_column(Enum(Sigs_AlldaysEnum))
    branch: Mapped[Optional[str]] = mapped_column(String)
    branch_type: Mapped[Optional[str]] = mapped_column(String)
    class_field: Mapped[Optional[Sigs_Class_fieldEnum]] = mapped_column(Enum(Sigs_Class_fieldEnum))
    component: Mapped[Optional[str]] = mapped_column(String)
    component_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    component_role: Mapped[Optional[Sigs_Component_roleEnum]] = mapped_column(Enum(Sigs_Component_roleEnum))
    cycle_length_lb: Mapped[Optional[str]] = mapped_column(String)
    cycle_length_ub: Mapped[Optional[Sigs_Cycle_length_ubEnum]] = mapped_column(Enum(Sigs_Cycle_length_ubEnum))
    cycle_length_unit: Mapped[Optional[Sigs_Cycle_length_unitEnum]] = mapped_column(Enum(Sigs_Cycle_length_unitEnum))
    cyclesigs: Mapped[Optional[str]] = mapped_column(String)
    cyclesigs_note: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    divided: Mapped[Optional[bool]] = mapped_column(Boolean)
    dosecapnum: Mapped[Optional[str]] = mapped_column(String)
    dosecapunit: Mapped[Optional[Sigs_DosecapunitEnum]] = mapped_column(Enum(Sigs_DosecapunitEnum))
    dosecapunit_cui: Mapped[Optional[str]] = mapped_column(String)
    dosemaxnum: Mapped[Optional[str]] = mapped_column(String)
    doseminnum: Mapped[Optional[str]] = mapped_column(String)
    doseunit: Mapped[Optional[Sigs_DoseunitEnum]] = mapped_column(Enum(Sigs_DoseunitEnum))
    doseunit_cui: Mapped[Optional[str]] = mapped_column(String)
    durationmaxnum: Mapped[Optional[Sigs_DurationmaxnumEnum]] = mapped_column(Enum(Sigs_DurationmaxnumEnum))
    durationminnum: Mapped[Optional[Sigs_DurationminnumEnum]] = mapped_column(Enum(Sigs_DurationminnumEnum))
    durationunit: Mapped[Optional[Sigs_DurationunitEnum]] = mapped_column(Enum(Sigs_DurationunitEnum))
    durationunit_cui: Mapped[Optional[str]] = mapped_column(String)
    frequency: Mapped[Optional[Sigs_FrequencyEnum]] = mapped_column(Enum(Sigs_FrequencyEnum))
    frequency_cui: Mapped[Optional[str]] = mapped_column(String)
    inparens: Mapped[Optional[str]] = mapped_column(String)
    nat: Mapped[Optional[str]] = mapped_column(String)
    phase: Mapped[Optional[Sigs_PhaseEnum]] = mapped_column(Enum(Sigs_PhaseEnum), primary_key=True)
    portion: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    regimen: Mapped[Optional[str]] = mapped_column(String)
    regimen_cui: Mapped[Optional[str]] = mapped_column(String)
    route: Mapped[Optional[Sigs_RouteEnum]] = mapped_column(Enum(Sigs_RouteEnum))
    route_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    seqrel: Mapped[Optional[str]] = mapped_column(String)
    seqrelwhat: Mapped[Optional[str]] = mapped_column(String)
    seqrelwhen: Mapped[Optional[str]] = mapped_column(String)
    seqrelwhenunit: Mapped[Optional[Sigs_SeqrelwhenunitEnum]] = mapped_column(Enum(Sigs_SeqrelwhenunitEnum))
    sequence: Mapped[Optional[str]] = mapped_column(String)
    step_number: Mapped[Optional[Sigs_Step_numberEnum]] = mapped_column(Enum(Sigs_Step_numberEnum), primary_key=True)
    study: Mapped[Optional[str]] = mapped_column(String)
    tail: Mapped[Optional[str]] = mapped_column(String)
    targetlevel: Mapped[Optional[Sigs_TargetlevelEnum]] = mapped_column(Enum(Sigs_TargetlevelEnum))
    targetleveltype: Mapped[Optional[Sigs_TargetleveltypeEnum]] = mapped_column(Enum(Sigs_TargetleveltypeEnum))
    targetlevelunit: Mapped[Optional[Sigs_TargetlevelunitEnum]] = mapped_column(Enum(Sigs_TargetlevelunitEnum))
    targetlevelunit_cui: Mapped[Optional[str]] = mapped_column(String)
    timing: Mapped[Optional[str]] = mapped_column(String)
    timing_sequence: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    variant: Mapped[Optional[str]] = mapped_column(String)
    variant_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)

class Sites(Base):
    __tablename__ = 'sites'
    filename = 'sites.csv'


class Studies(Base):
    __tablename__ = 'studies'
    filename = 'studies.csv'

    biomarker: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    condition: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    condition_cui: Mapped[Optional[str]] = mapped_column(String)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end: Mapped[Optional[Studies_EndEnum]] = mapped_column(Enum(Studies_EndEnum))
    enrollment: Mapped[Optional[Studies_EnrollmentEnum]] = mapped_column(Enum(Studies_EnrollmentEnum))
    phase: Mapped[Optional[str]] = mapped_column(String)
    protocol: Mapped[Optional[bool]] = mapped_column(Boolean)
    pubs_in_hemonc: Mapped[Optional[int]] = mapped_column(Integer)
    reg_study: Mapped[Optional[bool]] = mapped_column(Boolean)
    registry: Mapped[Optional[Studies_RegistryEnum]] = mapped_column(Enum(Studies_RegistryEnum))
    sact: Mapped[Optional[bool]] = mapped_column(Boolean)
    sponsor: Mapped[Optional[str]] = mapped_column(String)
    sponsor_type: Mapped[Optional[Studies_Sponsor_typeEnum]] = mapped_column(Enum(Studies_Sponsor_typeEnum))
    start: Mapped[Optional[Studies_StartEnum]] = mapped_column(Enum(Studies_StartEnum))
    study: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    study_design: Mapped[Optional[Studies_Study_designEnum]] = mapped_column(Enum(Studies_Study_designEnum))
    study_design_imputed: Mapped[Optional[bool]] = mapped_column(Boolean)
    study_group: Mapped[Optional[str]] = mapped_column(String)
    trial_id: Mapped[Optional[str]] = mapped_column(String)
    unreg_study: Mapped[Optional[bool]] = mapped_column(Boolean)

class StudyDemographics(Base):
    __tablename__ = 'study_demographics'
    filename = 'study_demographics.csv'


class StudyEligibility(Base):
    __tablename__ = 'study_eligibility'
    filename = 'study_eligibility.csv'


class StudyResults(Base):
    __tablename__ = 'study_results'
    filename = 'study_results.csv'

    arm_type: Mapped[Optional[StudyResults_Arm_typeEnum]] = mapped_column(Enum(StudyResults_Arm_typeEnum))
    biomarker: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    c_modifier: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    comparator: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    comparator_code: Mapped[Optional[str]] = mapped_column(String)
    condition: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    condition_cui: Mapped[Optional[str]] = mapped_column(String)
    context: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    efficacy: Mapped[Optional[str]] = mapped_column(String)
    endpoint: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    endpoint_class: Mapped[Optional[StudyResults_Endpoint_classEnum]] = mapped_column(Enum(StudyResults_Endpoint_classEnum))
    endpoint_type: Mapped[Optional[StudyResults_Endpoint_typeEnum]] = mapped_column(Enum(StudyResults_Endpoint_typeEnum))
    error: Mapped[Optional[bool]] = mapped_column(Boolean)
    estci: Mapped[Optional[StudyResults_EstciEnum]] = mapped_column(Enum(StudyResults_EstciEnum))
    estimate: Mapped[Optional[StudyResults_EstimateEnum]] = mapped_column(Enum(StudyResults_EstimateEnum))
    estlb: Mapped[Optional[StudyResults_EstlbEnum]] = mapped_column(Enum(StudyResults_EstlbEnum))
    estub: Mapped[Optional[StudyResults_EstubEnum]] = mapped_column(Enum(StudyResults_EstubEnum))
    metric: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    metric_version: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    metricnumthatarm: Mapped[Optional[StudyResults_MetricnumthatarmEnum]] = mapped_column(Enum(StudyResults_MetricnumthatarmEnum))
    metricnumthisarm: Mapped[Optional[str]] = mapped_column(String)
    metricunit: Mapped[Optional[StudyResults_MetricunitEnum]] = mapped_column(Enum(StudyResults_MetricunitEnum))
    r_modifier: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    regimen: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    statistic: Mapped[Optional[StudyResults_StatisticEnum]] = mapped_column(Enum(StudyResults_StatisticEnum))
    study: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    toxicity: Mapped[Optional[str]] = mapped_column(String)

class Units(Base):
    __tablename__ = 'units'
    filename = 'units.csv'

    concept_code: Mapped[Optional[datetime]] = mapped_column(DateTime)
    date_added: Mapped[Optional[str]] = mapped_column(String)
    unit: Mapped[Optional[str]] = mapped_column(String)
    unit_type: Mapped[Optional[Units_Unit_typeEnum]] = mapped_column(Enum(Units_Unit_typeEnum))

class VariantEligibility(Base):
    __tablename__ = 'variant_eligibility'
    filename = 'variant_eligibility.csv'

    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    logic: Mapped[Optional[bool]] = mapped_column(Boolean)
    logic_count: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    regimen: Mapped[Optional[str]] = mapped_column(String)
    regimen_cui: Mapped[Optional[str]] = mapped_column(String)
    string: Mapped[Optional[str]] = mapped_column(String)
    study: Mapped[Optional[str]] = mapped_column(String)
    type: Mapped[Optional[str]] = mapped_column(String)
    unit: Mapped[Optional[str]] = mapped_column(String)
    unit_cui: Mapped[Optional[str]] = mapped_column(String)
    variant_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)

class VariantBlob(Base):
    __tablename__ = 'variantblob'
    filename = 'variant.blob.csv'

    block: Mapped[Optional[VariantBlob_BlockEnum]] = mapped_column(Enum(VariantBlob_BlockEnum))
    chunk: Mapped[Optional[str]] = mapped_column(String)
    chunk_type: Mapped[Optional[VariantBlob_Chunk_typeEnum]] = mapped_column(Enum(VariantBlob_Chunk_typeEnum))
    date_created: Mapped[Optional[str]] = mapped_column(String)
    date_retired: Mapped[Optional[str]] = mapped_column(String)
    order: Mapped[Optional[int]] = mapped_column(Integer)
    version: Mapped[Optional[int]] = mapped_column(Integer)

class Variants(Base):
    __tablename__ = 'variants'
    filename = 'variants.csv'

    allsigshavecyclesigs: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshavedose: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshavedoseunit: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshaveduration: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshavedurationunit: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshavefrequency: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshaveroute: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshaveschedule: Mapped[Optional[bool]] = mapped_column(Boolean)
    allsigshavesequence: Mapped[Optional[bool]] = mapped_column(Boolean)
    blob: Mapped[Optional[str]] = mapped_column(String)
    blob_version: Mapped[Optional[int]] = mapped_column(Integer)
    branches: Mapped[Optional[int]] = mapped_column(Integer)
    components: Mapped[Optional[int]] = mapped_column(Integer)
    cyclesigs: Mapped[Optional[int]] = mapped_column(Integer)
    date_added: Mapped[Optional[datetime]] = mapped_column(DateTime)
    date_study_modified: Mapped[Optional[datetime]] = mapped_column(DateTime)
    date_tracer_modified: Mapped[Optional[datetime]] = mapped_column(DateTime)
    fullyspecified: Mapped[Optional[bool]] = mapped_column(Boolean)
    portions: Mapped[Optional[int]] = mapped_column(Integer)
    regimen: Mapped[Optional[str]] = mapped_column(String)
    regimen_cui: Mapped[Optional[str]] = mapped_column(String)
    routes: Mapped[Optional[int]] = mapped_column(Integer)
    sigs: Mapped[Optional[int]] = mapped_column(Integer)
    study: Mapped[Optional[str]] = mapped_column(String)
    timings: Mapped[Optional[int]] = mapped_column(Integer)
    tracer: Mapped[Optional[str]] = mapped_column(String)
    variant: Mapped[Optional[str]] = mapped_column(String)
    variant_cui: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    version: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)


class Drugs_Canmed_major_class(Base):
    __tablename__ = 'drugs_canmed_major_class'
    canmed_major_class: Mapped[str] = mapped_column(String, primary_key=True)

class Drugs_Canmed_major_classMap(Base):
    __tablename__ = 'drugs_canmed_major_class_map'
    drug: Mapped[int] = mapped_column(
        ForeignKey('drugs.drug'), primary_key=True)
    canmed_major_class: Mapped[str] = mapped_column(
        ForeignKey('drugs_canmed_major_class.canmed_major_class'), primary_key=True)

class Drugs_Canmed_major_class_cui(Base):
    __tablename__ = 'drugs_canmed_major_class_cui'
    canmed_major_class_cui: Mapped[str] = mapped_column(String, primary_key=True)

class Drugs_Canmed_major_class_cuiMap(Base):
    __tablename__ = 'drugs_canmed_major_class_cui_map'
    drug: Mapped[int] = mapped_column(
        ForeignKey('drugs.drug'), primary_key=True)
    canmed_major_class_cui: Mapped[str] = mapped_column(
        ForeignKey('drugs_canmed_major_class_cui.canmed_major_class_cui'), primary_key=True)

class Drugs_Canmed_minor_class(Base):
    __tablename__ = 'drugs_canmed_minor_class'
    canmed_minor_class: Mapped[str] = mapped_column(String, primary_key=True)

class Drugs_Canmed_minor_classMap(Base):
    __tablename__ = 'drugs_canmed_minor_class_map'
    drug: Mapped[int] = mapped_column(
        ForeignKey('drugs.drug'), primary_key=True)
    canmed_minor_class: Mapped[str] = mapped_column(
        ForeignKey('drugs_canmed_minor_class.canmed_minor_class'), primary_key=True)

class Drugs_Canmed_minor_class_cui(Base):
    __tablename__ = 'drugs_canmed_minor_class_cui'
    canmed_minor_class_cui: Mapped[str] = mapped_column(String, primary_key=True)

class Drugs_Canmed_minor_class_cuiMap(Base):
    __tablename__ = 'drugs_canmed_minor_class_cui_map'
    drug: Mapped[int] = mapped_column(
        ForeignKey('drugs.drug'), primary_key=True)
    canmed_minor_class_cui: Mapped[str] = mapped_column(
        ForeignKey('drugs_canmed_minor_class_cui.canmed_minor_class_cui'), primary_key=True)

class Indications_Biomarker2(Base):
    __tablename__ = 'indications_biomarker2'
    biomarker2: Mapped[str] = mapped_column(String, primary_key=True)

class Indications_Biomarker2Map(Base):
    __tablename__ = 'indications_biomarker2_map'
    component_cui: Mapped[int] = mapped_column(
        ForeignKey('indications.component_cui'), primary_key=True)
    biomarker2: Mapped[str] = mapped_column(
        ForeignKey('indications_biomarker2.biomarker2'), primary_key=True)

class Indications_Biomarker2_finding(Base):
    __tablename__ = 'indications_biomarker2_finding'
    biomarker2_finding: Mapped[str] = mapped_column(String, primary_key=True)

class Indications_Biomarker2_findingMap(Base):
    __tablename__ = 'indications_biomarker2_finding_map'
    component_cui: Mapped[int] = mapped_column(
        ForeignKey('indications.component_cui'), primary_key=True)
    biomarker2_finding: Mapped[str] = mapped_column(
        ForeignKey('indications_biomarker2_finding.biomarker2_finding'), primary_key=True)

class Indications_Biomarker4(Base):
    __tablename__ = 'indications_biomarker4'
    biomarker4: Mapped[str] = mapped_column(String, primary_key=True)

class Indications_Biomarker4Map(Base):
    __tablename__ = 'indications_biomarker4_map'
    component_cui: Mapped[int] = mapped_column(
        ForeignKey('indications.component_cui'), primary_key=True)
    biomarker4: Mapped[str] = mapped_column(
        ForeignKey('indications_biomarker4.biomarker4'), primary_key=True)

class Indications_Biomarker4_finding(Base):
    __tablename__ = 'indications_biomarker4_finding'
    biomarker4_finding: Mapped[str] = mapped_column(String, primary_key=True)

class Indications_Biomarker4_findingMap(Base):
    __tablename__ = 'indications_biomarker4_finding_map'
    component_cui: Mapped[int] = mapped_column(
        ForeignKey('indications.component_cui'), primary_key=True)
    biomarker4_finding: Mapped[str] = mapped_column(
        ForeignKey('indications_biomarker4_finding.biomarker4_finding'), primary_key=True)
