from project.operations.operation import (
    Operation,
)

from project.enums.logic_value_enum import (
    LogicValueEnum,
)


class LogicOperation(Operation):
    class BasicLogicOperaion(Operation):
        @classmethod
        def not_operation(cls, bit_1: str) -> str:
            if bit_1 == LogicValueEnum.ZERO.value:
                return LogicValueEnum.ONE.value

            if bit_1 == LogicValueEnum.ONE.value:
                return LogicValueEnum.ZERO.value

            if bit_1 == LogicValueEnum.HIGH_IMPEDANCE.value:
                return LogicValueEnum.HIGH_IMPEDANCE.value

            if bit_1 == LogicValueEnum.UNKNOWN.value:
                return LogicValueEnum.UNKNOWN.value

        @classmethod
        def and_operation(cls, bit_1: str, bit_2: str) -> str:
            if bit_1 == LogicValueEnum.ZERO.value:
                return LogicValueEnum.ZERO.value

            if bit_1 == LogicValueEnum.ONE.value:
                return bit_2

            if bit_1 == LogicValueEnum.HIGH_IMPEDANCE.value:
                if bit_2 == LogicValueEnum.ZERO.value:
                    return LogicValueEnum.ZERO.value

                if bit_2 == LogicValueEnum.ONE.value or bit_2 == LogicValueEnum.HIGH_IMPEDANCE.value:
                    return LogicValueEnum.HIGH_IMPEDANCE.value

                return LogicValueEnum.UNKNOWN.value

            if bit_1 == LogicValueEnum.UNKNOWN.value:
                if bit_2 == LogicValueEnum.ZERO.value:
                    return LogicValueEnum.ZERO.value

                return LogicValueEnum.UNKNOWN.value

        @classmethod
        def or_operation(cls, bit_1: str, bit_2: str) -> str:
            if bit_1 == LogicValueEnum.ZERO.value:
                return bit_2

            if bit_1 == LogicValueEnum.ONE.value:
                return LogicValueEnum.ONE.value

            if bit_1 == LogicValueEnum.HIGH_IMPEDANCE.value:
                if bit_2 == LogicValueEnum.ZERO.value or bit_2 == LogicValueEnum.HIGH_IMPEDANCE.value:
                    return LogicValueEnum.HIGH_IMPEDANCE.value

                if bit_2 == LogicValueEnum.ONE.value:
                    return LogicValueEnum.ONE.value

                return LogicValueEnum.UNKNOWN.value

            if bit_1 == LogicValueEnum.UNKNOWN.value:
                if bit_2 == LogicValueEnum.ONE.value:
                    return LogicValueEnum.ONE.value

                return LogicValueEnum.UNKNOWN.value

        @classmethod
        def xor_operation(cls, bit_1: str, bit_2: str) -> str:
            return cls.or_operation(
                bit_1=cls.and_operation(
                    bit_1=cls.not_operation(
                        bit_1=bit_1
                    ),
                    bit_2=bit_2
                ),
                bit_2=cls.and_operation(
                    bit_1=bit_1,
                    bit_2=cls.not_operation(
                        bit_1=bit_2
                    )
                )
            )

    @classmethod
    def input_operation(cls, bits: list[str]) -> str:
        assert len(bits) == 1

        return None

    @classmethod
    def output_operation(cls, bits: list[str]) -> str:
        assert len(bits) == 1

        return bits[0]

    @classmethod
    def buffer_operation(cls, bits: list[str]) -> str:
        assert len(bits) == 1

        return bits[0]

    @classmethod
    def not_operation(cls, bits: list[str]) -> str:
        assert len(bits) == 1

        return cls.BasicLogicOperaion.not_operation(
            bit_1=bits[0]
        )

    @classmethod
    def and_operation(cls, bits: list[str]) -> str:
        assert len(bits) >= 2

        if len(bits) == 2:
            return cls.BasicLogicOperaion.and_operation(
                bit_1=bits[0],
                bit_2=bits[1]
            )

        return cls.BasicLogicOperaion.and_operation(
            bit_1=bits[0],
            bit_2=cls.and_operation(bits=bits[1:])
        )

    @classmethod
    def nand_operation(cls, bits: list[str]) -> str:
        assert len(bits) >= 2

        return cls.BasicLogicOperaion.not_operation(
            bit_1=cls.and_operation(
                bits=bits
            )
        )

    @classmethod
    def or_operation(cls, bits: list[str]) -> str:
        assert len(bits) >= 2

        if len(bits) == 2:
            return cls.BasicLogicOperaion.or_operation(
                bit_1=bits[0],
                bit_2=bits[1]
            )

        return cls.BasicLogicOperaion.or_operation(
            bit_1=bits[0],
            bit_2=cls.or_operation(bits=bits[1:])
        )

    @classmethod
    def nor_operation(cls, bits: list[str]) -> str:
        assert len(bits) >= 2

        return cls.BasicLogicOperaion.not_operation(
            bit_1=cls.or_operation(
                bits=bits
            )
        )

    @classmethod
    def xor_operation(cls, bits: list[str]) -> str:
        assert len(bits) >= 2

        if len(bits) == 2:
            return cls.BasicLogicOperaion.xor_operation(
                bit_1=bits[0],
                bit_2=bits[1]
            )

        return cls.xor_operation(
            bit_1=bits[0],
            bit_2=cls.xor_operation(bits=bits[1:])
        )

    @classmethod
    def xnor_operation(cls, bits: list[str]) -> str:
        assert len(bits) >= 2

        return cls.BasicLogicOperaion.not_operation(
            bit_1=cls.xor_operation(
                bits=bits
            )
        )

    @classmethod
    def fanout_operation(cls, bits: list[str]) -> str:
        assert len(bits) == 1

        return bits[0]
