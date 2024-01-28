from abc import ABCMeta, abstractmethod
from supersnabb.time.date import Date


class Calendar(metaclass=ABCMeta):
    @abstractmethod
    def is_business_day(self, dt: Date):
        pass
