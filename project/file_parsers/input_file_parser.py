from project.file_parsers.file_parser import (
    FileParser,
)


class InputFileParser(FileParser):
    @classmethod
    def fetch_list_from_line(cls, line: str) -> list:
        return line.strip().split(' ')
