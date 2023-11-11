import pyparsing as pp

IDGrammer = pp.Word(pp.nums)


@IDGrammer.set_parse_action
def set_ID_action(results: pp.ParseResults):
    return results[0]


IDsGrammer = IDGrammer + pp.OneOrMore(pp.Suppress(',') + IDGrammer)

InputGrammer = pp.Suppress(
    'INPUT') + pp.Suppress('(') + IDGrammer + pp.Suppress(')')

OutputGrammer = pp.Suppress(
    'OUTPUT') + pp.Suppress('(') + IDGrammer + pp.Suppress(')')

BufferGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('BUFF') + \
    pp.Suppress('(') + IDGrammer + pp.Suppress(')')

NotGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('NOT') + \
    pp.Suppress('(') + IDGrammer + pp.Suppress(')')

AndGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('AND') + \
    pp.Suppress('(') + IDsGrammer + pp.Suppress(')')

NandGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('NAND') + \
    pp.Suppress('(') + IDsGrammer + pp.Suppress(')')

OrGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('OR') + \
    pp.Suppress('(') + IDsGrammer + pp.Suppress(')')

NorGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('NOR') + \
    pp.Suppress('(') + IDsGrammer + pp.Suppress(')')

XorGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('XOR') + \
    pp.Suppress('(') + IDsGrammer + pp.Suppress(')')

XnorGrammer = IDGrammer + pp.Suppress('=') + pp.Suppress('XNOR') + \
    pp.Suppress('(') + IDsGrammer + pp.Suppress(')')
