from project.operations.operation import (
    Operation,
)

from project.logic_units import *

from project.enums.logic_value_binary_enum import (
    LogicValueBinaryEnum,
)


class FaultSimulationDeductiveOperation(Operation):
    class ValidationFaultSimulationDeductiveOperation(Operation):
        @classmethod
        def __value_validation(cls, gate: Gate) -> None:
            assert gate.value in LogicValueBinaryEnum.list_values()

            for input_wire in gate.input_wires:
                assert input_wire.value in LogicValueBinaryEnum.list_values()

            for output_wire in gate.output_wires:
                assert output_wire.value in LogicValueBinaryEnum.list_values()

        @classmethod
        def input_operation(cls, gate: InputGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) == 0
            assert len(gate.output_wires) == 1

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def output_operation(cls, gate: OutputGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) == 1
            assert len(gate.output_wires) == 0

            assert gate.input_wires[0] in all_fault_dict

        @classmethod
        def buffer_operation(cls, gate: BufferGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) == 1
            assert len(gate.output_wires) == 1

            assert gate.input_wires[0] in all_fault_dict
            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def not_operation(cls, gate: NotGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) == 1
            assert len(gate.output_wires) == 1

            assert gate.input_wires[0] in all_fault_dict
            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def and_operation(cls, gate: AndGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) >= 2
            assert len(gate.output_wires) == 1

            for input_wire in gate.input_wires:
                assert input_wire in all_fault_dict

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def nand_operation(cls, gate: NandGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) >= 2
            assert len(gate.output_wires) == 1

            for input_wire in gate.input_wires:
                assert input_wire in all_fault_dict

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def or_operation(cls, gate: OrGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) >= 2
            assert len(gate.output_wires) == 1

            for input_wire in gate.input_wires:
                assert input_wire in all_fault_dict

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def nor_operation(cls, gate: NorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) >= 2
            assert len(gate.output_wires) == 1

            for input_wire in gate.input_wires:
                assert input_wire in all_fault_dict

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def xor_operation(cls, gate: XorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) >= 2
            assert len(gate.output_wires) == 1

            for input_wire in gate.input_wires:
                assert input_wire in all_fault_dict

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def xnor_operation(cls, gate: XnorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) >= 2
            assert len(gate.output_wires) == 1

            for input_wire in gate.input_wires:
                assert input_wire in all_fault_dict

            assert gate.output_wires[0] not in all_fault_dict

        @classmethod
        def fanout_operation(cls, gate: XorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
            cls.__value_validation(
                gate=gate
            )

            assert len(gate.input_wires) == 1
            assert len(gate.output_wires) >= 2

            assert gate.input_wires[0] in all_fault_dict

            for output_wire in gate.output_wires:
                assert output_wire not in all_fault_dict

    @classmethod
    def input_operation(cls, gate: InputGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.input_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def output_operation(cls, gate: OutputGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.output_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )
        pass

    @classmethod
    def buffer_operation(cls, gate: BufferGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.buffer_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
            all_fault_dict[gate.input_wires[0]]
        )

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def not_operation(cls, gate: NotGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.not_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
            all_fault_dict[gate.input_wires[0]]
        )

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def and_operation(cls, gate: AndGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.and_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        if gate.value == LogicValueBinaryEnum.ONE.value:
            for input_wire in gate.input_wires:
                all_fault_dict[gate.output_wires[0]] = all_fault_dict[
                    gate.output_wires[0]
                ].union(
                    all_fault_dict[input_wire]
                )

        else:
            temp: set[Wire] = set()

            for input_wire in gate.input_wires:
                if input_wire.value == LogicValueBinaryEnum.ZERO.value:
                    if len(all_fault_dict[gate.output_wires[0]]) == 0:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
                            all_fault_dict[input_wire]
                        )
                    else:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].intersection(
                            all_fault_dict[input_wire]
                        )
                else:
                    temp.union(
                        all_fault_dict[input_wire]
                    )

            all_fault_dict[gate.output_wires[0]
                           ] = all_fault_dict[gate.output_wires[0]] - temp

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def nand_operation(cls, gate: NandGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.nand_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        if gate.value == LogicValueBinaryEnum.ZERO.value:
            for input_wire in gate.input_wires:
                all_fault_dict[gate.output_wires[0]] = all_fault_dict[
                    gate.output_wires[0]
                ].union(
                    all_fault_dict[input_wire]
                )

        else:
            temp: set[Wire] = set()

            for input_wire in gate.input_wires:
                if input_wire.value == LogicValueBinaryEnum.ZERO.value:
                    if len(all_fault_dict[gate.output_wires[0]]) == 0:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
                            all_fault_dict[input_wire]
                        )
                    else:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].intersection(
                            all_fault_dict[input_wire]
                        )
                else:
                    temp.union(
                        all_fault_dict[input_wire]
                    )

            all_fault_dict[gate.output_wires[0]
                           ] = all_fault_dict[gate.output_wires[0]] - temp

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def or_operation(cls, gate: OrGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.or_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        if gate.value == LogicValueBinaryEnum.ZERO.value:
            for input_wire in gate.input_wires:
                all_fault_dict[gate.output_wires[0]] = all_fault_dict[
                    gate.output_wires[0]
                ].union(
                    all_fault_dict[input_wire]
                )

        else:
            temp: set[Wire] = set()

            for input_wire in gate.input_wires:
                if input_wire.value == LogicValueBinaryEnum.ONE.value:
                    if len(all_fault_dict[gate.output_wires[0]]) == 0:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
                            all_fault_dict[input_wire]
                        )
                    else:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].intersection(
                            all_fault_dict[input_wire]
                        )
                else:
                    temp.union(
                        all_fault_dict[input_wire]
                    )

            all_fault_dict[gate.output_wires[0]
                           ] = all_fault_dict[gate.output_wires[0]] - temp

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def nor_operation(cls, gate: NorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.nor_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        if gate.value == LogicValueBinaryEnum.ONE.value:
            for input_wire in gate.input_wires:
                all_fault_dict[gate.output_wires[0]] = all_fault_dict[
                    gate.output_wires[0]
                ].union(
                    all_fault_dict[input_wire]
                )

        else:
            temp: set[Wire] = set()

            for input_wire in gate.input_wires:
                if input_wire.value == LogicValueBinaryEnum.ONE.value:
                    if len(all_fault_dict[gate.output_wires[0]]) == 0:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
                            all_fault_dict[input_wire]
                        )
                    else:
                        all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].intersection(
                            all_fault_dict[input_wire]
                        )
                else:
                    temp.union(
                        all_fault_dict[input_wire]
                    )

            all_fault_dict[gate.output_wires[0]
                           ] = all_fault_dict[gate.output_wires[0]] - temp

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def xor_operation(cls, gate: XorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.xor_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        for index in range(1, 2**len(gate.input_wires)):
            binary_index: str = bin(index)[2:]

            if binary_index.count('1') % 2 == 1:
                binary_index = binary_index.zfill(len(gate.input_wires))
                include_wires: set[Wire] = set()
                exclude_wires: set[Wire] = set()

                for i in range(len(gate.input_wires)):
                    if binary_index[i] == LogicValueBinaryEnum.ZERO.value:
                        exclude_wires = exclude_wires.union(
                            all_fault_dict[gate.input_wires[i]]
                        )
                    else:
                        if len(include_wires) == 0:
                            include_wires = include_wires.union(
                                all_fault_dict[gate.input_wires[i]]
                            )

                        else:
                            include_wires = include_wires.intersection(
                                all_fault_dict[gate.input_wires[i]]
                            )

                all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
                    include_wires - exclude_wires
                )

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def xnor_operation(cls, gate: XnorGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.xnor_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        all_fault_dict[gate.output_wires[0]] = set()

        for index in range(1, 2**len(gate.input_wires)):
            binary_index: str = bin(index)[2:]

            if binary_index.count('1') % 2 == 1:
                binary_index = binary_index.zfill(len(gate.input_wires))
                include_wires: set[Wire] = set()
                exclude_wires: set[Wire] = set()

                for i in range(len(gate.input_wires)):
                    if binary_index[i] == LogicValueBinaryEnum.ZERO.value:
                        exclude_wires = exclude_wires.union(
                            all_fault_dict[gate.input_wires[i]]
                        )
                    else:
                        if len(include_wires) == 0:
                            include_wires = include_wires.union(
                                all_fault_dict[gate.input_wires[i]]
                            )

                        else:
                            include_wires = include_wires.intersection(
                                all_fault_dict[gate.input_wires[i]]
                            )

                all_fault_dict[gate.output_wires[0]] = all_fault_dict[gate.output_wires[0]].union(
                    include_wires - exclude_wires
                )

        all_fault_dict[gate.output_wires[0]].add(
            f'{gate.output_wires[0].id}_s-a-{LogicValueBinaryEnum.ONE.value if gate.output_wires[0].value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
        )

    @classmethod
    def fanout_operation(cls, gate: FanoutGate, all_fault_dict: dict[Wire, set[str]]) -> None:
        cls.ValidationFaultSimulationDeductiveOperation.fanout_operation(
            gate=gate,
            all_fault_dict=all_fault_dict
        )

        for output_wire in gate.output_wires:
            all_fault_dict[output_wire] = set()

            all_fault_dict[output_wire] = all_fault_dict[output_wire].union(
                all_fault_dict[gate.input_wires[0]]
            )

            all_fault_dict[output_wire].add(
                f'{output_wire.id}_s-a-{LogicValueBinaryEnum.ONE.value if output_wire.value == LogicValueBinaryEnum.ZERO.value else LogicValueBinaryEnum.ZERO.value}'
            )
