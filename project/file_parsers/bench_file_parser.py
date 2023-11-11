from project.file_parsers.file_parser import (
    FileParser,
)

from project.grammers.bench_grammer import *

from project.enums.gate_type_enum import (
    GateTypeEnum,
)


class BenchFileParser(FileParser):
    @classmethod
    def fetch_from_line(cls, line: str) -> tuple[list[str], GateTypeEnum]:
        ids: list(str) = []
        gate_type: GateTypeEnum = GateTypeEnum.NotFound

        if InputGrammer.can_parse_next(line, 0):
            ids = InputGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Input

        elif OutputGrammer.can_parse_next(line, 0):
            ids = OutputGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Output

        elif BufferGrammer.can_parse_next(line, 0):
            ids = BufferGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Buffer

        elif NotGrammer.can_parse_next(line, 0):
            ids = NotGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Not

        elif AndGrammer.can_parse_next(line, 0):
            ids = AndGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.And

        elif NandGrammer.can_parse_next(line, 0):
            ids = NandGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Nand

        elif OrGrammer.can_parse_next(line, 0):
            ids = OrGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Or

        elif NorGrammer.can_parse_next(line, 0):
            ids = NorGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Nor

        elif XorGrammer.can_parse_next(line, 0):
            ids = XorGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Xor

        elif XnorGrammer.can_parse_next(line, 0):
            ids = XnorGrammer.parseString(line, parse_all=True)
            gate_type = GateTypeEnum.Xnor

        return (
            ids,
            gate_type
        )
