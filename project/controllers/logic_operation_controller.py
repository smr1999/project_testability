from project.controllers.controller import (
    Controller,
)

from project.operations.logic_operation import (
    LogicOperation,
)

from project.enums.operation_type_enum import (
    OperationTypeEnum,
)

from project.enums.logic_value_enum import (
    LogicValueEnum,
)


class LogicOperationController(Controller):
    def __init__(self, input_vector: list[str], operation_type: OperationTypeEnum = OperationTypeEnum.Unknown) -> None:
        self.__input_vector: list[str] = input_vector
        self.__operation_type: OperationTypeEnum = operation_type

    @property
    def input_vector(self) -> list[str]:
        return self.__input_vector

    @property
    def operation_type(self) -> OperationTypeEnum:
        return self.__operation_type

    def __validate_input_vector(self) -> None:
        for input_item in self.input_vector:
            assert input_item in LogicValueEnum.list_values()

    def run(self) -> str:
        self.__validate_input_vector()

        if self.operation_type == OperationTypeEnum.Input:
            return LogicOperation.input_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Output:
            return LogicOperation.output_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Buffer:
            return LogicOperation.buffer_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Not:
            return LogicOperation.not_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.And:
            return LogicOperation.and_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Nand:
            return LogicOperation.nand_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Or:
            return LogicOperation.or_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Nor:
            return LogicOperation.nor_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Xor:
            return LogicOperation.xor_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Xnor:
            return LogicOperation.xnor_operation(
                bits=self.input_vector
            )

        if self.operation_type == OperationTypeEnum.Fanout:
            return LogicOperation.fanout_operation(
                bits=self.input_vector
            )

        assert False
