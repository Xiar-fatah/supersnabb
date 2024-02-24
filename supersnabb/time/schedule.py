from __future__ import annotations
from supersnabb.time.date import Date, Tenor
from supersnabb.time.calendar import Calendar
from supersnabb.time.calendars.null_calendar import NullCalendar
from typing import Union, Optional


class Schedule:
    """
    A class used to generate cashflow schedules for interest rates products using backwards or forward generation schedule.

    Parameters
    ----------
    effective_date : datetime.datetime
        The effective date of the schedule. Meaning the date from which the schedule starts. It also corresponds to the date
        when a swap starts accruing interest.

    termination_date : datetime.datetime
        The termination date of the schedule. Meaning the date from which the schedule ends. It also corresponds to the end
        date of the swap.

    tenor : str
        The tenor of the schedule. Meaning the period between two coupons. For example, a 6M tenor means that the period
        between two coupons is 6 months.

    calendar : Callable
        The calendar used to generate the schedule. It is used to determine whether a date is a business day or not.

    convention : Callable
        The convention used to generate the schedule. It is used to determine how to adjust a date if it is not a business day.

    termination_date_convention : Callable
        The convention used to adjust the termination date. It is used to determine how to adjust the termination date if it is not a business day.

    rule : str
        The rule used to generate the schedule. It is used to determine whether the schedule is generated forward or backward.

    end_of_month : bool
        Whether to adjust dates to the end of the month or not.

    first_date : datetime.datetime
        The first date of the schedule. Impacts the regularity of the schedule, occurs when the schedule is customized.

    next_to_last : datetime.datetime
        The next to last date of the schedule. Impacts the regularity of the schedule, occurs when the schedule is customized.
    """

    def __init__(
        self,
        effective_date: Date,
        termination_date: Date,
        tenor: Union[str, Tenor],
        calendar: Calendar,
        convention: str,
        termination_date_convention: str,
        rule: str,
        end_of_month: Optional[bool] = None,
        first_date: Optional[Date] = None,
        next_to_last: Optional[Date] = None,
    ):
        self.effective_date = effective_date
        self.termination_date = termination_date
        if isinstance(type(tenor), type(Tenor)):
            self.tenor = tenor
        elif isinstance(tenor, str):
            self.tenor = Tenor(tenor)
        else:
            raise ValueError(
                f"tenor must be a string or a Tenor object, received: {tenor}"
            )
        self.calendar = calendar
        self.convention = convention
        self.termination_date_convention = termination_date_convention
        if rule.lower() not in ["backward", "forward"]:
            raise ValueError(
                "rule must be backward or forward received: {}".format(rule)
            )
        else:
            self.rule = rule.lower()
        self.end_of_month = end_of_month
        self.first_date = first_date
        self.next_to_last = next_to_last
        self._dates = []
        self._is_regular = []
        self._schedule = self._create_schedule()

    def __repr__(self):
        return self._schedule.__repr__()

    def __len__(self):
        return len(self._dates)

    @property
    def has_is_regular(self):
        """
        Returns a boolean indicating whether the schedule has is_regular or not.
        """
        return len(self._is_regular) != 0

    @property
    def is_regular(self):
        """
        Returns a list of booleans indicating whether the schedule is regular or not. It is related
        to whether first_date or next_to_last is used.
        """
        return self._is_regular

    @property
    def dates(self):
        """
        Returns the dates of the schedule.
        """
        return self._dates

    def _create_schedule(self):
        # Checks for forward generation and IMM generation
        if self.first_date is not None:
            match self.rule:
                case (
                    "forward"
                ):  # Note there is indeed more cases but not implemented yet
                    if not (self.first_date > self.effective_date) or not (
                        self.first_date <= self.termination_date
                    ):
                        raise ValueError(
                            f"first_date must be after effective_date: {self.effective_date} and before termination_date: {self.termination_date}, received: {self.first_date}."
                        )
        if self.next_to_last is not None:
            match self.rule:
                case "forward":
                    if not (self.next_to_last >= self.effective_date is True) or (
                        self.next_to_last < self.termination_date is True
                    ):
                        raise ValueError(
                            f"next_to_last must be after effective_date: {self.effective_date} and before termination_date: {self.termination_date}, received: {self.next_to_last}."
                        )
        periods = 1

        match self.rule:
            case "backward":
                self._dates.append(self.termination_date)
                seed = self.termination_date

                # Checks if next_to_last is regular or not
                if self.next_to_last is not None:
                    self._dates.insert(0, self.next_to_last)
                    temp = NullCalendar.advance(seed, self.tenor * -1, self.convention)
                    if temp != self.next_to_last:
                        self._is_regular.insert(0, False)
                    else:
                        self._is_regular.insert(0, True)
                    seed = self.next_to_last

                exit_date = self.effective_date
                if self.first_date is not None:
                    exit_date = self.first_date

                while True:
                    # temp moves back in time using -periods * tenor
                    temp = NullCalendar.advance(
                        seed, self.tenor * -periods, self.convention
                    )
                    if temp < exit_date:
                        # Checks if first_date is regular or not
                        if self.first_date is not None:
                            adjusted_front_date = self.calendar.adjust(
                                self._dates[0], self.convention
                            )
                            adjusted_first_date = self.calendar.adjust(
                                self.first_date, self.convention
                            )
                            if adjusted_front_date != adjusted_first_date:
                                self._dates.insert(0, self.first_date)
                                self._is_regular.insert(0, False)
                        break
                    else:
                        # Appends all other dates not related to first_date or next_to_last
                        adjusted_front_date = self.calendar.adjust(
                            self._dates[0], self.convention
                        )
                        adjusted_temp = self.calendar.adjust(temp, self.convention)
                        if adjusted_front_date != adjusted_temp:
                            self._dates.insert(0, temp)
                            self._is_regular.insert(0, True)
                        periods += 1
                # Checks if effective_date is regular or not
                adjusted_front_date = self.calendar.adjust(
                    self._dates[0], self.convention
                )
                adjusted_effective_date = self.calendar.adjust(
                    self.effective_date, self.convention
                )
                if adjusted_front_date != adjusted_effective_date:
                    self._dates.insert(0, self.effective_date)
                    self._is_regular.insert(0, False)

            case "forward":
                self._dates.append(self.effective_date)
                seed = self.effective_date
                # Checks if first_date is regular or not
                if self.first_date is not None:
                    self._dates.append(self.first_date)
                    temp = NullCalendar.advance(
                        seed, self.tenor * periods, self.convention
                    )
                    if temp != self.first_date:
                        self._is_regular.append(False)
                    else:
                        self._is_regular.append(True)
                    seed = self.first_date
                exit_date = self.termination_date
                if self.next_to_last is not None:
                    exit_date = self.next_to_last
                while True:
                    temp = NullCalendar().advance(
                        seed, self.tenor * periods, self.convention
                    )
                    if temp > exit_date:
                        # Checks if next_to_last is regular or not
                        if self.next_to_last is not None:
                            adjusted_back_date = self.calendar.adjust(
                                self._dates[-1], self.convention
                            )
                            adjusted_next_to_last = self.calendar.adjust(
                                self.next_to_last, self.convention
                            )
                            if adjusted_back_date != adjusted_next_to_last:
                                self._dates.append(self.next_to_last)
                                self._is_regular.append(False)
                        break
                    else:
                        # Appends all other dates not related to first_date or next_to_last
                        adjusted_back_date = self.calendar.adjust(
                            self._dates[-1], self.convention
                        )
                        adjusted_temp = self.calendar.adjust(temp, self.convention)
                        if adjusted_back_date != adjusted_temp:
                            self._dates.append(temp)
                            self._is_regular.append(True)
                        periods += 1
                    # Checks if termination_date is regular or not
                adjusted_back_date = self.calendar.adjust(
                    self._dates[-1], self.convention
                )
                adjusted_termination_date = self.calendar.adjust(
                    self.termination_date, self.convention
                )
                if adjusted_back_date != adjusted_termination_date:
                    self._dates.append(self.termination_date)
                    self._is_regular.append(False)
        # At last adjust the resulting dates
        for idx, date in enumerate(self._dates):
            self._dates[idx] = self.calendar.adjust(date, self.convention)

        return self._dates
