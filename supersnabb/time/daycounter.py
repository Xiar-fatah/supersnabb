from abc import ABCMeta, abstractmethod
from supersnabb.time.date import Date


class Daycounter(metaclass=ABCMeta):
    @abstractmethod
    def year_fraction(self, d1: Date, d2: Date) -> float:
        pass

    @abstractmethod
    def day_count(self, d1: Date, d2: Date) -> int:
        return d2.serial_number - d1.serial_number
