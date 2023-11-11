from io import (
    TextIOWrapper,
)

from project.controllers.controller import (
    Controller,
)

from project.file_parsers.input_file_parser import (
    InputFileParser,
)

from project.enums.logic_value_enum import (
    LogicValueEnum,
)


class InputController(Controller):
    def __init__(self, input_file_object: TextIOWrapper) -> None:
        self.__input_file_object: TextIOWrapper = input_file_object

        self.__inputs: dict[str: str] = {}

    @property
    def input_file_object(self) -> TextIOWrapper:
        return self.__input_file_object

    @property
    def inputs(self) -> dict[str: str]:
        return self.__inputs

    @inputs.setter
    def inputs(self, inputs_: dict[str: str]) -> None:
        self.__inputs = inputs_

    def __update_inputs(self) -> None:
        lines = self.input_file_object.readlines()
        assert len(lines) == 2

        ids: list[str] = InputFileParser.fetch_list_from_line(lines[0])
        values: list[str] = InputFileParser.fetch_list_from_line(lines[1])

        assert len(ids) == len(values)

        self.inputs = dict(zip(ids, values))

    def __validate_inputs(self) -> None:
        for _, value in self.inputs.items():
            assert value in LogicValueEnum.list_values()

    def run(self) -> None:
        self.__update_inputs()
        self.__validate_inputs()
