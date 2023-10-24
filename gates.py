class LOGIC:
    def __init__(self, id) -> None:
        self.id = id
        self.value = 'X'

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class INPUT(LOGIC):
    def __init__(self, id) -> None:
        super().__init__(id)

    def __repr__(self) -> str:
        return f'<INPUT {self.id}: {self.get_value()}>'


class OUTPUT(LOGIC):
    def __init__(self, id) -> None:
        super().__init__(id)

    def __repr__(self) -> str:
        return f'<OUTPUT {self.id}: {self.get_value()}>'


class GATE(LOGIC):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id)
        self.inputs = self.init_inputs(
            input_ids=input_ids
        )

    def init_inputs(self, input_ids):
        inputs = dict()
        for input_id in input_ids:
            inputs[input_id] = 'X'

        return inputs

    def set_input_value(self, input_id, value):
        self.inputs[input_id] = value

    def operate(self):
        pass


class BUFF(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<BUFF {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class AND(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<AND {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class OR(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<OR {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class XOR(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<XOR {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class NOT(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<NOT {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class NAND(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<NAND {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class NOR(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<NOR {self.id}: {self.get_value()}, inputs: ({self.inputs})>'


class XNOR(GATE):
    def __init__(self, id, input_ids: list) -> None:
        super().__init__(id, input_ids)

    def operate(self):
        pass

    def __repr__(self) -> str:
        return f'<XNOR {self.id}: {self.get_value()}, inputs: ({self.inputs})>'
