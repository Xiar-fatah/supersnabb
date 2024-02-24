from abc import abstractmethod, ABCMeta


class Coupon(metaclass=ABCMeta):
    @property
    @abstractmethod
    def discount_factor(self):
        pass

    @property
    @abstractmethod
    def coupon(self):
        pass

    @property
    @abstractmethod
    def accrual(self):
        pass
