from io import (
    TextIOWrapper,
)

from project.controllers.controller import (
    Controller,
)

from project.controllers.network_controller import (
    NetworkController
)

from project.logic_units import *

from project.operations.fault_simulation_operations.fault_simulation_deductive_operation import (
    FaultSimulationDeductiveOperation,
)

from project.enums.fault_simulation_type_enum import (
    FaultSimulationTypeEnum,
)


class FaultSimulationController(Controller):
    def __init__(self, network_controller: NetworkController, fault_simulation_type: FaultSimulationTypeEnum = FaultSimulationTypeEnum.Unknown) -> None:
        self.__network_controller: NetworkController = network_controller
        self.__fault_simulation_type: FaultSimulationTypeEnum = fault_simulation_type
        self.__all_faults_dict: dict[Wire, set[str]] = {}

    @property
    def network_controller(self) -> NetworkController:
        return self.__network_controller

    @property
    def fault_simulation_type(self) -> FaultSimulationTypeEnum:
        return self.__fault_simulation_type

    @property
    def all_fault_dict(self) -> dict[Wire, set[str]]:
        return self.__all_faults_dict

    def __fault_simulation_deductive(self) -> None:
        for level in range(0, self.network_controller.max_network_level + 1):
            for gate in self.network_controller.total_gates_with_level[level]:
                if isinstance(gate, InputGate):
                    FaultSimulationDeductiveOperation.input_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, OutputGate):
                    FaultSimulationDeductiveOperation.output_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                if isinstance(gate, BufferGate):
                    FaultSimulationDeductiveOperation.buffer_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, NotGate):
                    FaultSimulationDeductiveOperation.not_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, AndGate):
                    FaultSimulationDeductiveOperation.and_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, NandGate):
                    FaultSimulationDeductiveOperation.nand_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, OrGate):
                    FaultSimulationDeductiveOperation.or_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, NorGate):
                    FaultSimulationDeductiveOperation.nor_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, XorGate):
                    FaultSimulationDeductiveOperation.xor_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, XnorGate):
                    FaultSimulationDeductiveOperation.xnor_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

                elif isinstance(gate, FanoutGate):
                    FaultSimulationDeductiveOperation.fanout_operation(
                        gate=gate,
                        all_fault_dict=self.all_fault_dict
                    )

    def write_nets_and_outputs_faults(self, result_file_object: TextIOWrapper = None) -> None:
        for wire, fault_set in self.all_fault_dict.items():
            result_file_object.write(
                f'Wire:{wire.id}, Value:{wire.value}, Discovered faults:{fault_set} \n'
            )

        result_file_object.write("------------------\n")

        for output_gate in list(self.network_controller.output_gates.values()):
            result_file_object.write(
                f'OutputGate: {output_gate.id}, Value:{output_gate.value}, Wire:{output_gate.input_wires[0].id}, Discoverd faults:{self.all_fault_dict[output_gate.input_wires[0]]} \n'
            )

    def run(self) -> None:
        assert self.fault_simulation_type != FaultSimulationTypeEnum.Unknown

        if self.fault_simulation_type == FaultSimulationTypeEnum.Deductive:
            return self.__fault_simulation_deductive()

        assert False
