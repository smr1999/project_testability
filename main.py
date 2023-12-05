from project.controllers.main_controller import (
    MainController,
)


if __name__ == '__main__':
    test_names: list[str] = ['c17', 'c432', 'c499', 'c880',
                             'c1355', 'c1908', 'c2670', 'c3540', 'c5315', 'c6288', 'c7552']

    for test_name in ['test']:
        print(f'Testing {test_name}')
        main_controller: MainController = MainController(
            bench_file_name=f'bench_files/{test_name}.bench',
            fault_dictionary_file_name=f'result_files/fault_dictionary_{test_name}'
        )
        main_controller.run()

        del main_controller
