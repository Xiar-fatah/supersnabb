from supersnabb.time.date import Date
from supersnabb.time.calendars.null_calendar import NullCalendar
from supersnabb.time.business_day_convention import BusinessDayConvention
import QuantLib as ql
from datetime import date
from dateutil.relativedelta import relativedelta


def test_swedish_calendar_ql():
    num_dates = 10000
    dt = date(2000, 1, 1)
    for idx in range(num_dates):
        dt = dt + relativedelta(days=1)
        ql_dt = ql.Date(dt.day, dt.month, dt.year)
        ss_dt = Date(dt.year, dt.month, dt.day)
        ql_null = ql.NullCalendar()
        assert ql.NullCalendar().isBusinessDay(ql_dt) == NullCalendar().is_business_day(
            ss_dt
        )
        assert ql_null.isBusinessDay(ql_dt) == NullCalendar().is_business_day(ss_dt)


jenkins = "2"
