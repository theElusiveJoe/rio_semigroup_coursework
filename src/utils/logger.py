import logging
from logging import StreamHandler
import sys
from enum import IntEnum
from typing import Callable


class LogFlags(IntEnum):
    NO = 0
    BRIEF = 1
    DETAILED = 2
    BRIEF_AND_DET = 3


class _MyLogger:
    l: logging.Logger
    enabled_lvl: LogFlags = LogFlags.BRIEF

    def __init__(self):
        self.l = logging.Logger('my_logger')
        self.l.setLevel(logging.INFO)
        self.l.addHandler(StreamHandler(stream=sys.stdout))

    def log(self, s_func: Callable[[],str], lvl: int, flags: int):
        if self.enabled_lvl & flags:
            s = s_func()
            s = f"{' '*4*(lvl-1)}-> {s}"
            self.l.info(s)


_logger_instance = _MyLogger()


def log(s_func: Callable[[],str], lvl: int = 1, flags: int = LogFlags.DETAILED):
    assert lvl > 0
    _logger_instance.log(s_func, lvl, flags)


def set_log_lvl(flags: LogFlags):
    _logger_instance.enabled_lvl = flags
