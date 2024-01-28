from supersnabb.time.date import Date
from supersnabb.time.calendar.null_calendar import NullCalendar
import QuantLib as ql
from datetime import date
from dateutil.relativedelta import relativedelta


def test_swedish_calendar_ql():
    num_dates = 10000
    dt = date(2000, 1, 1)
    for idx in range(num_dates):
        dt = dt + relativedelta(days=1)
        ql_dt = ql.Date(dt.day, dt.month, dt.year)
        ql_ss = Date(dt.year, dt.month, dt.day)
        assert ql.NullCalendar().isBusinessDay(ql_dt) == NullCalendar().is_business_day(
            ql_ss
        )
