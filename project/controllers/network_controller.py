from io import (
    TextIOWrapper,
)

from project.controllers import (
    controller,
)

from project.file_parsers.bench_file_parser import (
    BenchFileParser,
)

from project.logic_units import *

from project.enums.gate_type_enum import (
    GateTypeEnum,
)


class NetworkController(controller.Controller):
    def __init__(self, bench_file_object: TextIOWrapper) -> None:
        self.__bench_file_object: TextIOWrapper = bench_file_object

        self.__input_gates: dict[str, Gate] = {}
        self.__intermidate_gates: dict[str, Gate] = {}
        self.__fanout_gates: dict[str, Gate] = {}
        self.__output_gates: dict[str, Gate] = {}

        self.__wires: list[Wire] = []

    @property
    def bench_file_object(self) -> TextIOWrapper:
        return self.__bench_file_object

    @property
    def input_gates(self) -> dict[str, Gate]:
        return self.__input_gates

    @input_gates.setter
    def input_gates(self, input_gate_: dict[str, Gate]) -> None:
        self.__input_gates = input_gate_

    @property
    def intermidate_gates(self) -> dict[str, Gate]:
        return self.__intermidate_gates

    @intermidate_gates.setter
    def intermidate_gates(self, intermidate_gate_: dict[str, Gate]) -> None:
        self.__intermidate_gates = intermidate_gate_

    @property
    def fanout_gates(self) -> dict[str, Gate]:
        return self.__fanout_gates

    @fanout_gates.setter
    def fanout_gates(self, fanout_gates_: dict[str, Gate]) -> None:
        self.__fanout_gates = fanout_gates_

    @property
    def output_gates(self) -> dict[str, Gate]:
        return self.__output_gates

    @output_gates.setter
    def output_gates(self, output_gate_: dict[str, Gate]) -> None:
        self.__output_gates = output_gate_

    @property
    def total_gates_with_level(self) -> dict[int, list[Gate]]:
        temp_gates: list[Gate] = list(self.input_gates.values()) + list(self.intermidate_gates.values(
        )) + list(self.fanout_gates.values()) + list(self.output_gates.values())

        levelize_gates: dict = {}
        for temp_gate in temp_gates:
            if temp_gate.level not in levelize_gates:
                levelize_gates[temp_gate.level] = [temp_gate]
            else:
                levelize_gates[temp_gate.level].append(temp_gate)

        return levelize_gates

    @property
    def wires(self) -> list[Wire]:
        return self.__wires

    @wires.setter
    def wires(self, wires_: list[Wire]):
        self.__wires = wires_

    def __update_primay_gates(self) -> None:
        line: str = self.bench_file_object.readline()

        while line:
            ids, gate_type = BenchFileParser.fetch_from_line(
                line=line
            )

            if gate_type == GateTypeEnum.NotFound:
                line = self.bench_file_object.readline()
                continue

            if gate_type == GateTypeEnum.Input:
                self.input_gates[ids[0]] = InputGate(id=ids[0])

            elif gate_type == GateTypeEnum.Output:
                self.output_gates[ids[0]] = OutputGate(id=ids[0])

            elif gate_type == GateTypeEnum.Buffer:
                self.intermidate_gates[ids[0]] = BufferGate(id=ids[0])

            elif gate_type == GateTypeEnum.Not:
                self.intermidate_gates[ids[0]] = NotGate(id=ids[0])

            elif gate_type == GateTypeEnum.And:
                self.intermidate_gates[ids[0]] = AndGate(id=ids[0])

            elif gate_type == GateTypeEnum.Nand:
                self.intermidate_gates[ids[0]] = NandGate(id=ids[0])

            elif gate_type == GateTypeEnum.Or:
                self.intermidate_gates[ids[0]] = OrGate(id=ids[0])

            elif gate_type == GateTypeEnum.Nor:
                self.intermidate_gates[ids[0]] = NorGate(id=ids[0])

            elif gate_type == GateTypeEnum.Xor:
                self.intermidate_gates[ids[0]] = XorGate(id=ids[0])

            elif gate_type == GateTypeEnum.Xnor:
                self.intermidate_gates[ids[0]] = XnorGate(id=ids[0])

            for id in ids[1:]:
                wire: Wire = Wire(
                    input_gate=(self.input_gates | self.intermidate_gates)[id],
                    output_gate=(self.input_gates |
                                 self.intermidate_gates)[ids[0]]
                )

                (self.input_gates | self.intermidate_gates)[
                    ids[0]].add_input_wire(wire)
                (self.input_gates | self.intermidate_gates)[
                    id].add_output_wire(wire)

                self.wires.append(wire)

            line = self.bench_file_object.readline()

    def __add_connection_to_output_gates(self) -> None:
        temp_gates: dict = self.input_gates | self.intermidate_gates

        for id, output_gate in self.output_gates.items():
            wire: Wire = Wire(
                input_gate=temp_gates[id],
                output_gate=output_gate
            )

            temp_gates[id].add_output_wire(wire)
            output_gate.add_input_wire(wire)

            self.wires.append(wire)

    def __update_fanout_gates(self) -> None:
        for id, gate in (self.input_gates | self.intermidate_gates).items():
            if len(gate.output_wires) > 1:
                fanout_gate: FanoutGate = FanoutGate(id=id)
                self.fanout_gates[id] = fanout_gate

                for output_wire in gate.output_wires:
                    output_wire.input_gate = fanout_gate

                    fanout_gate.add_output_wire(output_wire)

                gate.output_wires.clear()

                wire: Wire = Wire(
                    input_gate=gate,
                    output_gate=fanout_gate
                )
                gate.add_output_wire(wire)
                fanout_gate.add_input_wire(wire)

                self.wires.append(wire)

    def __update_gates_level(self) -> None:
        gate_queue: list[Gate] = list(self.input_gates.values())

        start_point: int = 0
        while len(gate_queue) != 0:
            assert start_point != len(gate_queue)

            temp_gate: Gate = gate_queue[start_point]

            if isinstance(temp_gate, InputGate):
                temp_gate.level = 0
            else:
                max_input_gate_level: int = 0
                for input_wire in temp_gate.input_wires:
                    if input_wire.input_gate.level == -1:
                        break
                    else:
                        max_input_gate_level = max(
                            max_input_gate_level,
                            input_wire.input_gate.level
                        )
                else:
                    temp_gate.level = max_input_gate_level + 1

            if temp_gate.level == -1:
                start_point += 1
            else:
                gate_queue.pop(start_point)

                for wire in temp_gate.output_wires:
                    if wire.output_gate not in gate_queue and wire.output_gate.level == -1:
                        gate_queue.append(wire.output_gate)

                start_point = 0

    def display_gates(self) -> None:
        for _, gate in self.input_gates.items():
            print(gate)

        for _, gate in self.intermidate_gates.items():
            print(gate)

        for _, gate in self.fanout_gates.items():
            print(gate)

        for _, gate in self.output_gates.items():
            print(gate)

    def inject_and_execute(self, inject_values: dict[str, str]) -> None:
        total_gates: dict[int, list[Gate]] = self.total_gates_with_level
        max_network_level = max(list(total_gates.keys()))

        for level in range(0, max_network_level + 1):
            gates_in_level: list[Gate] = total_gates[level]
            if level == 0:
                assert len(inject_values) == len(gates_in_level)

                for id, gate in self.input_gates.items():
                    gate.set_value_and_propagate(inject_values[id])
            else:
                for gate in gates_in_level:
                    gate.set_value_and_propagate()

    def write_nets(self, result_file_object: TextIOWrapper = None) -> None:
        total_gates: dict[int, list[Gate]] = self.total_gates_with_level
        max_network_level = max(list(total_gates.keys()))

        for gate_level in range(0, max_network_level+1):
            for gate in total_gates[gate_level]:
                if len(gate.output_wires) > 1:
                    index: int = 1
                    for output_wire in gate.output_wires:
                        result_file_object.write(output_wire.input_gate.id +
                                                 f'_{index}' + ' ' + output_wire.value + '\n')
                        index += 1
                elif len(gate.output_wires) == 1:
                    result_file_object.write(
                        gate.output_wires[0].input_gate.id + ' ' + gate.output_wires[0].value + '\n')

    def run(self) -> None:
        self.__update_primay_gates()
        self.__update_fanout_gates()
        self.__add_connection_to_output_gates()
        self.__update_gates_level()
