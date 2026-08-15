from enum import Enum


class Authors_RoleEnum(str, Enum):
    FIRST_AUTHOR = 'first author'
    SECOND_AUTHOR = 'second author'
    MIDDLE_AUTHOR = 'middle author'
    LAST_AUTHOR = 'last author'
    CO_TO_FIRST_AUTHOR = 'co-first author'
    CO_TO_LAST_AUTHOR = 'co-last author'

class Authors_Site_typeEnum(str, Enum):
    NO_DATA = 'no data'
    TBD = 'tbd'
    ACADEMIC_MEDICAL_CENTER = 'academic medical center'
    NCI_TO_CCC = 'nci-ccc'
    GOVERNMENT = 'government'
    NCI_TO_CC = 'nci-cc'
    COOPERATIVE_GROUP = 'cooperative group'
    COMMUNITY_PRACTICE = 'community practice'
    PHARMACEUTICAL_INDUSTRY = 'pharmaceutical industry'

class Conditions_Condition_typeEnum(str, Enum):
    CLASSICAL_HEMATOLOGY = 'classical hematology'
    OTHER_HEMATOLOGIC_NEOPLASM = 'other hematologic neoplasm'
    LYMPHOID = 'lymphoid'
    MYELOID = 'myeloid'
    ENDOCRINE = 'endocrine'
    THORACIC = 'thoracic'
    OTHER = 'other'
    SARCOMA = 'sarcoma'
    GASTROINTESTINAL = 'gastrointestinal'
    CNS = 'cns'
    GENITOURINARY = 'genitourinary'
    OTHER_SOLID_NEOPLASM = 'other solid neoplasm'
    DERMATOLOGIC = 'dermatologic'
    BREAST = 'breast'
    GYNECOLOGIC = 'gynecologic'
    OTHER_NEOPLASM = 'other neoplasm'
    HEAD_NECK = 'head & neck'
    PLASMA_CELL = 'plasma cell'
    NET = 'net'

class Conditions_SectionEnum(str, Enum):
    ACUTE_LEUKEMIA = 'acute leukemia'
    AGGRESSIVE_LYMPHOMA = 'aggressive lymphoma'
    BREAST_ONCOLOGY = 'breast oncology'
    CYTOPENIAS = 'cytopenias'
    DERMATOLOGIC_ONCOLOGY = 'dermatologic oncology'
    DISEASE_TO_AGNOSTIC = 'disease-agnostic'
    ENDOCRINE_ONCOLOGY = 'endocrine oncology'
    GENITORURINARY_ONCOLOGY = 'genitorurinary oncology'
    GI_ONCOLOGY_EXTRAINTESTINAL = 'gi oncology, extraintestinal'
    GI_ONCOLOGY_INTESTINAL = 'gi oncology, intestinal'
    GYNECOLOGIC_ONCOLOGY = 'gynecologic oncology'
    HEAD_NECK_ONCOLOGY = 'head & neck oncology'
    HEMOGLOBINOPATHIES = 'hemoglobinopathies'
    HEMOLYTIC_DISORDERS = 'hemolytic disorders'
    HEMOSTASIS_AND_THROMBOSIS = 'hemostasis and thrombosis'
    HISTIOCYTE_DISORDERS = 'histiocyte disorders'
    INDOLENT_LYMPHOMA = 'indolent lymphoma'
    LYMPHOPROLIFERATIVE_DISORDERS = 'lymphoproliferative disorders'
    MESOTHELIOMA = 'mesothelioma'
    MYELOPROLIFERATIVE_NEOPLASMS_AND_MYELODYSPLASTIC_SYNDROMES = 'myeloproliferative neoplasms and myelodysplastic syndromes'
    NEURO_TO_ONCOLOGY = 'neuro-oncology'
    PEDIATRIC_CNS_MALIGNANCIES = 'pediatric cns malignancies'
    PEDIATRIC_HEMATOLOGIC_NEOPLASMS = 'pediatric hematologic neoplasms'
    PEDIATRIC_SOLID_TUMORS = 'pediatric solid tumors'
    PLASMA_CELL_DYSCRASIAS = 'plasma cell dyscrasias'
    SARCOMA = 'sarcoma'
    T_TO_CELL_AND_NK_TO_CELL_NEOPLASMS = 't-cell and nk-cell neoplasms'
    THORACIC_ONCOLOGY = 'thoracic oncology'
    TRANSPLANT_AND_IEC = 'transplant and iec'
    BLANK_NO_EDITORIAL_BOARD_MAPPING = 'blank (no editorial board mapping)'

