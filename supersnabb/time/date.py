from datetime import date as dt


class Date:
    """
    Represents a custom type for dates.

    Parameters
    ----------
    date : str
        The date string, e.g. "2020-01-01".
    """

    def __init__(self, year: int, month: int, day: int):
        if not isinstance([year, month, day], int):
            raise ValueError("year, month and day must be integers")
        else:
            self._date = dt(year, month, day)


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
