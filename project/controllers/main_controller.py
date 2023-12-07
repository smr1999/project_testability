from io import (
    TextIOWrapper,
)

from project.controllers.network_controller import (
    NetworkController,
)

from project.controllers.fault_simulation_controller import (
    FaultSimulationController,
)

from project.controllers.exhaustive_test_vector_injection_controller import (
    ExhaustiveTestVectorInjectionController,
)

from project.controllers.fault_dictionary_generator_controller import (
    FaultDictionaryGeneratorController,
)

from project.controllers.fault_collapse_controller import (
    FaultCollapseController,
)

from project.controllers.controller import (
    Controller,
)

from project.utilities.file_utility import (
    FileUtility,
)

from project.enums.fault_simulation_type_enum import (
    FaultSimulationTypeEnum,
)


class MainController(Controller):
    def __init__(self, bench_file_name: str, fault_dictionary_file_name: str) -> None:
        self.bench_file_name: str = bench_file_name
        self.fault_dictionary_file_name: str = fault_dictionary_file_name

    def __initilize_controllers(self) -> None:
        assert self.bench_file_name
        self.__network_controller = NetworkController(
            bench_file_object=FileUtility.read_file(
                file_dir=self.bench_file_name
            )
        )

        self.__fault_simulation_controller = FaultSimulationController(
            network_controller=self.__network_controller,
            fault_simulation_type=FaultSimulationTypeEnum.Deductive
        )

        self.__exhaustive_test_vector_injection_controller = ExhaustiveTestVectorInjectionController(
            network_controller=self.__network_controller,
            fault_simulation_controller=self.__fault_simulation_controller
        )

        self.__fault_collapse_controller = FaultCollapseController(
            network_controller=self.__network_controller
        )

    def run(self):
        self.__initilize_controllers()

        self.__network_controller.run()
        print(f'Network gates of {self.bench_file_name} has been initilized.')

        self.__exhaustive_test_vector_injection_controller.run()
        print(
            f'Exhaustive test vector injection on {self.bench_file_name} completed and faults found.')

        FaultDictionaryGeneratorController(
            detected_fault_dict=self.__exhaustive_test_vector_injection_controller.detected_fault_dict,
            essential_test_vectors=self.__exhaustive_test_vector_injection_controller.essential_test_vectors
        ).generate_fault_dictionary_file(
            fault_dictionary_file_object=FileUtility.write_file(
                file_dir=f'{self.fault_dictionary_file_name}_without_fault_collapsing.csv'
            )
        )
        print(
            f'Fault dictionary of {self.bench_file_name} without fault collapsing generated in {self.fault_dictionary_file_name}_without_fault_collapsing.csv.')

        self.__fault_collapse_controller.run()

        self.__exhaustive_test_vector_injection_controller.equivalent_fault_dict = self.__fault_collapse_controller.fault_collapse_dict
        self.__exhaustive_test_vector_injection_controller.apply_fault_collapse()

        FaultDictionaryGeneratorController(
            detected_fault_dict=self.__exhaustive_test_vector_injection_controller.detected_fault_dict,
            essential_test_vectors=self.__exhaustive_test_vector_injection_controller.essential_test_vectors
        ).generate_fault_dictionary_file(
            fault_dictionary_file_object=FileUtility.write_file(
                file_dir=f'{self.fault_dictionary_file_name}_with_fault_collapsing.csv'
            ),
            show_essential_test_vectors=True
        )
        print(
            f'Fault dictionary of {self.bench_file_name} with fault collapsing generated in {self.fault_dictionary_file_name}_with_fault_collapsing.csv.')
