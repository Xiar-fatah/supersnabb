from datetime import date


class Date:
    """
    Represents a custom type for dates.

    Parameters
    ----------
    date : str
        The date string, e.g. "2020-01-01".
    """

    def __init__(self, year: int, month: int, day: int):
        if not all(isinstance(date_args, int) for date_args in [year, month, day]):
            raise ValueError("year, month and day must be integers")
        else:
            self._date = dt(year, month, day)

    def _week_day(self, date: dt) -> int:
        """
        Returns the weekday of a date. For example dt(2023,1,1) would be a Monday, i.e., 0.

        date : dt
            The date of which to calculate the weekday.
        """
        return date.weekday()

    def _day_of_month(self, date: dt) -> int:
        """
        Returns the day of the month. For example dt(2023,1,1) would be the first day of the month, i.e., 1.

        date : dt
            The date of which to calculate the day of month.
        """
        return date.day

    def _day_of_year(self, date: dt) -> int:
        """
        Returns the day of the year. For example dt(2023,1,1) would be the first day of the year, i.e., 1.

        date : dt
            The date of which to calculate the day of year.
        """
        return (date - dt(date.year, 1, 1)).days + 1

    def _year(self, date: dt) -> int:
        """
        Returns the year of a date. For example dt(2023,1,1) would be 2023.

        date : dt
            The date of which to calculate the year.
        """
        return date.year

    def _month(self, date: dt) -> int:
        """
        Returns the month of a date. For example dt(2023,1,1) would be January, i.e., 1.

        date : dt
            The date of which to calculate the month.
        """
        return date.month

    def _is_weekend(self, date: dt) -> bool:
        """
        Returns true if date such as date(2023,1,2) is a weekend else false.

        date : date
            is a date object such as date(2023,1,2)
        """
        if date.weekday() < 5:
            return False
        else:
            return True

    def _calc_day_of_year(self, date: dt) -> int:
        """
        Calculates the day of the year. For example dt(2023,1,1) would be the first day of the year, i.e., 1.

        date : dt
            The date of which to calculate the day of year.
        """
        return (date - dt(date.year, 1, 1)).days + 1


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
