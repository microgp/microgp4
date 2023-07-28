__all__ = ["FitnessLog"]

from pprint import pformat
from datetime import datetime


class FitnessLog:
    def __init__(self, backend: str):
        if backend == "list":
            self._log = list()
        else:
            raise NotImplementedError

    def __iadd__(self, value):
        self._log.append((datetime.now(), value))

    def __str__(self):
        return "[" + ",\n ".join(f"({d}, {v})" for d, v in self._log) + "]"
