from abc import ABCMeta, abstractmethod


class Instrument(ABCMeta):
    @abstractmethod
    def npv(self):
        pass
