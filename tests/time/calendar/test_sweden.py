from supersnabb.time.date import Date
from supersnabb.time.calendar.sweden import Sweden
import QuantLib as ql


def test_swedish_calendar_ql():
    raise NotImplementedError


def test_swedish_calendar():
    assert Sweden().is_holiday(Date(2023, 1, 6)) is True
    assert Sweden().is_holiday(Date(2023, 4, 2)) is True
    assert Sweden().is_holiday(Date(2023, 4, 1)) is True
    assert Sweden().is_holiday(Date(2023, 4, 3)) is False
    assert Sweden().is_holiday(Date(2023, 4, 7)) is True  # Good Friday
    assert Sweden().is_holiday(Date(2023, 4, 10)) is True  # Easter Monday
    assert Sweden().is_holiday(Date(2023, 5, 18)) is True  # Ascension Thursday
    assert Sweden().is_holiday(Date(2023, 5, 18)) is True  # Whit Monday
    assert Sweden().is_holiday(Date(2023, 1, 1)) is True  # New Year's Day
    assert Sweden().is_holiday(Date(2023, 1, 6)) is True  # Epiphany
    assert Sweden().is_holiday(Date(2023, 6, 6)) is True  # National Day
    assert Sweden().is_holiday(Date(2023, 6, 24)) is True  # Midsummer Eve
    assert Sweden().is_holiday(Date(2023, 12, 24)) is True  # Christmas Eve
    assert Sweden().is_holiday(Date(2023, 12, 25)) is True  # Christmas Day
    assert Sweden().is_holiday(Date(2023, 12, 26)) is True  # Boxing Day
    assert Sweden().is_holiday(Date(2023, 12, 31)) is True  # New Year's E
