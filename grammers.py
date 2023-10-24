import pyparsing as pp

ID = pp.Word(pp.nums)


@ID.set_parse_action
def set_ID_action(results: pp.ParseResults):
    return int(results[0])


IDS = ID + pp.OneOrMore(pp.Suppress(',') + ID)

INPUT = pp.Suppress('INPUT') + pp.Suppress('(') + ID + pp.Suppress(')')
OUTPUT = pp.Suppress('OUTPUT') + pp.Suppress('(') + ID + pp.Suppress(')')

NOT = ID + pp.Suppress('=') + pp.Suppress('NOT') + \
    pp.Suppress('(') + ID + pp.Suppress(')')
BUFF = ID + pp.Suppress('=') + pp.Suppress('BUFF') + \
    pp.Suppress('(') + ID + pp.Suppress(')')

AND = ID + pp.Suppress('=') + pp.Suppress('AND') + \
    pp.Suppress('(') + IDS + pp.Suppress(')')
OR = ID + pp.Suppress('=') + pp.Suppress('OR') + \
    pp.Suppress('(') + IDS + pp.Suppress(')')
XOR = ID + pp.Suppress('=') + pp.Suppress('XOR') + \
    pp.Suppress('(') + IDS + pp.Suppress(')')
NAND = ID + pp.Suppress('=') + pp.Suppress('NAND') + \
    pp.Suppress('(') + IDS + pp.Suppress(')')
NOR = ID + pp.Suppress('=') + pp.Suppress('NOR') + \
    pp.Suppress('(') + IDS + pp.Suppress(')')
XNOR = ID + pp.Suppress('=') + pp.Suppress('XNOR') + \
    pp.Suppress('(') + IDS + pp.Suppress(')')
