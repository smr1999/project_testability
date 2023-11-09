from io import (
    TextIOWrapper,
)

from project.gates import *
from project.wires import *
from project.parsers import (
    BenchParser,
    InputParser
)
from project.enums import (
    GateType,
    LogicValue
)


class GateController:
    def __init__(self, bench_file_object: TextIOWrapper) -> None:
        self.__bench_file_object: TextIOWrapper = bench_file_object

        self.__input_gates: dict = {}
        self.__intermidate_gates: dict = {}
        self.__fanout_gates: dict = {}
        self.__output_gates: dict = {}

    @property
    def bench_file_object(self) -> TextIOWrapper:
        return self.__bench_file_object

    @property
    def input_gates(self) -> dict:
        return self.__input_gates

    @input_gates.setter
    def input_gates(self, input_gate_: dict) -> None:
        self.__input_gates = input_gate_

    @property
    def intermidate_gates(self) -> dict:
        return self.__intermidate_gates

    @intermidate_gates.setter
    def intermidate_gates(self, intermidate_gate_: dict) -> None:
        self.__intermidate_gates = intermidate_gate_

    @property
    def fanout_gates(self) -> dict:
        return self.__fanout_gates

    @fanout_gates.setter
    def fanout_gates(self, fanout_gates_: dict) -> None:
        self.__fanout_gates = fanout_gates_

    @property
    def output_gates(self) -> dict:
        return self.__output_gates

    @output_gates.setter
    def output_gates(self, output_gate_: dict) -> None:
        self.__output_gates = output_gate_

    def __update_primay_gates(self) -> None:
        line = self.bench_file_object.readline()

        while line:
            ids, gate_type = BenchParser.fetch_from_line(line)

            if gate_type == GateType.NotFound:
                line = self.bench_file_object.readline()
                continue

            if gate_type == GateType.Input:
                self.input_gates[ids[0]] = InputGate(ids[0])

            elif gate_type == GateType.Output:
                self.output_gates[ids[0]] = OutputGate(ids[0])

            elif gate_type == GateType.Buffer:
                self.intermidate_gates[ids[0]] = BufferGate(ids[0])

            elif gate_type == GateType.Not:
                self.intermidate_gates[ids[0]] = NotGate(ids[0])

            elif gate_type == GateType.And:
                self.intermidate_gates[ids[0]] = AndGate(ids[0])

            elif gate_type == GateType.Nand:
                self.intermidate_gates[ids[0]] = NandGate(ids[0])

            elif gate_type == GateType.Or:
                self.intermidate_gates[ids[0]] = OrGate(ids[0])

            elif gate_type == GateType.Nor:
                self.intermidate_gates[ids[0]] = NorGate(ids[0])

            elif gate_type == GateType.Xor:
                self.intermidate_gates[ids[0]] = XorGate(ids[0])

            elif gate_type == GateType.Xnor:
                self.intermidate_gates[ids[0]] = XnorGate(ids[0])

            temp_gates = self.input_gates | self.intermidate_gates

            for w in ids[1:]:
                wire = Wire(
                    input_gate=temp_gates[w],
                    output_gate=temp_gates[ids[0]]
                )

                temp_gates[ids[0]].add_input_wire(wire)
                temp_gates[w].add_output_wire(wire)

            line = self.bench_file_object.readline()

    def __add_connection_to_output_gates(self) -> None:
        temp_gates = self.input_gates | self.intermidate_gates

        for id, output_gate in self.output_gates.items():
            wire = Wire(
                input_gate=temp_gates[id],
                output_gate=output_gate
            )

            temp_gates[id].add_output_wire(wire)
            output_gate.add_input_wire(wire)

    def __update_fanout_gates(self) -> None:
        for id, gate in (self.input_gates | self.intermidate_gates).items():
            if len(gate.output_wires) > 1:
                fanout_gate = FanoutGate(id=id)
                self.fanout_gates[id] = fanout_gate

                for output_wire in gate.output_wires:
                    output_wire.input_gate = fanout_gate

                    fanout_gate.add_output_wire(output_wire)

                gate.output_wires = []

                wire = Wire(
                    input_gate=gate,
                    output_gate=fanout_gate
                )
                gate.add_output_wire(wire)
                fanout_gate.add_input_wire(wire)

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

    def inject_and_execute(self, inject_values: dict) -> None:
        assert len(self.input_gates) == len(inject_values)

        for id, value in inject_values.items():
            input_gate: Gate = self.input_gates.get(id, None)
            assert input_gate

            input_gate.set_value_and_propagate(value)

        temp_gates: list[Gate] = list(self.intermidate_gates.values(
        )) + list(self.fanout_gates.values()) + list(self.output_gates.values())

        levelize_gates: dict = {}
        for temp_gate in temp_gates:
            if temp_gate.level not in levelize_gates:
                levelize_gates[temp_gate.level] = [temp_gate]
            else:
                levelize_gates[temp_gate.level].append(temp_gate)

        max_network_level: int = max(list(levelize_gates.keys()))

        for level in range(1, max_network_level + 1):
            for gate in levelize_gates[level]:
                gate.set_value_and_propagate()

    def run(self) -> None:
        self.__update_primay_gates()
        self.__update_fanout_gates()
        self.__add_connection_to_output_gates()
        self.__update_gates_level()


class InputController:
    def __init__(self, input_file_object: TextIOWrapper) -> None:
        self.__input_file_object: TextIOWrapper = input_file_object

        self.__inputs: dict = {}

    @property
    def input_file_object(self) -> TextIOWrapper:
        return self.__input_file_object

    @property
    def inputs(self) -> dict:
        return self.__inputs

    @inputs.setter
    def inputs(self, inputs_: dict) -> None:
        self.__inputs = inputs_

    def __update_inputs(self) -> None:
        lines = self.input_file_object.readlines()
        assert len(lines) == 2

        ids = InputParser.fetch_list_from_line(lines[0])
        values = InputParser.fetch_list_from_line(lines[1])

        assert len(ids) == len(values)

        self.inputs = dict(zip(ids, values))

    def __validate_inputs(self) -> None:
        for id, value in self.inputs.items():
            assert value in LogicValue.list_values()

    def run(self) -> None:
        self.__update_inputs()
        self.__validate_inputs()


class Controller:
    def __init__(self, bench_file_name: str, input_file_name: str, test_input_file_name: str) -> None:
        self.bench_file_name: str = bench_file_name
        self.input_file_name: str = input_file_name
        self.test_vector_file_name: str = test_input_file_name

    def __read_file(self, file_dir_: str) -> TextIOWrapper:
        return open(
            file=file_dir_,
            mode='r'
        )

    def __initilize_controllers(self) -> None:
        assert self.bench_file_name
        self.__gate_controller = GateController(
            bench_file_object=self.__read_file(self.bench_file_name)
        )

        assert self.input_file_name
        self.__input_controller = InputController(
            input_file_object=self.__read_file(self.input_file_name)
        )

    def run(self):
        self.__initilize_controllers()

        self.__gate_controller.run()
        self.__input_controller.run()

        self.__gate_controller.inject_and_execute(
            self.__input_controller.inputs)

        self.__gate_controller.display_gates()
