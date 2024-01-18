from project.controllers.network_controller import (
    NetworkController,
)

from project.controllers.fault_simulation_controller import (
    FaultSimulationController,
)

from project.controllers.controller import (
    Controller,
)

from project.logic_units.gates import *


class ExhaustiveTestVectorInjectionController(Controller):
    def __init__(self, network_controller: NetworkController, fault_simulation_controller: FaultSimulationController) -> None:
        self.__network_controller: NetworkController = network_controller
        self.__fault_simulation_controller: FaultSimulationController = fault_simulation_controller
        self.__detected_fault_dict: dict[str: set[str]] = dict()

        self.__equivalent_fault_dict: dict[str: str] = None

    @property
    def detected_fault_dict(self) -> dict[str: set[str]]:
        return self.__detected_fault_dict

    @property
    def equivalent_fault_dict(self) -> dict[str: str]:
        return self.__equivalent_fault_dict

    @equivalent_fault_dict.setter
    def equivalent_fault_dict(self, equivalent_fault_dict_: dict[str: str]) -> None:
        self.__equivalent_fault_dict = equivalent_fault_dict_

    def __get_eqivalent_fault(self, fault_name: str) -> str:
        if fault_name in self.__equivalent_fault_dict:
            # return self.__get_eqivalent_fault(
            #     fault_name=self.__equivalent_fault_dict[fault_name]
            # )
            return self.__equivalent_fault_dict[fault_name]

        return fault_name

    def apply_fault_collapse(self) -> None:
        assert self.__equivalent_fault_dict

        for test_vector_bin, detected_faults in self.__detected_fault_dict.items():
            temp_detected_faults: list[str] = list(detected_faults)

            for gate_level in range(self.__network_controller.max_network_level):
                for _, gates in self.__network_controller.total_gates_with_level.items():
                    for gate in gates:
                        if not isinstance(gate, FanoutGate):
                            for input_wire in gate.input_wires:
                                s_a_0_fault: str = f'{input_wire.id}_s-a-0'
                                s_a_1_fault: str = f'{input_wire.id}_s-a-1'

                                if s_a_0_fault in temp_detected_faults:
                                    temp_detected_faults[temp_detected_faults.index(
                                        s_a_0_fault)] = self.__get_eqivalent_fault(fault_name=s_a_0_fault)

                                if s_a_1_fault in temp_detected_faults:
                                    temp_detected_faults[temp_detected_faults.index(
                                        s_a_1_fault)] = self.__get_eqivalent_fault(fault_name=s_a_1_fault)

            self.__detected_fault_dict[test_vector_bin] = set(
                temp_detected_faults
            )

    @property
    def essential_test_vectors(self) -> list[str]:
        detected_fault_test_vectors: dict[str: list[str]] = dict()
        for test_vector_bin, detected_faults in self.__detected_fault_dict.items():
            for detected_fault in detected_faults:
                if detected_fault not in detected_fault_test_vectors:
                    detected_fault_test_vectors[detected_fault] = [
                        test_vector_bin]
                else:
                    detected_fault_test_vectors[detected_fault].append(
                        test_vector_bin)

        essential_test_vectors_: list[str] = list()

        for _, test_vectors in detected_fault_test_vectors.items():
            if len(test_vectors) == 1:
                essential_test_vectors_.append(test_vectors[0])

        return essential_test_vectors_

    def run(self) -> None:
        for test_vector in range(2**len(self.__network_controller.input_gates)):
            test_vector_bin: str = bin(test_vector)[2:].zfill(
                len(self.__network_controller.input_gates)
            )

            test_vector_list: list[str] = list(test_vector_bin)

            self.__network_controller.inject_and_execute(
                inject_values=test_vector_list
            )
            self.__fault_simulation_controller.run()
            self.__detected_fault_dict[test_vector_bin] = self.__fault_simulation_controller.detectable_faults

            self.__fault_simulation_controller.reset()
            self.__network_controller.reset()
