from io import (
    TextIOWrapper,
)

from project.controllers.network_controller import (
    NetworkController,
)

from project.controllers.input_controller import (
    InputController,
)

from project.controllers.fault_simulation_controller import (
    FaultSimulationController,
)

from project.enums.fault_simulation_type_enum import (
    FaultSimulationTypeEnum,
)


class MainController:
    def __init__(self, bench_file_name: str, input_file_name: str, test_input_file_name: str, true_value_result_file_name: str) -> None:
        self.bench_file_name: str = bench_file_name
        self.input_file_name: str = input_file_name
        self.test_input_file_name: str = test_input_file_name
        self.true_value_result_file_name: str = true_value_result_file_name

    def __read_file(self, file_dir_: str) -> TextIOWrapper:
        return open(
            file=file_dir_,
            mode='r'
        )

    def __write_file(self, file_dir_: str) -> TextIOWrapper:
        return open(
            file=file_dir_,
            mode='w'
        )

    def __initilize_controllers(self) -> None:
        assert self.bench_file_name
        self.__network_controller = NetworkController(
            bench_file_object=self.__read_file(self.bench_file_name)
        )

        assert self.input_file_name
        self.__input_controller = InputController(
            input_file_object=self.__read_file(self.input_file_name)
        )

        assert self.test_input_file_name
        self.__test_input_controller = InputController(
            input_file_object=self.__read_file(self.test_input_file_name)
        )

        self.__fault_simulation_controller = FaultSimulationController(
            network_controller=self.__network_controller,
            fault_simulation_type=FaultSimulationTypeEnum.Deductive
        )

    def run(self):
        self.__initilize_controllers()

        self.__network_controller.run()
        print('Network of gates has been initilized.')

        self.__input_controller.run()
        print('Input file has been read.')

        self.__network_controller.inject_and_execute(
            inject_values=self.__input_controller.inputs
        )
        print('Inputs injected to network and gated has been executed.')

        # self.__network_controller.display_gates()
        self.__network_controller.write_nets(
            result_file_object=self.__write_file(
                file_dir_=self.true_value_result_file_name
            )
        )
        print('True-Value simulation result has been wrote in file.')

        self.__network_controller.reset()
        print('Network values has been reset.')

        self.__test_input_controller.run()
        print('Test input file has been read.')

        self.__network_controller.inject_and_execute(
            inject_values=self.__test_input_controller.inputs
        )
        print('Test inputs injected to network and gated has been executed.')

        self.__fault_simulation_controller.run()
        for k, v in self.__fault_simulation_controller.all_fault_dict.items():
            print(k , v)