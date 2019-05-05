from enum import Enum

# TODO-01 Define Error Type or Exception cbchoi


class AttributeType(Enum):
    # BEHAVIOR = 0
    ASPECT = 1
    MULTI_ASPECT = 2
    UNKNOWN_TYPE = -1

    @staticmethod
    def resolve_type_from_str(name):
        # if "BEHAVIOR" == name.upper():
        #    return AttributeType.BEHAVIOR
        if "ASPECT" == name.upper():
            return AttributeType.ASPECT
        elif "MULTI_ASPECT" == name.upper():
            return AttributeType.MULTI_ASPECT
        else:
            return AttributeType.UNKNOWN_TYPE

    @staticmethod
    def resolve_type_from_enum(enum):
        # if enum == AttributeType.BEHAVIOR:
        #    return "BEHAVIOR"
        if enum == AttributeType.ASPECT:
            return "ASPECT"
        elif enum == AttributeType.MULTI_ASPECT:
            return "MULTI_ASPECT"
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
        elif "ASPECT" == name.upper():
            return AttributeType.ASPECT
        elif "ALTERNATIVE" == name.upper():
            return AttributeType.MULTI_ASPECT
        else:
            return AttributeType.UNKNOWN_TYPE

    @staticmethod
    def resolve_type_from_enum(enum):
        if enum == AttributeType.BEHAVIOR:
            return "BEHAVIOR"
        elif enum == AttributeType.ASPECT:
            return "ASPECT"
        elif enum == AttributeType.MULTI_ASPECT:
            return "ALTERNATIVE"
        else:
            return "UNKNOWN"
