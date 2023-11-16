from project.controllers.main_controller import (
    MainController,
)


if __name__ == '__main__':
    MainController(
        bench_file_name='bench_files/c17.bench',
        input_file_name='input_files/c17.txt',
        test_input_file_name='test_files/deductive_fault_simulation_c17.txt',
        true_value_result_file_name='result_files/true_value_simulation_result_c17.txt'
    ).run()
