from typing import List
from supersnabb.time.date import Date
from supersnabb.time.calendar import Calendar
from supersnabb.time.daycounter import Daycounter
from enum import StrEnum, auto
from bisect import bisect_right


class InterpolationType(StrEnum):
    LINEAR = auto()
    LOGLINEAR = auto()
    FLATFORWARD = auto()


class Interpolation:
    def __init__(
        self,
        dates: List[Date],
        rates: List[float],
        daycount: Daycounter,
        interpolation: InterpolationType = InterpolationType.LINEAR,
    ):
        match interpolation:
            case InterpolationType.LINEAR:
                self.interpolation_method = self._linear_interpolation
            case InterpolationType.LOGLINEAR:
                self.interpolation_method = self._log_linear_interpolation
            case InterpolationType.FLATFORWARD:
                self.interpolation_method = self._flat_forward
            case _:
                raise ValueError(
                    f"Interpolation type not supported received: {interpolation}"
                )
        self.dates = dates
        self.rates = rates
        self.daycount = daycount

    def interpolate(self, date: Date) -> int:
        right_node = self._locate(
            date.serial_number, [dates.serial_number for dates in self.dates]
        )
        left_node = (
            right_node
            if (right_node == 0) | (right_node == len(self.dates))
            else right_node - 1
        )
        return self.interpolation_method(
            date.serial_number,
            self.dates[left_node].serial_number,
            self.dates[right_node].serial_number,
            self.rates[left_node],
            self.rates[right_node],
        )

    def _locate(self, x: float, dates: List[Date]) -> int:
        """
        Finds the index of dates of which x is to the right.

        Example
        -------
        Assume dates = [1,2,3,4] and x is 2.5, then _locate will return 3.

        Parameters
        ----------
        x : float
            The pillar to find the interpolated value for.

        """
        if x < dates[0]:
            return 0
        elif x > dates[-1]:
            return len(dates)
        else:
            return bisect_right(dates, x + 10e-7)
        # 0.0000001 is to mimic c++ upper bound

    def _linear_interpolation(
        self, x: float, x_begin: float, x_end: float, y_begin: float, y_end: float
    ) -> float:
        """
        Linear interpolation between two points.

        Parameters
        ----------
        x : float
            The pillar to find the interpolated value for.
        x_begin: float
            The initial pillar of the curve, is most likely 0.
        x_end: float
            The
        y_begin: float
            The initial value of the curve.
        y_end: float
            The end value of the curve.
        """
        return y_begin + (x - x_begin) * (y_end - y_begin) / (x_end - x_begin)

    def _log_linear_interpolation(
        self, x: float, x_begin: float, x_end: float, y_begin: float, y_end: float
    ) -> float:
        """
        Log linear interpolation between two points.

        Parameters
        ----------
        x : float
            The pillar to find the interpolated value for.
        x_begin: float
            The initial pillar of the curve, is most likely 0.
        x_end: float
            The
        y_begin: float
            The initial value of the curve.
        y_end: float
            The end value of the curve.
        """
        return y_begin * (y_end / y_begin) ** ((x - x_begin) / (x_end - x_begin))

    def _flat_forward(
        self, x: float, x_begin: float, x_end: float, y_begin: float, y_end: float
    ) -> float:
        """
        Flat forward interpolation between two points.

        Parameters
        ----------
        x : float
            The pillar to find the interpolated value for.
        x_begin: float
            The initial pillar of the curve, is most likely 0.
        x_end: float
            The
        y_begin: float
            The initial value of the curve.
        y_end: float
            The end value of the curve.
        """
        if x < x_begin:
            return y_begin
        else:
            return y_end
