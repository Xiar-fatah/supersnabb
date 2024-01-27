from abc import ABCMeta, abstractmethod


class Calendar(metaclass=ABCMeta):
    @abstractmethod
    def is_holiday(self):
        pass
