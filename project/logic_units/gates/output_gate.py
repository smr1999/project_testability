from project.logic_units.gates.gate import (
    Gate,
)


class OutputGate(Gate):
    def _specific_validation(self) -> None:
        assert len(self.input_wires) == 1
        assert len(self.output_wires) == 0
