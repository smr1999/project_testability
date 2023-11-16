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
        max_gate_level: int = max(
            list(self.network_controller.total_gates_with_level.keys())
        )

        for level in range(0, max_gate_level + 1):
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

    def run(self) -> None:
        assert self.fault_simulation_type != FaultSimulationTypeEnum.Unknown

        if self.fault_simulation_type == FaultSimulationTypeEnum.Deductive:
            return self.__fault_simulation_deductive()

        assert False
