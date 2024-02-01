from supersnabb.time.date import Date
from supersnabb.time.calendar.sweden import Sweden
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
        ql_sweden = ql.Sweden()
        assert ql_sweden.isBusinessDay(ql_dt) == Sweden().is_business_day(ss_dt)
        assert (
            ql_sweden.adjust(ql_dt, ql.Following).ISO()
            == Sweden().adjust(ss_dt, BusinessDayConvention.FOLLOWING).ISO()
        )
        assert (
            ql_sweden.adjust(ql_dt, ql.ModifiedFollowing).ISO()
            == Sweden().adjust(ss_dt, BusinessDayConvention.MODIFIEDFOLLOWING).ISO()
        )
        assert (
            ql_sweden.adjust(ql_dt, ql.Preceding).ISO()
            == Sweden().adjust(ss_dt, BusinessDayConvention.PRECEDING).ISO()
        )
        assert (
            ql_sweden.adjust(ql_dt, ql.ModifiedPreceding).ISO()
            == Sweden().adjust(ss_dt, BusinessDayConvention.MODIFIEDPRECEDING).ISO()
        )
        assert (
            ql_sweden.adjust(ql_dt, ql.Nearest).ISO()
            == Sweden().adjust(ss_dt, BusinessDayConvention.NEAREST).ISO()
        )
        assert (
            ql_sweden.adjust(ql_dt, ql.Unadjusted).ISO()
            == Sweden().adjust(ss_dt, BusinessDayConvention.UNADJUSTED).ISO()
        )


def test_swedish_calendar():
    assert Sweden().is_business_day(Date(2023, 1, 6)) is False
    assert Sweden().is_business_day(Date(2023, 4, 2)) is False
    assert Sweden().is_business_day(Date(2023, 4, 1)) is False

    assert Sweden().is_business_day(Date(2023, 4, 3)) is True

    assert Sweden().is_business_day(Date(2023, 4, 7)) is False  # Good Friday
    assert Sweden().is_business_day(Date(2023, 4, 10)) is False  # Easter Monday
    assert Sweden().is_business_day(Date(2023, 5, 18)) is False  # Ascension Thursday
    assert Sweden().is_business_day(Date(2023, 5, 18)) is False  # Whit Monday
    assert Sweden().is_business_day(Date(2023, 1, 1)) is False  # New Year's Day
    assert Sweden().is_business_day(Date(2023, 1, 6)) is False  # Epiphany
    assert Sweden().is_business_day(Date(2023, 6, 6)) is False  # National Day
    assert Sweden().is_business_day(Date(2023, 6, 23)) is False  # Midsummer Eve
    assert Sweden().is_business_day(Date(2023, 12, 24)) is False  # Christmas Eve
    assert Sweden().is_business_day(Date(2023, 12, 25)) is False  # Christmas Day
    assert Sweden().is_business_day(Date(2023, 12, 26)) is False  # Boxing Day
    assert Sweden().is_business_day(Date(2023, 12, 31)) is False  # New Year's E
