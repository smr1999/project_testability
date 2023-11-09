from io import (
    TextIOWrapper,
)

from project.gates import *
from project.wires import *
from project.parsers import BenchParser
from project.enums import GateType


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

    def add_input_gate(self, id: str, input_gate_: InputGate):
        assert id not in self.input_gates

        self.input_gates[id] = input_gate_

    @property
    def intermidate_gates(self) -> dict:
        return self.__intermidate_gates

    @intermidate_gates.setter
    def intermidate_gates(self, intermidate_gate_: dict) -> None:
        self.__intermidate_gates = intermidate_gate_

    def add_intermidate_gate(self, id: str, intermidate_gate_: Gate):
        assert id not in self.intermidate_gates
        assert intermidate_gate_ not in [InputGate, OutputGate, FanoutGate]

        self.intermidate_gates[id] = intermidate_gate_

    @property
    def fanout_gates(self) -> dict:
        return self.__fanout_gates

    @fanout_gates.setter
    def fanout_gates(self, fanout_gates_: dict) -> None:
        self.__fanout_gates = fanout_gates_

    def add_fanout_gate(self, id: str, fanout_gate_: FanoutGate) -> None:
        assert id not in self.fanout_gates

        self.fanout_gates[id] = fanout_gate_

    @property
    def output_gates(self) -> dict:
        return self.__output_gates

    @output_gates.setter
    def output_gates(self, output_gate_: dict) -> None:
        self.__output_gates = output_gate_

    def _add_output_gate(self, id: str, output_gate_: OutputGate):
        assert id not in self.output_gates

        self.output_gates[id] = output_gate_

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

    def update_gates(self) -> None:
        self.__update_primay_gates()
        self.__update_fanout_gates()
        self.__add_connection_to_output_gates()

    def display_gates(self) -> None:
        for _, gate in self.input_gates.items():
            print(gate)

        for _, gate in self.intermidate_gates.items():
            print(gate)

        for _, gate in self.fanout_gates.items():
            print(gate)

        for _, gate in self.output_gates.items():
            print(gate)


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
        self.__gate_controller = GateController(
            bench_file_object=self.__read_file(self.bench_file_name)
        )

    def run(self):
        self.__initilize_controllers()

        self.__gate_controller.update_gates()
        self.__gate_controller.display_gates()
