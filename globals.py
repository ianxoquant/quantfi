from enum import IntEnum


class OptionType(IntEnum):
    CALL = 1
    FORWARD = 0
    PUT = -1
