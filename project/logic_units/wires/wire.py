from project.enums.logic_value_enum import (
    LogicValueEnum,
)


class Wire:
    def __init__(self, input_gate, output_gate) -> None:
        self.__value: str = LogicValueEnum.UNKNOWN.value
        self.__has_set_value: bool = False

        assert input_gate and output_gate
        self.__input_gate = input_gate
        self.__output_gate = output_gate

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
    def input_gate(self):
        return self.__input_gate

    @input_gate.setter
    def input_gate(self, input_gate_) -> None:
        assert input_gate_

        self.__input_gate = input_gate_

    @property
    def output_gate(self):
        return self.__output_gate

    @output_gate.setter
    def set_output_gate(self, output_gate_) -> None:
        assert output_gate_

        self.__output_gate = output_gate_

    @property
    def gates(self):
        return (
            self.input_gate,
            self.output_gate
        )

    def __repr__(self) -> str:
        return f'<{self.input_gate.__class__.__name__}_{self.input_gate.id}__{self.__class__.__name__}__{self.output_gate.__class__.__name__}_{self.output_gate.id}:{self.value}>'
