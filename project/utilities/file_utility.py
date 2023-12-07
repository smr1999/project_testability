from io import (
    TextIOWrapper,
)

from project.utilities.utility import (
    Utility,
)


class FileUtility(Utility):
    @classmethod
    def write_file(cls, file_dir: str) -> TextIOWrapper:
        return open(
            file=file_dir,
            mode='w'
        )

    @classmethod
    def read_file(cls, file_dir: str) -> TextIOWrapper:
        return open(
            file=file_dir,
            mode='r'
        )
