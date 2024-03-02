from abc import ABCMeta, abstractmethod


class InterestRateIndex(meta=ABCMeta):
    @abstractmethod
    def forecast_fixing(self):
        pass

    @abstractmethod
    def maturity_date(self):
        pass
