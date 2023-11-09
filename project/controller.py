from project.gates import *
from project.wires import *
from project.parsers import BenchParser
from project.enums import GateType

class Controller:
    def __init__(self, bench_file_name: str, input_file_name: str, test_vector_file_name: str) -> None:
        self.__bench_file_name: str = bench_file_name
        self.__input_file_name: str = input_file_name
        self.__test_vector_file_name: str = test_vector_file_name
        
        self.__gates = {}
        
    def read_file(self, file_dir_: str):
        return open(
            file=file_dir_,
            mode='r'
        )
    
    def add_primay_gates(self):
        file = self.read_file(
            file_dir_= self.__bench_file_name
        )

        line = file.readline()
        while line:
            ids, gate_type = BenchParser.fetch_from_line(line)

            if gate_type == GateType.NotFound:
                line = file.readline()
                continue
            
            if gate_type == GateType.Input:
                self.gates[ids[0]] = InputGate(ids[0])
            
            elif gate_type == GateType.Output:
                self.gates[ids[0]] = OutputGate(ids[0])
            
            elif gate_type == GateType.Buffer:
                self.gates[ids[0]] = BufferGate(ids[0])

            elif gate_type == GateType.Not:
                self.gates[ids[0]] = NotGate(ids[0])

            elif gate_type == GateType.And:
                self.gates[ids[0]] = AndGate(ids[0])

            elif gate_type == GateType.Nand:
                self.gates[ids[0]] = NandGate(ids[0])

            elif gate_type == GateType.Or:
                self.gates[ids[0]] = OrGate(ids[0])

            elif gate_type == GateType.Nor:
                self.gates[ids[0]] = NorGate(ids[0])

            elif gate_type == GateType.Xor:
                self.gates[ids[0]] = XorGate(ids[0])

            elif gate_type == GateType.Xnor:
                self.gates[ids[0]] = XnorGate(ids[0])
            
            for w in ids[1:]:
                wire = Wire(
                    input_gate = self.gates[w],
                    output_gate= self.gates[ids[0]]
                )

                self.gates[ids[0]].add_input_wire(wire)
                self.gates[w].add_output_wire(wire)

            line = file.readline()

    def add_fanout_gates(self):
        primary_gates = self.gates.copy().items()

        for id, gate in primary_gates:
            if len(gate.output_wires) > 1:
                gate_id = f'{id}-f'

                fanout_gate = FanoutGate(id = gate_id)
                self.gates[gate_id] = fanout_gate
                
                wire = Wire(
                    input_gate= gate,
                    output_gate= fanout_gate
                )

                for output_wire in gate.output_wires:
                    output_wire.input_gate = fanout_gate

                    fanout_gate.add_output_wire(output_wire)

                gate.output_wires.clear()
                gate.add_output_wire(wire)
                fanout_gate.add_input_wire(wire)

    @property
    def gates(self):
        return self.__gates
    


