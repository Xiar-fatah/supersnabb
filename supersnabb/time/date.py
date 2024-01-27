from datetime import date as date
from dateutil.relativedelta import relativedelta


class Date:
    """
    Represents a custom type for dates.

    Parameters
    ----------
    year: int
        The year of the date.
    month: int
        The month of the date.
    day: int
        The day of the date.

    """

    def __init__(self, year: int, month: int, day: int):
        if not all(isinstance(date_args, int) for date_args in [year, month, day]):
            raise ValueError("year, month and day must be integers")
        else:
            self._date = date(year, month, day)

    def _week_day(self, dt: date) -> int:
        """
        Returns the weekday of a date. For example date(2023,1,1) would be a Monday, i.e., 0.

        dt: date
            The date of which to calculate the weekday.
        """
        return dt.weekday()

    def _day_of_month(self, dt: date) -> int:
        """
        Returns the day of the month. For example date(2023,1,1) would be the first day of the month, i.e., 1.

        dt: date
            The date of which to calculate the day of month.
        """
        return dt.day

    def _day_of_year(self, dt: date) -> int:
        """
        Returns the day of the year. For example date(2023,1,1) would be the first day of the year, i.e., 1.

        dt: date
            The date of which to calculate the day of year.
        """
        return (dt - dt(dt.year, 1, 1)).days + 1

    def _year(self, dt: date) -> int:
        """
        Returns the year of a date. For example date(2023,1,1) would be 2023.

        dt: date
            The date of which to calculate the year.
        """
        return dt.year

    def _month(self, dt: date) -> int:
        """
        Returns the month of a date. For example date(2023,1,1) would be January, i.e., 1.

        dt: date
            The date of which to calculate the month.
        """
        return dt.month

    def _is_weekend(self, date: date) -> bool:
        """
        Returns true if date such as date(2023,1,2) is a weekend else false.

        date : date
            is a date object such as date(2023,1,2)
        """
        if date.weekday() < 5:
            return False
        else:
            return True

    def _calc_day_of_year(self, date: date) -> int:
        """
        Calculates the day of the year. For example date(2023,1,1) would be the first day of the year, i.e., 1.

        date : date
            The date of which to calculate the day of year.
        """
        return (date - date(date.year, 1, 1)).days + 1


class Tenor:
    """
    Represents a custom type for tenors.

    Parameters
    ----------
    tenor : str
        The tenor string, e.g. "1D", "1W", "1M", "1Y".
    """

    def __init__(self, tenor: str):
        # Check that tenor is a string and fulfills the format
        if not isinstance(tenor, str):
            raise ValueError("tenor must be a string")
        if tenor[-1].upper() not in ["D", "W", "M", "Y"]:
            raise ValueError("tenor must end with D, W, M or Y")
        if tenor[0] == "-":
            self.length = int(tenor[:-1])
            if tenor[1:-1].isdigit() is not True:
                raise ValueError("tenor must start with a number")

        elif not tenor[:-1].isdigit():
            raise ValueError("tenor must start with a number")
        else:
            self.length = int(tenor[:-1])

        self._tenor = tenor.upper()
        self.unit = self._tenor[-1]

    def __repr__(self):
        return self._tenor

    def __add__(self, value):
        if isinstance(value, date):
            return self._add_tenor_to_date(value, self.length, self.unit, "add")
        elif isinstance(value, Tenor):
            if self.unit != value.unit:
                raise ValueError("cannot add tenors of different units")
            return Tenor(str(self.length + value.length) + self.unit)
        else:
            value = Tenor(value)
            return self + value

    def __sub__(self, value):
        if isinstance(value, date):
            return self._add_tenor_to_date(value, self.length, self.unit, "sub")
        elif isinstance(value, Tenor):
            if self.unit != value.unit:
                raise ValueError("cannot add tenors of different units")
            return Tenor(str(self.length - value.length) + self.unit)
        else:
            value = Tenor(value)
            return self - value

    def _add_tenor_to_date(self, dt: date, length: int, unit: str, func: str) -> date:
        """
        Returns d + n*unit. Meaning that datetime.date(2023,1,1) + Tenor("1D") would return datetime.date(2023,1,2).
        Note that if the unit is negative then the date will be subtracted instead of added.

        Parameters
        ----------
        date : datetime.date
            The date to add the tenor to.
        fixing : int
            The number of units to add to the date.
        time_unit : str
            The unit of the tenor, can be "D", "W", "M" or "Y".
        """
        if unit == "D":
            if func == "sub":
                return dt - relativedelta(days=length)
            else:
                return dt + relativedelta(days=length)
        elif unit == "W":
            if func == "sub":
                return dt - relativedelta(weeks=length)
            else:
                return dt + relativedelta(weeks=length)
        elif unit == "M":
            if func == "sub":
                return dt - relativedelta(months=length)
            else:
                return dt + relativedelta(months=length)
        elif unit == "Y":
            if func == "sub":
                return dt - relativedelta(years=length)
            else:
                return dt + relativedelta(years=length)

    def __mul__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Tenor needs to be multiplied with an integer")
        return Tenor(str(self.length * value) + self.unit)
