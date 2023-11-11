from enum import Enum


class OperationTypeEnum(Enum):
    Unknown = -1
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
