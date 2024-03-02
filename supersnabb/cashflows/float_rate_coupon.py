import pandas as pd
from supersnabb.cashflows.coupon import Coupon
from supersnabb.time.schedule import Schedule
from supersnabb.time.daycounter import Daycounter
from supersnabb.time.business_day_convention import BusinessDayConvention
from supersnabb.time.calendar import Calendar
from supersnabb.time.date import Tenor, Date
from supersnabb.termstructure.curve import DiscountCurve, ForwardCurve
from typing import Optional


class FloatRateCoupon(Coupon):
    pass


class FloatRateLeg:
    def __init__(
        self,
        float_schedule: Schedule,
        nominal: int,
        float_rate: float,
        float_daycount: Daycounter,
        float_convention: BusinessDayConvention,
        calendar: Calendar,
        discount_curve: DiscountCurve,
        forward_curve: ForwardCurve,
        payment_lag: Optional[Tenor] = Tenor("0D"),
    ):
        pass
