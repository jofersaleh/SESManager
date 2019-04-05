from enum import Enum

# TODO-01 Define Error Type or Exception cbchoi


class AttributeType(Enum):
    BEHAVIOR = 0
    STRUCTURAL = 1
    ALTERNATIVE = 2
    UNKNOWN_TYPE = -1

    @staticmethod
    def resolve_type_from_str(name):
        if "BEHAVIOR" == name.upper():
            return AttributeType.BEHAVIOR
        elif "STRUCTURAL" == name.upper():
            return AttributeType.STRUCTURAL
        elif "ALTERNATIVE" == name.upper():
            return AttributeType.ALTERNATIVE
        else:
            return AttributeType.UNKNOWN_TYPE

    @staticmethod
    def resolve_type_from_enum(enum):
        if enum == AttributeType.BEHAVIOR:
            return "BEHAVIOR"
        elif enum == AttributeType.STRUCTURAL:
            return "STRUCTURAL"
        elif enum == AttributeType.ALTERNATIVE:
            return "ALTERNATIVE"
        else:
            return "UNKNOWN"


class AlternativeType(Enum):
    AND = 0
    OR = 1

    UNKNOWN_TYPE = -1

    @staticmethod
    def resolve_type_from_str(name):
        if "BEHAVIOR" == name.upper():
            return AttributeType.BEHAVIOR
        elif "STRUCTURAL" == name.upper():
            return AttributeType.STRUCTURAL
        elif "ALTERNATIVE" == name.upper():
            return AttributeType.ALTERNATIVE
        else:
            return AttributeType.UNKNOWN_TYPE

    @staticmethod
    def resolve_type_from_enum(enum):
        if enum == AttributeType.BEHAVIOR:
            return "BEHAVIOR"
        elif enum == AttributeType.STRUCTURAL:
            return "STRUCTURAL"
        elif enum == AttributeType.ALTERNATIVE:
            return "ALTERNATIVE"
        else:
            return "UNKNOWN"
