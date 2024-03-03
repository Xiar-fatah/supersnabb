from supersnabb.indices.interest_rate_index import InterestRateIndex
from supersnabb.time.date import Tenor, Date
from supersnabb.time.calendar import Calendar
from supersnabb.time.business_day_convention import BusinessDayConvention
from supersnabb.time.daycounter import Daycounter
from supersnabb.termstructure.curve import DiscountCurve


class IborIndex(InterestRateIndex):
    def __init__(
        self,
        tenor: Tenor,
        settlement_days: Tenor,
        currency: str,
        fixing_calendar: Calendar,
        convention: BusinessDayConvention,
        daycount: Daycounter,
        discount_curve: DiscountCurve,
    ):
        self.tenor = tenor
        self.settlement_days = settlement_days
        self.currency = currency
        self.fixing_calendar = fixing_calendar
        self.convention = convention
        self.daycount = daycount
        self.discount_curve = discount_curve

    def forecast_fixing_with_dates(self, d1: Date, d2: Date) -> float:
        t = self.daycount.year_fraction(d1, d2)
        df1 = self.discount_curve(d1)
        df2 = self.discount_curve(d2)
        return (df1 / df2 - 1) / t

    def maturity_date(self, date: Date) -> Date:
        return self.fixing_calendar.advance(date, self.tenor, self.convention)

    def value_date(self, date: Date) -> Date:
        return self.fixing_calendar.advance(
            self.maturity_date(date), self.settlement_days, self.convention
        )

    def fixing_date(self, date: Date) -> Date:
        return self.fixing_calendar.advance(
            date, -self.settlement_days, self.convention
        )

    def forecast_fixing(self):
        pass
