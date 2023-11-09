from enum import Enum


class OperationType(Enum):
    Input = 1
    Output = 2
    Buffer = 3
    Not = 4
    And = 5
    Nand = 6
    Or = 7
    Nor = 8
    Xor = 9
    Xnor = 10
    Fanout = 11


class LogicValue(Enum):
    ZERO = '0'
    ONE = '1'
    HIGH_IMPEDANCE = 'Z'
    UNKNOWN = 'X'

    @classmethod
    def list_values(cls):
        return list(map(lambda item: item.value, cls))


class GateType(Enum):
    Input = 1
    Output = 2
    Buffer = 3
    Not = 4
    And = 5
    Nand = 6
    Or = 7
    Nor = 8
    Xor = 9
    Xnor = 10
    NotFound = 11