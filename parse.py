import grammers
import gates


class Parser:
    def __init__(self, bench_file) -> None:
        self.bench_file = bench_file

    def read_file(self):
        return open(self.bench_file, 'r')

    def __parse_line(self, line):
        if grammers.INPUT.can_parse_next(line, 0):
            return gates.INPUT(grammers.INPUT.parseString(line, parse_all=True)[0])

        elif grammers.OUTPUT.can_parse_next(line, 0):
            return gates.OUTPUT(grammers.OUTPUT.parseString(line, parse_all=True)[0])

        elif grammers.BUFF.can_parse_next(line, 0):
            return gates.BUFF(grammers.BUFF.parseString(line, parse_all=True)[0], grammers.BUFF.parseString(line, parse_all=True)[1:])

        elif grammers.AND.can_parse_next(line, 0):
            return gates.AND(grammers.AND.parseString(line, parse_all=True)[0], grammers.AND.parseString(line, parse_all=True)[1:])

        elif grammers.OR.can_parse_next(line, 0):
            return gates.OR(grammers.OR.parseString(line, parse_all=True)[0], grammers.OR.parseString(line, parse_all=True)[1:])

        elif grammers.XOR.can_parse_next(line, 0):
            return gates.XOR(grammers.XOR.parseString(line, parse_all=True)[0], grammers.XOR.parseString(line, parse_all=True)[1:])

        elif grammers.NOT.can_parse_next(line, 0):
            return gates.NOT(grammers.NOT.parseString(line, parse_all=True)[0], grammers.NOT.parseString(line, parse_all=True)[1:])

        elif grammers.NAND.can_parse_next(line, 0):
            return gates.NAND(grammers.NAND.parseString(line, parse_all=True)[0], grammers.NAND.parseString(line, parse_all=True)[1:])

        elif grammers.NOR.can_parse_next(line, 0):
            return gates.NOR(grammers.NOR.parseString(line, parse_all=True)[0], grammers.NOR.parseString(line, parse_all=True)[1:])

        elif grammers.XNOR.can_parse_next(line, 0):
            return gates.XNOR(grammers.XNOR.parseString(line, parse_all=True)[0], grammers.XNOR.parseString(line, parse_all=True)[1:])

        return  # pattern not found

    def parse_file(self):
        logics = []

        file = self.read_file()

        line = file.readline()
        while line:
            parsed_line = self.__parse_line(line)
            logics.append(parsed_line) if parsed_line else None
            line = file.readline()

        return logics


if __name__ == '__main__':
    filename = './all_benchs/c7552.bench'

    print(Parser(filename).parse_file())
