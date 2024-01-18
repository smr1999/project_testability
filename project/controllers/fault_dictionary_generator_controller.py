import csv

from io import (
    TextIOWrapper,
)

from project.controllers.controller import (
    Controller,
)


class FaultDictionaryGeneratorController(Controller):
    def __init__(self, detected_fault_dict: dict[str: set[str]], essential_test_vectors: list[str] = None) -> None:
        self.__detected_fault_dict: dict[str: set[str]] = detected_fault_dict
        self.__essential_test_vectors: list[str] = essential_test_vectors

    def __total_fault_names(self) -> set[str]:
        total_fault_names: set[str] = set()

        for _, detected_faults in self.__detected_fault_dict.items():
            total_fault_names = total_fault_names.union(
                detected_faults
            )

        return total_fault_names

    def generate_fault_dictionary_file(self, fault_dictionary_file_object: TextIOWrapper, show_essential_test_vectors: bool = False):
        fault_dictionary_writer = csv.writer(
            fault_dictionary_file_object, lineterminator='\n'
        )
        total_fault_names: list[str] = list(self.__total_fault_names())

        if show_essential_test_vectors:
            fault_dictionary_writer.writerow(
                ['test vector'] + total_fault_names + ['Essential / Not Essential'])
        else:
            fault_dictionary_writer.writerow(
                ['test vector'] + total_fault_names)

        for test_vector, detected_faults in self.__detected_fault_dict.items():
            temp: list[str] = [test_vector]

            for fault_name in total_fault_names:
                if fault_name in detected_faults:
                    temp.append(u'\u2713')
                else:
                    temp.append('')

            if show_essential_test_vectors:
                temp.append(
                    'Essential' if test_vector in self.__essential_test_vectors else 'Not Essential'
                )

            fault_dictionary_writer.writerow(temp)
