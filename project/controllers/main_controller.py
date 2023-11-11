from io import (
    TextIOWrapper,
)

from project.controllers.network_controller import (
    NetworkController,
)

from project.controllers.input_controller import (
    InputController,
)


class MainController:
    def __init__(self, bench_file_name: str, input_file_name: str, test_input_file_name: str, true_value_result_file_name: str) -> None:
        self.bench_file_name: str = bench_file_name
        self.input_file_name: str = input_file_name
        self.test_vector_file_name: str = test_input_file_name
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
