from abc import ABCMeta, abstractmethod


class InterestRateIndex(metaclass=ABCMeta):
    @abstractmethod
    def forecast_fixing(self):
        pass

    @abstractmethod
    def maturity_date(self):
        pass
