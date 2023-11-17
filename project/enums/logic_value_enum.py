from enum import Enum


class LogicValueEnum(Enum):
    ZERO = '0'
    ONE = '1'
    HIGH_IMPEDANCE = 'Z'
    UNKNOWN = 'U'

    @classmethod
    def list_values(cls):
        return list(map(lambda item: item.value, cls))
