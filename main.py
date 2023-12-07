from project.controllers.main_controller import (
    MainController,
)


if __name__ == '__main__':
    test_names: list[str] = ['c17', 'sample1', 'sample2']

    for test_name in test_names:
        print(f'Testing {test_name}')
        main_controller: MainController = MainController(
            bench_file_name=f'my_bench_files/{test_name}.bench',
            fault_dictionary_file_name=f'result_files/fault_dictionary_{test_name}'
        )
        main_controller.run()

        del main_controller
