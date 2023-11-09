from project.bench_grammers import *
from project.enums import (
    GateType, 
)


class BenchParser:
    @classmethod
    def fetch_from_line(cls, line: str) -> tuple[list[str], GateType]:
        ids: list(str) = []
        gate_type: GateType = GateType.NotFound

        if InputGrammer.can_parse_next(line, 0):
            ids = InputGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Input

        elif OutputGrammer.can_parse_next(line, 0):
            ids = OutputGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Output

        elif BufferGrammer.can_parse_next(line, 0):
            ids = BufferGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Buffer

        elif NotGrammer.can_parse_next(line, 0):
            ids = NotGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Not

        elif AndGrammer.can_parse_next(line, 0):
            ids = AndGrammer.parseString(line, parse_all=True)
            gate_type = GateType.And

        elif NandGrammer.can_parse_next(line, 0):
            ids = NandGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Nand

        elif OrGrammer.can_parse_next(line, 0):
            ids = OrGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Or

        elif NorGrammer.can_parse_next(line, 0):
            ids = NorGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Nor

        elif XorGrammer.can_parse_next(line, 0):
            ids = XorGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Xor

        elif XnorGrammer.can_parse_next(line, 0):
            ids = XnorGrammer.parseString(line, parse_all=True)
            gate_type = GateType.Xnor

        return (
            ids,
            gate_type
        )

class InputParser:
    @classmethod
    def fetch_list_from_line(cls, line: str) -> list:
        return line.strip().split(' ')