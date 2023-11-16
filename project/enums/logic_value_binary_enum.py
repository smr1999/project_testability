from enum import Enum

class LogicValueBinaryEnum(Enum):
    ZERO = '0'
    ONE = '1'

    @classmethod
    def list_values(cls):
        return list(map(lambda item: item.value, cls))