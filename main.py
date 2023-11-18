from project.controllers.main_controller import (
    MainController,
)


if __name__ == '__main__':
    test_names: list[str] = ['c17', 'c432', 'c499', 'c880',
                             'c1355', 'c1908', 'c2670', 'c3540', 'c5315', 'c6288', 'c7552']

    for test_name in test_names:
        print(f'Testing {test_name}')
        main_controller: MainController = MainController(
            bench_file_name=f'bench_files/{test_name}.bench',
            input_file_name=f'input_files/{test_name}.txt',
            test_input_file_name=f'test_input_files/{test_name}.txt',
            true_value_result_file_name=f'result_files/true_value_simulation_{test_name}.txt',
            fault_simulation_result_file_name=f'result_files/deductive_fault_simulation_{test_name}.txt'
        ).run()

        del main_controller
