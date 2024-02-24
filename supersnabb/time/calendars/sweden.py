from supersnabb.time.calendar import Calendar
from supersnabb.time.date import Date


class Sweden(Calendar):
    """
    Returns true if input is a business day in Sweden else false.
    """

    def __init__(self):
        pass

    def is_business_day(self, dt: Date):
        if not isinstance(dt, Date):
            raise TypeError(f"dt must be a Date object, received: {dt}")
        w = dt.weekday()
        d = dt.day_of_month()  # dayOfMonth
        dd = dt.day_of_year()
        m = dt.month()
        y = dt.year()
        easter_monday = dt.easter_monday()
        if (
            dt.is_week()
            # Good Friday
            | (dd == (easter_monday - 3))
            # Easter Monday
            | (dd == easter_monday)
            # Ascension Thursday
            | (dd == easter_monday + 38)
            # Whit Monday (till 2004)
            | ((dd == (easter_monday + 49)) & (y < 2005))
            # New Year's Day
            | ((d == 1) & (m == 1))
            # Epiphany
            | ((d == 6) & (m == 1))
            # May Day
            | ((d == 1) & (m == 5))
            # National Day
            # Only a holiday since 2005
            | ((d == 6) & (m == 6) & (y >= 2005))
            # Midsummer Eve (Friday between June 19-25)
            | ((w == 4) & (d >= 19) & (d <= 25) & (m == 6))
            # Christmas Eve
            | ((d == 24) & (m == 12))
            # Christmas Day
            | ((d == 25) & (m == 12))
            # Boxing Day
            | ((d == 26) & (m == 12))
            # New Year's Eve
            | ((d == 31) & (m == 12))
        ):
            return False
        else:
            return True
