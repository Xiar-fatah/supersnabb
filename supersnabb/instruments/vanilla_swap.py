from supersnabb.instruments.swap import Swap
from supersnabb.time.schedule import Schedule
from typing import Callable


class VanillaSwap(Swap):
    def __init__(
        self,
        type: str,
        schedule: Schedule,
        fixed_rate: float,
        fixed_daycount: Callable,
        ibor_index: Callable,
        spread: float,
        float_daycount: Callable,
        payment_convention: str,
        useIndexedCoupons: bool,
    ):

        pass
