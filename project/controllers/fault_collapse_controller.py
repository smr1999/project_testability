from project.logic_units.gates import *

from project.operations.fault_collapse_operation import (
    FaultCollapseOperation,
)

from project.controllers.network_controller import (
    NetworkController,
)

from project.controllers.controller import (
    Controller,
)


class FaultCollapseController(Controller):
    def __init__(self, network_controller: NetworkController) -> None:
        self.__network_controller: NetworkController = network_controller
        self.__fault_collapse_dict: dict[str: str] = dict()

    @property
    def fault_collapse_dict(self) -> dict[str: str]:
        return self.__fault_collapse_dict

    def add_fault_collapse(self, fault_collapse: list[tuple[str, list[str]]]) -> None:
        for item in fault_collapse:
            for equivalent_fault in item[1]:
                assert equivalent_fault not in self.__fault_collapse_dict

                self.__fault_collapse_dict[equivalent_fault] = item[0]

    def run(self) -> None:
        for level in range(self.__network_controller.max_network_level+1):
            for gate in self.__network_controller.total_gates_with_level[level]:
                if isinstance(gate, BufferGate):
                    self.add_fault_collapse(
                        fault_collapse=FaultCollapseOperation.buffer_operation(
                            gate=gate
                        )
                    )
                elif isinstance(gate, NotGate):
                    self.add_fault_collapse(
                        fault_collapse=FaultCollapseOperation.not_operation(
                            gate=gate
                        )
                    )
                elif isinstance(gate, AndGate):
                    self.add_fault_collapse(
                        fault_collapse=FaultCollapseOperation.and_operation(
                            gate=gate
                        )
                    )
                elif isinstance(gate, OrGate):
                    self.add_fault_collapse(
                        fault_collapse=FaultCollapseOperation.or_operation(
                            gate=gate
                        )
                    )
                elif isinstance(gate, NandGate):
                    self.add_fault_collapse(
                        fault_collapse=FaultCollapseOperation.nand_operation(
                            gate=gate
                        )
                    )
                elif isinstance(gate, NorGate):
                    self.add_fault_collapse(
                        fault_collapse=FaultCollapseOperation.nor_operation(
                            gate=gate
                        )
                    )
                else:
                    # Fanout/Xor/Xnor gates don't have equivalent faults
                    pass
