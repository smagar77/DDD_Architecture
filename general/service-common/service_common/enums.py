import enum


class ResponseTypeEnum(str, enum.Enum):
    success: str = 'SUCCESS'
    error: str = 'ERROR'
    warning: str = 'WARNING'
    info: str = 'INFO'


class UserTypeEnum(str, enum.Enum):
    farmer: str = 'FARMER'
    fpo: str = 'FPO'
    supplier: str = 'SUPPLIER'
    seller: str = 'SELLER',
    buyer: str = 'BUYER'
    adhtiya: str = 'ADHTIYA'
    field_agent: str = 'FIELD_AGENT'
    admin: str = 'ADMIN'
    super_admin: str = 'SUPER_ADMIN'


class OrderEnum(str, enum.Enum):
    desc: str = 'DESC'
    asc: str = 'ASC'


class OrderByEnum(str, enum.Enum):
    recently_added: str = 'RECENTLY_ADDED'
    recently_updated: str = 'RECENTLY_UPDATED'
    recently_added_rev: str = 'RECENTLY_ADDED_REV'
    recently_updated_rev: str = 'RECENTLY_UPDATED_REV'


class GenderEnum(str, enum.Enum):
    male = "MALE"
    female = "FEMALE"
    other = "OTHER"


class LanguageEnum(str, enum.Enum):
    english = "eng"
    marathi = "mar"
    hindi = "hin"


class CropSeasonEnum(str, enum.Enum):
    rubby: str = 'RUBBY'
    kharip: str = 'KHARIP'
    jade: str = 'JADE'


class CropTypeEnum(str, enum.Enum):
    main: str = 'MAIN'
    inter_crop: str = 'INTER_CROP'


class CropSowingMethodEnum(str, enum.Enum):
    hand: str = 'HAND'
    machine: str = 'MACHINE'
    tractor: str = 'TRACTOR'


class SoilTypeEnum(str, enum.Enum):
    fine_gained: str = 'FINE_GRAINED'
    black_soil: str = 'BLACK_SOIL'
    peat_soil: str = 'PEAT_SOIL'
    chalk_soil: str = 'CHALK_SOIL'
    loam_soil: str = 'LOAM_SOIL'
    clay_soil: str = 'CLAY_SOIL'
    slit_soil: str = 'SLIT_SOIL'
    sandy_soil: str = 'SANDY_SOIL'


class SurveyTypeEnum(str, enum.Enum):
    farmer: str = "FARMER"


class SurveyQuestionTypeEnum(str, enum.Enum):
    text: str = "FREE_TEXT"
    multi_choice: str = "MULTI_CHOICE"
