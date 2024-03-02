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
        settlement_days: int,
        currency: str,
        fixing_calendar: Calendar,
        convention: BusinessDayConvention,
        daycount: Daycounter,
        discount_curve: DiscountCurve,
    ):
        def forecast_fixing(self) -> float:
            pass

        def maturity_date(self) -> Date:
            pass
