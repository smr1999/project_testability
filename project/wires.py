from project.enums import (
    LogicValue,
)


class Wire:
    def __init__(self, input_gate, output_gate) -> None:
        self.__id = input_gate.id + '__' + output_gate.id
        self.__value: str = LogicValue.UNKNOWN.value
        self.__has_set_value: bool = False

        self.__input_gate = input_gate
        self.__output_gate = output_gate

    def update_id(self) -> None:
        assert self.input_gate and self.output_gate

        self.id = self.input_gate.id + '__' + self.output_gate.id

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id_: str) -> None:
        self.__id = id_

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value_: str) -> None:
        assert self.value in LogicValue.list_values()

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
    def input_gate(self, input_gate_):
        self.__input_gate = input_gate_
        self.update_id()

    @property
    def output_gate(self):
        return self.__output_gate

    @output_gate.setter
    def set_output_gate(self, output_gate_=None):
        self.__output_gate = output_gate_
        self.update_id()

    @property
    def gates(self):
        return (
            self.input_gate,
            self.output_gate
        )
