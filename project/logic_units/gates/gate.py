from project.controllers.logic_operation_controller import (
    LogicOperationController,
)
from project.enums.operation_type_enum import (
    OperationTypeEnum,
)

from project.enums.logic_value_enum import (
    LogicValueEnum,
)


from project.logic_units.wires.wire import (
    Wire,
)


class Gate:
    def __init__(self, id: str) -> None:
        self.__id: str = id
        self.__value: str = LogicValueEnum.UNKNOWN.value
        self.__has_set_value: bool = False
        self.__level: int = -1

        self.__input_wires: list[Wire] = []
        self.__output_wires: list[Wire] = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value_: str) -> None:
        assert value_ in LogicValueEnum.list_values()

        self.__value = value_
        self.has_set_value = True

    @property
    def has_set_value(self) -> bool:
        return self.__has_set_value

    @has_set_value.setter
    def has_set_value(self, has_set_value_: bool) -> None:
        self.__has_set_value = has_set_value_

    @property
    def level(self) -> int:
        return self.__level

    @level.setter
    def level(self, level_: int) -> None:
        assert level_ >= 0

        self.__level = level_

    @property
    def input_wires(self) -> list[Wire]:
        return self.__input_wires

    @input_wires.setter
    def output_wires(self, input_wires_: list[Wire]) -> None:
        self.__input_wires = input_wires_

    def add_input_wire(self, input_wire_: Wire) -> None:
        assert input_wire_.output_gate == self
        assert input_wire_ not in self.input_wires

        self.input_wires.append(input_wire_)

    @property
    def __input_wires_values(self) -> list[str]:
        return [
            input_wire.value for input_wire in self.input_wires
        ]

    @property
    def output_wires(self) -> list[Wire]:
        return self.__output_wires

    @output_wires.setter
    def output_wires(self, output_wires_: list[Wire]) -> None:
        self.__output_wires = output_wires_

    def add_output_wire(self, output_wire_: Wire) -> None:
        assert output_wire_.input_gate == self
        assert output_wire_ not in self.output_wires

        self.output_wires.append(output_wire_)

    @property
    def __output_wires_values(self) -> list[str]:
        return [
            output_wire.value for output_wire in self.output_wires
        ]

    def _specific_validation(self) -> None:
        pass

    def __validate_before_operation(self) -> None:
        assert self.has_set_value == False

        for input_wire in self.input_wires:
            assert input_wire.has_set_value == True

        for output_wire in self.output_wires:
            assert output_wire.has_set_value == False

    def __propagate_to_output_wires(self) -> None:
        assert self.has_set_value == True

        for output_wire in self.output_wires:
            output_wire.value = self.value

    def __validate_after_operation(self) -> None:
        assert self.has_set_value == True

        for output_wire in self.output_wires:
            assert output_wire.has_set_value == True

    def set_value_and_propagate(self, value_: str = None) -> None:
        self._specific_validation()

        self.__validate_before_operation()

        if value_:
            assert value_ in LogicValueEnum.list_values()

            self.value = value_
        else:
            operation_type = OperationTypeEnum[self.__class__.__name__.replace(
                'Gate', '')]

            self.value = LogicOperationController(
                input_vector=self.__input_wires_values,
                operation_type=operation_type
            ).run()

        self.__propagate_to_output_wires()

        self.__validate_after_operation()

    def reset(self) -> None:
        self.value = LogicValueEnum.UNKNOWN.value
        self.has_set_value = False

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}_{self.id}:{self.value}, level:{self.level}, input_wires: ({[input_wire for input_wire in self.input_wires]}), output_wires:({[output_wire for output_wire in self.output_wires]})>'
