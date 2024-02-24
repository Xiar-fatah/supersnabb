from supersnabb.instruments.swap import Swap
from supersnabb.time.schedule import Schedule
from supersnabb.cashflows.fixed_rate_coupon import FixedRateLeg
from typing import Callable


class VanillaSwap(Swap):
    def __init__(
        self,
        type: str,
        nominal: int,
        schedule: Schedule,
        fixed_rate: float,
        fixed_daycount: Callable,
        ibor_index: Callable,
        spread: float,
        float_daycount: Callable,
        payment_convention: str,
        useIndexedCoupons: bool,
    ):

        self.legs = []
        self.legs[0] = FixedRateLeg(
            fixed_schedule=schedule,
            nominal=nominal,
            fixed_rate=fixed_rate,
            fixed_daycount=fixed_daycount,
            fixed_convention=payment_convention,
        )
