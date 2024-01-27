from calendar import Calendar
from supersnabb.time.date import Date
from dateutil import easter  # Only needed for Easter Monday


class Sweden(Calendar):
    """
    Returns true if input is a business day in Sweden else false.
    """

    def is_holiday(self, dt: Date):
        if not isinstance(dt, Date):
            raise TypeError(f"dt must be a Date object, received: {dt}")

        easter_monday = Date._calc_day_of_year(
            easter.easter(dt._year(dt), 3) + dt.timedelta(1)
        )
        if (
            dt._is_weekend(dt)
            # Good Friday
            | (dt._day_of_year(dt) == easter_monday - 3)
            # Easter Monday
            | (dt._day_of_year(dt) == easter_monday)
            # Ascension Thursday
            | (dt._day_of_year(dt) == easter_monday + 38)
            # Whit Monday (till 2004)
            | ((dt._day_of_year(dt) == easter_monday + 49) & (dt._year(dt) < 2005))
            # New Year's Day
            | ((dt._day_of_month(dt) == 1) & (dt._month(dt) == 1))
            # Epiphany
            | ((dt._day_of_month(dt) == 6) & (dt._month(dt) == 1))
            # May Day
            | ((dt._day_of_month(dt) == 1) & (dt._month(dt) == 5))
            # National Day
            # Only a holiday since 2005
            | (
                (dt._day_of_month(dt) == 6)
                & (dt._month(dt) == 6)
                & (dt._year(dt) >= 2005)
            )
            # Midsummer Eve (Friday between June 19-25)
            | (
                (dt._week_day(dt) == 4)
                & (dt._day_of_month(dt) >= 19)
                & (dt._day_of_month(dt) <= 25)
                & (dt._month(dt) == 6)
            )
            # Christmas Eve
            | ((dt._day_of_month(dt) == 24) & (dt._month(dt) == 12))
            # Christmas Day
            | ((dt._day_of_month(dt) == 25) & (dt._month(dt) == 12))
            # Boxing Day
            | ((dt._day_of_month(dt) == 26) & (dt._month(dt) == 12))
            # New Year's Eve
            | ((dt._day_of_month(dt) == 31) & (dt._month(dt) == 12))
        ):
            return True
        else:
            return False
