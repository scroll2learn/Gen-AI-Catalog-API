from enum import Enum, auto


class DQ_LEVEL(Enum):
    ERROR = auto()
    WARNING = auto()

    def __str__(self):
        return self.name
