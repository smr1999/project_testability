from project.logic_units.gates.gate import (
    Gate,
)


class AndGate(Gate):
    def _specific_validation(self) -> None:
        assert len(self.input_wires) >= 2
        assert len(self.output_wires) == 1
