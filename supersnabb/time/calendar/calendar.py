from __future__ import annotations
from abc import ABCMeta, abstractmethod
from supersnabb.time.date import Date, Tenor
from supersnabb.time.business_day_convention import BusinessDayConvention


class Calendar(metaclass=ABCMeta):
    def adjust(
        self,
        date: Date,
        convention: BusinessDayConvention,
    ) -> Date:
        """
        Adjusts a given non business day to the next business day with respect to a convention.

        Parameters
        ----------
        date : Date
            The date to make the evaluation, for deposits it should be the reference date.
        convention : str
            The business day convention, such as following, modified following and such.
        calendar : Callable
            The calendar used to determine whether a date is a business day or not.
        """
        if convention == BusinessDayConvention.UNADJUSTED:
            return date

        date1 = date
        if (
            (convention == BusinessDayConvention.FOLLOWING)
            or (convention == BusinessDayConvention.MODIFIEDFOLLOWING)
            or (convention == BusinessDayConvention.HALFMONTHMODIFIEDFOLLOWING)
        ):
            while self.is_business_day(date1) is False:
                date1 = date1 + 1
            if (
                convention == BusinessDayConvention.MODIFIEDFOLLOWING
                or convention == BusinessDayConvention.HALFMONTHMODIFIEDFOLLOWING
            ):
                if date1.month() != date.month():
                    return self.adjust(date, BusinessDayConvention.PRECEDING)
                if convention == BusinessDayConvention.HALFMONTHMODIFIEDFOLLOWING:
                    if date.day <= 15 and date1.day > 15:
                        return self.adjust(date, BusinessDayConvention.PRECEDING)

        elif (convention == BusinessDayConvention.PRECEDING) or (
            convention == BusinessDayConvention.MODIFIEDPRECEDING
        ):
            while self.is_business_day(date1) is False:
                date1 = date1 - 1
            if convention == BusinessDayConvention.MODIFIEDPRECEDING and (
                date1.month() != date.month()
            ):
                return self.adjust(date, BusinessDayConvention.FOLLOWING)
        elif convention == BusinessDayConvention.NEAREST:
            date2 = date
            while (self.is_business_day(date1) is False) and (
                self.is_business_day(date2) is False
            ):
                date1 = date1 + 1
                date2 = date2 - 1
            if self.is_business_day(date1) is False:
                return date2
            else:
                return date1
        else:
            raise ValueError("Unknown business-day convention")
        return date1

    def advance_with_tenor(
        self: Calendar, date: Date, tenor: Tenor, convention: BusinessDayConvention
    ) -> Date:
        pass  # return self.advance(date, tenor, convention

    def advance(
        self,
        date: Date,
        advance_period: Tenor,  # rewrite this to n and unit instead
        convention: BusinessDayConvention,
    ) -> Date:
        """
        Advances the given date forth or back and adjusts it with respect to a convention.

        Parameters
        ----------
        date : Date
            The date to make the evaluation, for deposits it should be the reference date.
        fixing_period : Callable
            The period to advance the date, for example datetime.date(2023,1,2) + Tenor, meaning the input should be Tenor("2D").
        convention : str
            The business day convention, such as following, modified following and such.
        calendar : Callable
            The calendar used to determine whether a date is a business day or not.

        """
        n = advance_period.length
        if n == 0:
            return self.adjust(date, convention)
        elif advance_period.unit == "D":
            d1 = date
            if n > 0:
                while n > 0:
                    d1 = d1 + 1
                    while self.is_business_day(d1) is False:
                        d1 = d1 + 1
                    n -= 1
            else:
                while n < 0:
                    d1 = d1 - 1
                    while self.is_business_day(d1) is False:
                        d1 = d1 - 1
                    n += 1
            return d1
        elif advance_period.unit == "W":
            d1 = advance_period + date
            return self.adjust(d1, convention)
        else:
            d1 = advance_period + date
            return self.adjust(d1, convention)

    @abstractmethod
    def is_business_day(self, dt: Date):
        pass
