from supersnabb.time.date import Date
from supersnabb.time.calendar import Calendar
from supersnabb.time.daycounter import Daycounter
from supersnabb.termstructure.interpolation import InterpolationType, Interpolation
from typing import List
import pandas as pd


class ForwardCurve(Interpolation):
    pass


class DiscountCurve(Interpolation):
    def __init__(
        self,
        dates: List[Date],
        rates: List[float],
        daycount: Daycounter,
        calendar: Calendar,
        interpolation: InterpolationType = InterpolationType.LINEAR,
    ):
        super().__init__(
            dates=dates, rates=rates, daycount=daycount, interpolation=interpolation
        )
        self.dates = dates
        self.rates = rates
        self.daycount = daycount
        self.calendar = calendar

    def interpolate(self, date: Date) -> float:
        return super().interpolate(date)

    @property
    def curve(self):
        return pd.DataFrame({"dates": self.dates, "rates": self.rates}).set_index(
            "dates"
        )

    def __call__(self, date: Date) -> float:
        return self.interpolate(date)


class Curve:
    pass
