from __future__ import annotations
import datetime
from dateutil.relativedelta import relativedelta
from dateutil import easter  # Only needed for Easter Monday


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

    def __init__(self, y: int, m: int, d: int):
        if not all(isinstance(date_args, int) for date_args in [y, m, d]):
            raise ValueError("year, month and day must be integers")
        if y < 1900:
            raise ValueError("year must be greater than 1900")
        if m < 1 or m > 12:
            raise ValueError("month must be between 1 and 12")
        if d < 1 or d > 31:
            raise ValueError("day must be between 1 and 31")
        self.y = y
        self.m = m
        self.d = d
        self.leap = self._is_leap(y)
        self.date = datetime.date(y, m, d)
        # day_length = self._month_length(month, leap)
        self.month_offset = self._month_offset(m, self.leap)
        year_offset = self._year_offset(y)

        self.serial_number = d + self.month_offset + year_offset

    def is_week(self) -> bool:
        """
        Returns True if the date is a weekend.
        """
        return self.date.weekday() > 4

    def weekday(self) -> int:
        """
        Returns the day of the week for the date.
        """
        return self.date.weekday()

    def easter_monday(self) -> datetime.date:
        """
        Calculates eastern monday for the year of the date.
        """
        em_date = easter.easter(self.date.year) + datetime.timedelta(days=1)
        em_day_of_year = em_date.timetuple().tm_yday
        return em_day_of_year

    def day_of_year(self) -> int:
        return self.month_offset + self.d

    def month(self) -> int:
        # Is this class needed?
        d = self.day_of_year()
        m = int(d / 30) + 1

        while d <= self._month_offset(m, self.leap):
            m -= 1
        while d > self._month_offset(m + 1, self.leap):
            m += 1
        return m

    def year(self) -> int:
        y = int(self.serial_number / 365) + 1900
        if self.serial_number <= self._year_offset(y):
            y -= 1
        return y

    def _month_length(self, month: int, leap: bool) -> int:
        month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_length_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        return month_length_leap[month - 1] if leap else month_length[month - 1]

    def _month_offset(self, month: int, leap: bool) -> int:
        month_offset = [
            0,
            31,
            59,
            90,
            120,
            151,  # Jan - Jun
            181,
            212,
            243,
            273,
            304,
            334,  # Jun - Dec
            365,  # used in dayOfMonth to bracket day
        ]
        month_offset_leap = [
            0,
            31,
            60,
            91,
            121,
            152,  # Jan - Jun
            182,
            213,
            244,
            274,
            305,
            335,  # Jun - Dec
            366,  # used in dayOfMonth to bracket day
        ]
        return month_offset_leap[month - 1] if leap else month_offset[month - 1]

    def _year_offset(self, year: int) -> int:
        year_offset = [
            # 1900-1909
            0,
            366,
            731,
            1096,
            1461,
            1827,
            2192,
            2557,
            2922,
            3288,
            # 1910-1919
            3653,
            4018,
            4383,
            4749,
            5114,
            5479,
            5844,
            6210,
            6575,
            6940,
            # 1920-1929
            7305,
            7671,
            8036,
            8401,
            8766,
            9132,
            9497,
            9862,
            10227,
            10593,
            # 1930-1939
            10958,
            11323,
            11688,
            12054,
            12419,
            12784,
            13149,
            13515,
            13880,
            14245,
            # 1940-1949
            14610,
            14976,
            15341,
            15706,
            16071,
            16437,
            16802,
            17167,
            17532,
            17898,
            # 1950-1959
            18263,
            18628,
            18993,
            19359,
            19724,
            20089,
            20454,
            20820,
            21185,
            21550,
            # 1960-1969
            21915,
            22281,
            22646,
            23011,
            23376,
            23742,
            24107,
            24472,
            24837,
            25203,
            # 1970-1979
            25568,
            25933,
            26298,
            26664,
            27029,
            27394,
            27759,
            28125,
            28490,
            28855,
            # 1980-1989
            29220,
            29586,
            29951,
            30316,
            30681,
            31047,
            31412,
            31777,
            32142,
            32508,
            # 1990-1999
            32873,
            33238,
            33603,
            33969,
            34334,
            34699,
            35064,
            35430,
            35795,
            36160,
            # 2000-2009
            36525,
            36891,
            37256,
            37621,
            37986,
            38352,
            38717,
            39082,
            39447,
            39813,
            # 2010-2019
            40178,
            40543,
            40908,
            41274,
            41639,
            42004,
            42369,
            42735,
            43100,
            43465,
            # 2020-2029
            43830,
            44196,
            44561,
            44926,
            45291,
            45657,
            46022,
            46387,
            46752,
            47118,
            # 2030-2039
            47483,
            47848,
            48213,
            48579,
            48944,
            49309,
            49674,
            50040,
            50405,
            50770,
            # 2040-2049
            51135,
            51501,
            51866,
            52231,
            52596,
            52962,
            53327,
            53692,
            54057,
            54423,
            # 2050-2059
            54788,
            55153,
            55518,
            55884,
            56249,
            56614,
            56979,
            57345,
            57710,
            58075,
            # 2060-2069
            58440,
            58806,
            59171,
            59536,
            59901,
            60267,
            60632,
            60997,
            61362,
            61728,
            # 2070-2079
            62093,
            62458,
            62823,
            63189,
            63554,
            63919,
            64284,
            64650,
            65015,
            65380,
            # 2080-2089
            65745,
            66111,
            66476,
            66841,
            67206,
            67572,
            67937,
            68302,
            68667,
            69033,
            # 2090-2099
            69398,
            69763,
            70128,
            70494,
            70859,
            71224,
            71589,
            71955,
            72320,
            72685,
            # 2100-2109
            73050,
            73415,
            73780,
            74145,
            74510,
            74876,
            75241,
            75606,
            75971,
            76337,
            # 2110-2119
            76702,
            77067,
            77432,
            77798,
            78163,
            78528,
            78893,
            79259,
            79624,
            79989,
            # 2120-2129
            80354,
            80720,
            81085,
            81450,
            81815,
            82181,
            82546,
            82911,
            83276,
            83642,
            # 2130-2139
            84007,
            84372,
            84737,
            85103,
            85468,
            85833,
            86198,
            86564,
            86929,
            87294,
            # 2140-2149
            87659,
            88025,
            88390,
            88755,
            89120,
            89486,
            89851,
            90216,
            90581,
            90947,
            # 2150-2159
            91312,
            91677,
            92042,
            92408,
            92773,
            93138,
            93503,
            93869,
            94234,
            94599,
            # 2160-2169
            94964,
            95330,
            95695,
            96060,
            96425,
            96791,
            97156,
            97521,
            97886,
            98252,
            # 2170-2179
            98617,
            98982,
            99347,
            99713,
            100078,
            100443,
            100808,
            101174,
            101539,
            101904,
            # 2180-2189
            102269,
            102635,
            103000,
            103365,
            103730,
            104096,
            104461,
            104826,
            105191,
            105557,
            # 2190-2199
            105922,
            106287,
            106652,
            107018,
            107383,
            107748,
            108113,
            108479,
            108844,
            109209,
            # 2200
            109574,
        ]
        return year_offset[year - 1900]

    def _is_leap(self, year: int) -> bool:
        year_is_leap = [
            # 1900 is leap in agreement with Excel's bug
            # 1900 is out of valid date range anyway
            # 1900-1909
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 1910-1919
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 1920-1929
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 1930-1939
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 1940-1949
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 1950-1959
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 1960-1969
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 1970-1979
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 1980-1989
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 1990-1999
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2000-2009
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2010-2019
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2020-2029
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2030-2039
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2040-2049
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2050-2059
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2060-2069
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2070-2079
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2080-2089
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2090-2099
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2100-2109
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2110-2119
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2120-2129
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2130-2139
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2140-2149
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2150-2159
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2160-2169
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2170-2179
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2180-2189
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            # 2190-2199
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            # 2200
            False,
        ]
        return year_is_leap[year - 1900]


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

    def __add__(self, value) -> Tenor:
        if isinstance(value, datetime.date):
            return self._add_tenor_to_date(value, self.length, self.unit, "add")
        elif isinstance(value, Tenor):
            if self.unit != value.unit:
                raise ValueError("cannot add tenors of different units")
            return Tenor(str(self.length + value.length) + self.unit)
        else:
            value = Tenor(value)
            return self + value

    def _radd__(self, value) -> Tenor:
        return self.__add__(value)

    def __sub__(self, value) -> Tenor:
        if isinstance(value, datetime.date):
            return self._add_tenor_to_date(value, self.length, self.unit, "sub")
        elif isinstance(value, Tenor):
            if self.unit != value.unit:
                raise ValueError("cannot add tenors of different units")
            return Tenor(str(self.length - value.length) + self.unit)
        else:
            value = Tenor(value)
            return self - value

    def __rsub__(self, value) -> Tenor:
        return self.__sub__(value)

    def _add_tenor_to_date(
        self, dt: datetime.date, length: int, unit: str, func: str
    ) -> datetime.date:
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

    def __mul__(self, value: int) -> Tenor:
        if not isinstance(value, int):
            raise ValueError("Tenor needs to be multiplied with an integer")
        return Tenor(str(self.length * value) + self.unit)
