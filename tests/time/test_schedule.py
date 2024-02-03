import QuantLib as ql
from supersnabb.time.date import Tenor, Date
from supersnabb.time.schedule import Schedule
from supersnabb.time.calendar.sweden import Sweden
from supersnabb.time.business_day_convention import BusinessDayConvention
from datetime import date
from dateutil.relativedelta import relativedelta


def test_schedule_with_ql():
    num_dates = 10000
    dt = date(2000, 1, 1)
    for idx in range(num_dates):
        dt = dt + relativedelta(days=1)
        ss_dt = Date(dt.year, dt.month, dt.day)
        ql_dt = ql.Date(dt.day, dt.month, dt.year)
        ql_schedule = ql.Schedule(
            ql_dt,
            ql_dt + ql.Period("1Y"),
            ql.Period("3M"),
            ql.Sweden(),
            ql.ModifiedFollowing,
            ql.ModifiedFollowing,
            ql.DateGeneration.Forward,
            False,
        )
        ql_schedule = [date.ISO() for date in ql_schedule]
        ss_schedule = Schedule(
            ss_dt,
            Tenor("1Y") + ss_dt,
            Tenor("3M"),
            Sweden(),
            BusinessDayConvention.MODIFIEDFOLLOWING,
            BusinessDayConvention.MODIFIEDFOLLOWING,
            "forward",
            False,
        )
        ss_schedule = [date.ISO() for date in ss_schedule.dates]
        assert ss_schedule == ql_schedule