class Conditions_Age_focusEnum(str, Enum):
    UNDEFINED = 'undefined'
    PEDIATRIC = 'pediatric'

class Conditions_Map_type_ncitEnum(str, Enum):
    EXACT = 'exact'
    UP = 'up'
    DOWN = 'down'

class Conditions_Map_type_oncotreeEnum(str, Enum):
    UP = 'up'
    EXACT = 'exact'
    DOWN = 'down'

class Conditions_Map_type_icd9cmEnum(str, Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_icd10cmEnum(str, Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_icdo3Enum(str, Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT = 'sideways (semantic equivalence but not exact)'

class Conditions_Map_type_icdo3_morphEnum(str, Enum):
    EXACT = 'exact'
    DOWN_LESS_TO_TO_TO_MORE_GRANULAR = 'down (less-to-more granular)'
    UP_MORE_TO_TO_TO_LESS_GRANULAR = 'up (more-to-less granular)'
    SIDEWAYS_SEMANTIC_EQUIVALENCE_BUT_NOT_EXACT = 'sideways (semantic equivalence but not exact)'

class Drugs_Class_typeEnum(str, Enum):
    MECHANISTIC = 'mechanistic'
    BIOCHEMICAL = 'biochemical'
    NONSPECIFIC = 'nonspecific'
    FUNCTIONAL = 'functional'

class Indications_RegulatorEnum(str, Enum):
    FDA = 'fda'
    PMDA = 'pmda'
    EMA = 'ema'
    HC = 'hc'
    NMPA = 'nmpa'
    MFDS = 'mfds'

class Indications_NoteEnum(str, Enum):
    NO_LINKED_CONDITION = 'no linked condition'
    NO_MONTH_YEAR_INFORMATION = 'no month/year information'
    TO_BE_DISSECTED = 'to be dissected'

class Indications_SexEnum(str, Enum):
    MEN = 'men'
    WOMEN = 'women'

class Indications_Age_unitEnum(str, Enum):
    UNSPECIFIED = 'unspecified'
    MONTH = 'month'
    YEAR = 'year'

class Indications_Biomarker_findingEnum(str, Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    MORE_TO_COME = '[more to come]'

class Indications_Biomarker_typeEnum(str, Enum):
    PROTEIN = 'protein'
    GENE = 'gene'
    CHROMOSOME = 'chromosome'
    TRACER = 'tracer'
    VIRUS = 'virus'

class Indications_Biomarker2_findingEnum(str, Enum):
    NEGATIVE = 'negative'
    POSITIVE = 'positive'
    WILD_TO_TYPE = 'wild-type'
    NEGATIVE_ICH_0_1HC1_OR_IHC2_ISH_TO = 'negative (ich 0, 1hc1+ or ihc2+/ish-)'
    CPS_AT_LEAST_5 = 'cps at least 5'
    CPS_AT_LEAST_1 = 'cps at least 1'
    LOW_IHC_1_OR_IHC_2_ISH_TO_OR_ULTRALOW_IHC_0_WITH_MEMBRANE_ST = 'low (ihc 1+ or ihc 2+/ish-) or ultralow (ihc 0 with membrane staining)'

class Indications_Biomarker2_typeEnum(str, Enum):
    PROTEIN = 'protein'
    GENE = 'gene'

class Indications_Biomarker3_findingEnum(str, Enum):
    MUTATION = 'mutation'
    NEGATIVE = 'negative'
    WILD_TO_TYPE = 'wild-type'
    ACTIVATING_MUTATION = 'activating mutation'

class Indications_Biomarker3_typeEnum(str, Enum):
    GENE = 'gene'
    PROTEIN = 'protein'

class Indications_Biomarker4_findingEnum(str, Enum):
    TIL_AT_LEAST_1 = 'til at least 1%'
    POSITIVE = 'positive'
    WILD_TO_TYPE = 'wild-type'
    CPS_AT_LEAST_10 = 'cps at least 10'

class Indications_Biomarker4_typeEnum(str, Enum):
    PROTEIN = 'protein'
    GENE = 'gene'

class Indications_Biomarker2Enum(str, Enum):
    HER2 = 'her2'
    MAGE_TO_A4_ANTIGEN = 'mage-a4 antigen'
    EGFR = 'egfr'
    PR = 'pr'
    ALK = 'alk'
    CD19 = 'cd19'
    KRAS = 'kras'
    PD_TO_L1 = 'pd-l1'
    CLDN18_2 = 'cldn18.2'

class Indications_Biomarker4Enum(str, Enum):
    PD_TO_L1 = 'pd-l1'
    ROS1 = 'ros1'

class Persons_Hyphen_typeEnum(str, Enum):
    EASTERN = 'eastern'
    WESTERN = 'western'
    MENA = 'mena'

class Persons_GenderEnum(str, Enum):
    MAN = 'man'
    NOT_YET_DETERMINED = 'not yet determined'
    WOMAN = 'woman'
    COULD_NOT_BE_DETERMINED = 'could not be determined'
    UNKNOWN = 'unknown'

class Persons_Vital_statusEnum(str, Enum):
    I_1_ALIVE_NOT_KNOWN_TO_BE_DECEASED = '1 = alive (not known to be deceased)'
    I_0_DECEASED_IF_YEAR_UNKNOWN = '0 = deceased (if year unknown)'
    YYYY_YEAR_DECEASED = 'yyyy = year deceased'

class Refs_Ref_typeEnum(str, Enum):
    PRIMARY = 'primary'
    UPDATE = 'update'
    GUIDELINE = 'guideline'
    POOLED_UPDATE = 'pooled update'
    HRQOL_ANALYSIS = 'hrqol analysis'
    SUBGROUP_ANALYSIS = 'subgroup analysis'
    POOLED_SUBGROUP_ANALYSIS = 'pooled subgroup analysis'
    PRO_ANALYSIS = 'pro analysis'
    BIOMARKER_ANALYSIS = 'biomarker analysis'
    Q_TO_TWIST_ANALYSIS = 'q-twist analysis'
    TWIST_ANALYSIS = 'twist analysis'
    SAFETY_ANALYSIS = 'safety analysis'

class Sigs_PhaseEnum(str, Enum):
    CONSOLIDATION = 'consolidation'
    CONTINUATION = 'continuation'
    DELAYED_INTENSIFICATION = 'delayed intensification'
    INDUCTION = 'induction'
    INTENSIFICATION = 'intensification'
    INTERIM_MAINTENANCE = 'interim maintenance'
    MAINTENANCE = 'maintenance'
    PRE_TO_PHASE = 'pre-phase'
    POST_TO_CONSOLIDATION = 'post-consolidation'
    LT_MORE_TO_BE_ADDEDGT = '<more to be added>'
    UNSPECIFIED_DEFAULT = 'unspecified (default)'

class Sigs_Component_roleEnum(str, Enum):
    PRIMARY_SYSTEMIC = 'primary systemic'
    SECONDARY_SYSTEMIC = 'secondary systemic'
    LOCOREGIONAL = 'locoregional'

class Sigs_Cycle_length_unitEnum(str, Enum):
    INDETERMINATE = 'indeterminate'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'

class Sigs_Step_numberEnum(str, Enum):
    I_1_OF_1_DEFAULT = '1  of  1 (default)'
    I_1_OF_2 = '1  of  2'
    I_1_OF_3 = '1  of  3'
    I_1_OF_4 = '1  of  4'
    I_1_OF_5 = '1  of  5'
    I_2_OF_2 = '2  of  2'
    I_2_OF_3 = '2  of  3'
    I_2_OF_4 = '2  of  4'
    I_2_OF_5 = '2  of  5'
    I_3_OF_3 = '3  of  3'
    I_3_OF_4 = '3  of  4'
    I_3_OF_5 = '3  of  5'
    I_4_OF_4 = '4  of  4'
    I_4_OF_5 = '4  of  5'
    I_5_OF_5 = '5  of  5'

class Sigs_Class_fieldEnum(str, Enum):
    NON_TO_CANONICAL_SIG = 'non-canonical sig'
    IV_INTERMITTENT_CANONICAL_SIG = 'iv intermittent canonical sig'
    RAD_SIG = 'rad sig'
    IV_CONTINUOUS_CANONICAL_SIG = 'iv continuous canonical sig'
    NON_TO_IV_CANONICAL_SIG = 'non-iv canonical sig'

class Sigs_DoseunitEnum(str, Enum):
    AUC = 'auc'
    G_KG = 'g/kg'
    GBQ = 'gbq'
    GY = 'gy'
    IU = 'iu'
    IU_KG = 'iu/kg'
    IU_M_2 = 'iu/m^2'
    IU_M_2_DAY = 'iu/m^2/day'
    KBQ_KG = 'kbq/kg'
    MBQ_KG = 'mbq/kg'
    MCG = 'mcg'
    MCG_DAY = 'mcg/day'
    MCG_KG = 'mcg/kg'
    MCG_M_2 = 'mcg/m^2'
    MCG_M_2_DAY = 'mcg/m^2/day'
    MCI_KG = 'mci/kg'
    MG = 'mg'
    MG_DAY = 'mg/day'
    MG_KG = 'mg/kg'
    MG_KG_DAY = 'mg/kg/day'
    MG_M_2 = 'mg/m^2'
    MG_M_2_DAY = 'mg/m^2/day'
    MG_M_2_HR = 'mg/m^2/hr'
    PFU_ML = 'pfu/ml'
    UNITS = 'units'
    UNITS_KG = 'units/kg'
    UNITS_M_2 = 'units/m^2'
    UNITS_M_2_DAY = 'units/m^2/day'

class Sigs_DosecapunitEnum(str, Enum):
    GBQ = 'gbq'
    MG = 'mg'
    MCI = 'mci'
    MG_M_2 = 'mg/m^2'
    MG_DAY = 'mg/day'
    IU = 'iu'
    MBQ = 'mbq'

class Sigs_TargetlevelunitEnum(str, Enum):
    NG_ML = 'ng/ml'
    MCG_L = 'mcg/l'
    MG_L = 'mg/l'

class Sigs_TargetleveltypeEnum(str, Enum):
    PEAK = 'peak'
    TROUGH = 'trough'

class Sigs_RouteEnum(str, Enum):
    IA = 'ia'
    IM = 'im'
    INHALED = 'inhaled'
    INTRAVESICULARLY = 'intravesicularly'
    IP = 'ip'
    IT = 'it'
    IV = 'iv'
    NEBULIZED = 'nebulized'
    NOT_SPECIFIED = 'not specified'
    PO = 'po'
    SC = 'sc'

class Sigs_DurationunitEnum(str, Enum):
    MINUTE = 'minute'
    DAY = 'day'
    HOUR = 'hour'
    SECOND = 'second'

class Sigs_FrequencyEnum(str, Enum):
    ONCE_PER_DAY = 'once per day'
    ONCE = 'once'
    CONTINUOUS = 'continuous'
    EVERY_12_HOURS = 'every 12 hours'
    TWICE_PER_DAY = 'twice per day'
    THREE_TIMES_PER_DAY = 'three times per day'
    DAILY_NOS = 'daily nos'
    FOUR_TIMES_PER_DAY = 'four times per day'
    EVERY_6_HOURS = 'every 6 hours'
    EVERY_4_HOURS = 'every 4 hours'
    ONCE_EVERY_MORNING = 'once every morning'
    ONCE_EVERY_EVENING = 'once every evening'
    EVERY_8_HOURS = 'every 8 hours'
    FIVE_TIMES_PER_DAY = 'five times per day'
    TWICE = 'twice'

class Studies_RegistryEnum(str, Enum):
    CLINICALTRIALS_GOV = 'clinicaltrials.gov'
    ISRCTN = 'isrctn'
    UMIN = 'umin'
    JAPANESE_CLINICAL_TRIALS_REGISTRY = 'japanese clinical trials registry'
    EUDRACT = 'eudract'
    CHICTR = 'chictr'
    JRCTS = 'jrcts'
    ACTRN = 'actrn'
    NETHERLANDS_TRIAL_REGISTRY = 'netherlands trial registry'
    DRKS = 'drks'
    DRK = 'drk'
    CLINICAL_TRIALS_REGISTRY_OF_INDIA = 'clinical trials registry of india'
    NL = 'nl'
    ANZCTR = 'anzctr'
    KCT = 'kct'
    RPCEC = 'rpcec'
    VALUE = ''

class Studies_Study_designEnum(str, Enum):
    CBD = 'cbd'
    ESCALATION = 'escalation'
    NON_TO_RANDOMIZED = 'non-randomized'
    IN_TO_CLASS_SWITCH = 'in-class switch'
    OUT_TO_OF_TO_CLASS_SWITCH = 'out-of-class switch'
    DE_TO_ESCALATION = 'de-escalation'
    MIXED = 'mixed'

class Studies_Sponsor_typeEnum(str, Enum):
    PHARMACEUTICAL_INDUSTRY = 'pharmaceutical industry'
    GOVERNMENT = 'government'
    COOPERATIVE_GROUP = 'cooperative group'
    ACADEMIC_MEDICAL_CENTER = 'academic medical center'
    COMMUNITY_PRACTICE = 'community practice'
    OTHER = 'other'
    ACADEMIC_CONSORTIUM = 'academic consortium'

class StudyResults_Endpoint_classEnum(str, Enum):
    TIME_TO_TO_TO_EVENT = 'time-to-event'
    RATE = 'rate'
    COULD_NOT_BE_DETERMINED = 'could not be determined'
    EVENT_AT_FIXED_TIME = 'event at fixed time'
    OTHER = 'other'
    RATE_AT_FIXED_TIME = 'rate at fixed time'
    TIME_TO_TO_TO_MEDIAN_EVENT = 'time-to-median event'

class StudyResults_Endpoint_typeEnum(str, Enum):
    UNDESIGNATED = 'undesignated'
    SECONDARY = 'secondary'
    PRIMARY = 'primary'
    CO_TO_PRIMARY = 'co-primary'

class StudyResults_Arm_typeEnum(str, Enum):
    CONTROL = 'control'
    ESCALATION = 'escalation'
    IN_TO_CLASS_SWITCH = 'in-class switch'
    OUT_TO_OF_TO_CLASS_SWITCH = 'out-of-class switch'
    DE_TO_ESCALATION = 'de-escalation'

class StudyResults_MetricunitEnum(str, Enum):
    MONTHS = 'months'
    WEEKS = 'weeks'
    TIMED_RATE = 'timed rate'
    UNTIMED_RATE = 'untimed rate'
    DAYS = 'days'
    YEARS = 'years'

class StudyResults_StatisticEnum(str, Enum):
    HR = 'hr'
    NOT_APPLICABLE = 'not applicable'
    SHR = 'shr'
    AHR = 'ahr'
    RR = 'rr'
    PFS48_DIFFERENCE = 'pfs48 difference'
    RMST_DIFFERENCE = 'rmst difference'
    OR = 'or'
    RMST = 'rmst'
    RATE_RATIO = 'rate ratio'

class Canonicaltriples_Class_1Enum(str, Enum):
    PROCEDURE = 'procedure'
    REGIMEN = 'regimen'
    ANY_CONCEPT = 'any concept'
    COMPONENT = 'component'
    STUDY = 'study'
    SYNTHETIC_REGIMEN = 'synthetic regimen'
    REGIMEN_CLASS = 'regimen class'
    REFERENCE = 'reference'
    COMPONENT_CLASS = 'component class'
    CONDITION = 'condition'
    CONTEXT = 'context'
    REGIMEN_STUB = 'regimen stub'
    REGIMEN_VARIANT = 'regimen variant'

class HemoncClasses_Omopdomain_idEnum(str, Enum):
    DRUG = 'drug'
    CONDITION = 'condition'
    PROCEDURE = 'procedure'
    MEASUREMENT = 'measurement'
    REGIMEN = 'regimen'

class HemoncClasses_Omopstandard_conceptEnum(str, Enum):
    RXNORM = 'rxnorm'
    C = 'c'
    HEMONC = 'hemonc'
    N_A_TO_NATIVELY_ENCODED = 'n/a - natively encoded'

class HemoncClasses_Class_typeEnum(str, Enum):
    CORE = 'core'
    EXTENSION = 'extension'
    INTERMEDIATE = 'intermediate'
    NUMERIC = 'numeric'
    READY_FOR_CORE = 'ready for core'

class Contexttable_IntentEnum(str, Enum):
    NON_TO_CURATIVE = 'non-curative'
    NOT_APPLICABLE = 'not applicable'
    CURATIVE = 'curative'
    UNSPECIFIED = 'unspecified'
    PREVENTION = 'prevention'

class Contexttable_PhaseEnum(str, Enum):
    ADJUVANT = 'adjuvant'
    CONSOLIDATION = 'consolidation'
    DEFINITIVE = 'definitive'
    DELAYED_INTENSIFICATION = 'delayed intensification'
    EARLY_INTENSIFICATION = 'early intensification'
    INDUCTION = 'induction'
    MAINTENANCE = 'maintenance'
    INTENSIFICATION = 'intensification'
    PRE_TO_PHASE = 'pre-phase'
    INTERIM_MAINTENANCE = 'interim maintenance'
    LATE_INTENSIFICATION = 'late intensification'
    NEOADJUVANT = 'neoadjuvant'
    PERIOPERATIVE = 'perioperative'

class Contexttable_Risk_stratificationEnum(str, Enum):
    HIGH_TO_RISK = 'high-risk'
    INTERMEDIATE_TO_RISK = 'intermediate-risk'
    LOW_TO_RISK = 'low-risk'
    UNSTRATIFIED = 'unstratified'
    FAVORABLE = 'favorable'
    UNFAVORABLE = 'unfavorable'
    STANDARD_TO_RISK = 'standard-risk'
    VERY_HIGH_TO_RISK = 'very high-risk'

class Contexttable_Therapy_typeEnum(str, Enum):
    CHEMORADIOTHERAPY = 'chemoradiotherapy'
    CHEMOTHERAPY = 'chemotherapy'
    ANTICOAGULATION = 'anticoagulation'
    LOCAL = 'local'
    SYSTEMIC = 'systemic'
    RADIOTHERAPY = 'radiotherapy'
    ENDOCRINE_THERAPY = 'endocrine therapy'
    REPLACEMENT_PRODUCTS = 'replacement products'
    IMMUNOTHERAPY = 'immunotherapy'
    INTRAPERITONEAL = 'intraperitoneal'
    ANTIBIOTIC = 'antibiotic'
    ADT_AND_RADIOTHERAPY = 'adt and radiotherapy'
    PERIOPERATIVE_THERAPY_AND_HYPERTHERMIC_INTRA_TO_PERITONEAL_C = 'perioperative therapy and hyperthermic intra-peritoneal chemotherapy'

class Exclusions_Rev1Enum(str, Enum):
    JEREMY = 'jeremy'
    ALEENAH = 'aleenah'

class Inclusions_Ref_typeEnum(str, Enum):
    PRIMARY = 'primary'
    EFFICACY_UPDATE = 'efficacy update'
    UNDETERMINED = 'undetermined'
    SAFETY_UPDATE = 'safety update'
    OTHER_UPDATE = 'other update'

class Inclusions_ReasonEnum(str, Enum):
    NON_TO_PHASE_3_WITH_PRIMARY_PUBLICATION_IN_HIGH_TO_IMPACT_JO = 'non-phase 3 with primary publication in high-impact journal'
    PHASE_3_SACT = 'phase 3 sact'
    EXCEPTION = 'exception'
    NON_TO_PHASE_3_PIVOTAL_STUDY = 'non-phase 3 pivotal study'
    PHASE_3_CLASSICAL_HEMATOLOGY = 'phase 3 classical hematology'
    NON_TO_PHASE_3_WITH_UPDATE_IN_HIGH_TO_IMPACT_JOURNAL = 'non-phase 3 with update in high-impact journal'
    CLINICAL_PRACTICE_GUIDELINE = 'clinical practice guideline'
    PHASE_3_GVHD = 'phase 3 gvhd'

class Units_Unit_typeEnum(str, Enum):
    UNITS_PER_VOLUME = 'units per volume'
    CALCULATED_DOSE = 'calculated dose'
    TIME = 'time'
    UNITS_PER_WEIGHT = 'units per weight'
    RADIATION_UNITS = 'radiation units'
    UNITLESS_QUANTITY = 'unitless quantity'
    UNITLESS_QUANTITY_PER_WEIGHT = 'unitless quantity per weight'
    UNITLESS_QUANTITY_PER_BSA = 'unitless quantity per bsa'
    WEIGHT = 'weight'
    WEIGHT_PER_SURFACE_AREA_USED_IN_BMI = 'weight per surface area (used in bmi)'
    BSA_BODY_SURFACE_AREA = 'bsa (body surface area)'
    UNITS_PER_TIME = 'units per time'
    WEIGHT_PER_VOLUME = 'weight per volume'
    UNITS_PER_BSA = 'units per bsa'
    UNITS_PER_BSA_PER_TIME = 'units per bsa per time'
    UNITS_PER_WEIGHT_PER_TIME = 'units per weight per time'
    WEIGHT_PER_VOLUME_USED_IN_CERTAIN_LABORATORY_TESTS_E_G_CREAT = 'weight per volume used in certain laboratory tests, e.g., creatinine'
    CREATININE_CLEARANCE = 'creatinine clearance'
    UNITLESS_QUANTITY_PER_BSA_PER_TIME = 'unitless quantity per bsa per time'

class Variantblob_BlockEnum(str, Enum):
    HEADER = 'header'
    BODY_TOP = 'body.top'
    BODY = 'body'
    BODY_BOTTOM = 'body.bottom'

class Variantblob_Chunk_typeEnum(str, Enum):
    STRING = 'string'
    NUMERIC = 'numeric'
    CUI = 'cui'

