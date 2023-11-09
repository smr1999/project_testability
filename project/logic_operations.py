from project.enums import OperationType, LogicValue


class LogicOperation:
    def __init__(self, input_items: list[str], operation_type: OperationType) -> None:
        self.input_items = input_items
        self.operation_type = operation_type

    def __validate_inputs(self, input_items) -> None:
        for input_item in input_items:
            assert input_item in LogicValue.list_values()

    def operate(self):
        self.__validate_inputs(
            input_items=self.input_items
        )

        if self.operation_type == OperationType.Input:
            return self.__input_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Output:
            return self.__output_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Buffer:
            return self.__buffer_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Not:
            return self.__not_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.And:
            return self.__and_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Nand:
            return self.__nand_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Or:
            return self.__or_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Nor:
            return self.__nor_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Xor:
            return self.__xor_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Xnor:
            return self.__xnor_operation(
                input_items=self.input_items
            )

        if self.operation_type == OperationType.Fanout:
            return self.__fanout_operation(
                input_items=self.input_items
            )

    def __input_operation(self, input_items) -> str:
        return None

    def __output_operation(self, input_items) -> str:
        assert len(input_items) == 1

        return input_items[0]


    def __basic_buff_operation(self, input_item_1) -> str:
        return input_item_1

    def __buffer_operation(self, input_items) -> str:
        assert len(input_items) == 1

        return self.__basic_buff_operation(
            input_item_1=input_items[0]
        )

    def __basic_not_operation(self, input_item_1) -> str:
        if input_item_1 == LogicValue.ZERO.value:
            return LogicValue.ONE.value

        if input_item_1 == LogicValue.ONE.value:
            return LogicValue.ZERO.value

        if input_item_1 == LogicValue.HIGH_IMPEDANCE.value:
            return LogicValue.HIGH_IMPEDANCE.value

        if input_item_1 == LogicValue.UNKNOWN.value:
            return LogicValue.UNKNOWN.value

    def __not_operation(self, input_items) -> str:
        assert len(input_items) == 1

        return self.__basic_not_operation(
            input_item_1=input_items[0]
        )

    def __basic_and_operation(self, input_item_1, input_item_2) -> str:
        if input_item_1 == LogicValue.ZERO.value:
            return LogicValue.ZERO.value

        if input_item_1 == LogicValue.ONE.value:
            return input_item_2

        if input_item_1 == LogicValue.HIGH_IMPEDANCE.value:
            if input_item_2 == LogicValue.ZERO.value:
                return LogicValue.ZERO.value

            if input_item_2 == LogicValue.ONE.value or input_item_2 == LogicValue.HIGH_IMPEDANCE.value:
                return LogicValue.HIGH_IMPEDANCE.value

            return LogicValue.UNKNOWN.value

        if input_item_1 == LogicValue.UNKNOWN.value:
            if input_item_2 == LogicValue.ZERO.value:
                return LogicValue.ZERO.value

            return LogicValue.UNKNOWN.value

    def __and_operation(self, input_items) -> str:
        assert len(input_items) >= 2

        if len(input_items) == 2:
            return self.__basic_and_operation(
                input_item_1=input_items[0],
                input_item_2=input_items[1]
            )

        return self.__and_operation(
            input_items=[
                input_items[0],
                self.__and_operation(input_items[1:])
            ]
        )

    def __nand_operation(self, input_items) -> str:
        assert len(input_items) >= 2

        and_result = self.__and_operation(
            input_items=input_items
        )

        return self.__basic_not_operation(
            input_item_1=and_result
        )

    def __basic_or_operation(self, input_item_1, input_item_2) -> str:
        if input_item_1 == LogicValue.ZERO.value:
            return input_item_2

        if input_item_1 == LogicValue.ONE.value:
            return LogicValue.ONE.value

        if input_item_1 == LogicValue.HIGH_IMPEDANCE.value:
            if input_item_2 == LogicValue.ZERO.value or input_item_2 == LogicValue.HIGH_IMPEDANCE.value:
                return LogicValue.HIGH_IMPEDANCE.value

            if input_item_2 == LogicValue.ONE.value:
                return LogicValue.ONE.value

            return LogicValue.UNKNOWN.value

        if input_item_1 == LogicValue.UNKNOWN.value:
            if input_item_2 == LogicValue.ONE.value:
                return LogicValue.ONE.value

            return LogicValue.UNKNOWN.value

    def __or_operation(self, input_items) -> str:
        assert len(input_items) >= 2

        if len(input_items) == 2:
            return self.__basic_or_operation(
                input_item_1=input_items[0],
                input_item_2=input_items[1]
            )

        return self.__or_operation(
            input_items=[
                input_items[0],
                self.__or_operation(input_items[1:])
            ]
        )

    def __nor_operation(self, input_items) -> str:
        assert len(input_items) >= 2

        or_result = self.__or_operation(
            input_items=input_items
        )

        return self.__basic_not_operation(
            input_item_1=or_result
        )

    def __basic_xor_operation(self, input_item_1, input_item_2) -> str:
        return self.__basic_or_operation(
            input_item_1=self.__basic_and_operation(
                input_item_1=self.__basic_not_operation(
                    input_item_1=input_item_1
                ),
                input_item_2=input_item_2
            ),
            input_item_2=self.__basic_and_operation(
                input_item_1=input_item_1,
                input_item_2=self.__basic_not_operation(
                    input_item_1=input_item_2
                )
            )
        )

    def __xor_operation(self, input_items) -> str:
        assert len(input_items) >= 2

        if len(input_items) == 2:
            return self.__basic_xor_operation(
                input_item_1=input_items[0],
                input_item_2=input_items[1]
            )

        return self.__xor_operation(
            input_items=[
                input_items[0],
                self.__xor_operation(input_items[1:])
            ]
        )

    def __xnor_operation(self, input_items) -> str:
        assert len(input_items) >= 2

        xor_result = self.__xor_operation(
            input_items=input_items
        )

        return self.__basic_not_operation(
            input_item_1=xor_result
        )

    def __fanout_operation(self, input_items) -> str:
        assert len(input_items) == 1

        return input_items[0]
