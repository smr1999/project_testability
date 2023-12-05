from project.logic_units.gates import *

from project.operations.operation import (
    Operation,
)


class FaultCollapseOperation(Operation):
    @classmethod
    def buffer_operation(cls, gate: BufferGate) -> list[tuple[str, list[str]]]:
        return [
            (
                f'{gate.output_wires[0].id}_s-a-0',
                [f'{gate.input_wires[0].id}_s-a-0']
            ),
            (
                f'{gate.output_wires[0].id}_s-a-1',
                [f'{gate.input_wires[0].id}_s-a-1']
            ),
        ]

    @classmethod
    def not_operation(cls, gate: NotGate) -> list[tuple[str, list[str]]]:
        return [
            (
                f'{gate.output_wires[0].id}_s-a-0',
                [f'{gate.input_wires[0].id}_s-a-1']
            ),
            (
                f'{gate.output_wires[0].id}_s-a-1',
                [f'{gate.input_wires[0].id}_s-a-0']
            ),
        ]

    @classmethod
    def and_operation(cls, gate: AndGate) -> list[tuple[str, list[str]]]:
        return [
            (
                f'{gate.output_wires[0].id}_s-a-0',
                [f'{input_wire.id}_s-a-0' for input_wire in gate.input_wires]
            ),
        ]

    @classmethod
    def or_operation(cls, gate: OrGate) -> list[tuple[str, list[str]]]:
        return [
            (
                f'{gate.output_wires[0].id}_s-a-1',
                [f'{input_wire.id}_s-a-1' for input_wire in gate.input_wires]
            )
        ]

    @classmethod
    def nand_operation(cls, gate: NandGate) -> list[tuple[str, list[str]]]:
        return [
            (
                f'{gate.output_wires[0].id}_s-a-1',
                [f'{input_wire.id}_s-a-0' for input_wire in gate.input_wires]
            )
        ]

    @classmethod
    def nor_operation(cls, gate: NorGate) -> list[tuple[str, list[str]]]:
        return [
            (
                f'{gate.output_wires[0].id}_s-a-0',
                [f'{input_wire.id}_s-a-1' for input_wire in gate.input_wires]
            )
        ]

    @classmethod
    def xor_operation(cls, gate: XorGate) -> list[tuple[str, list[str]]]:
        return []

    @classmethod
    def xor_operation(cls, gate: XnorGate) -> list[tuple[str, list[str]]]:
        return []

    @classmethod
    def fanout_operation(cls, gate: FanoutGate) -> list[tuple[str, list[str]]]:
        return []
