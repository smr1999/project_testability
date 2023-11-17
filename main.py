from project.controllers.main_controller import (
    MainController,
)


if __name__ == '__main__':
    MainController(
        bench_file_name='bench_files/c7552.bench',
        input_file_name='input_files/c7552.txt',
        test_input_file_name='test_input_files/c7552.txt',
        true_value_result_file_name='result_files/true_value_simulation_c7552.txt',
        fault_simulation_result_file_name='result_files/deductive_fault_simulation_c7552.txt'
    ).run()
