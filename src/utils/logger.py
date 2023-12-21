import logging
from logging import StreamHandler
import sys


class _MyLogger:
    l: logging.Logger
    h: StreamHandler

    def __init__(self):
        self.l = my_logger = logging.Logger('my_logger')
        self.l.setLevel(logging.INFO)
        self.h = StreamHandler(stream=sys.stdout)

    def log(self, s: str):
        self.l.info(s)

    def enable(self):
        self.l.addHandler(self.h)

    def disable(self):
        self.l.removeHandler(self.h)


_logger_instance = _MyLogger()


def log(s: str, lvl=1):
    assert lvl > 0
    s = f"{' '*4*(lvl-1)}-> {s}"
    _logger_instance.log(s)


def enable_logging():
    _logger_instance.enable()


def disable_logging():
    _logger_instance.disable()
