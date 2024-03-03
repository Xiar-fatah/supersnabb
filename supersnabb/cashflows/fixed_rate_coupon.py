import pandas as pd
from supersnabb.cashflows.coupon import Coupon
from supersnabb.time.schedule import Schedule
from supersnabb.time.daycounter import Daycounter
from supersnabb.time.business_day_convention import BusinessDayConvention
from supersnabb.time.calendar import Calendar
from supersnabb.time.date import Tenor, Date
from supersnabb.termstructure.curve import DiscountCurve
from typing import Optional


class FixedRateCoupon(Coupon):
    def __init__(
        self,
        payment_date: Date,
        nominal: int,
        rate: float,
        start_accrual_date: Date,
        end_accrual_date: Date,
        start_ref_date: Date,
        end_ref_date: Date,
        daycount: Daycounter,
        discount_curve: DiscountCurve,
    ):
        self.payment_date = payment_date
        self.nominal = nominal
        self.rate = rate
        self.start_accrual_date = start_accrual_date
        self.end_accrual_date = end_accrual_date
        self.start_ref_date = start_ref_date
        self.end_ref_date = end_ref_date
        self.daycount = daycount
        self.discount_curve = discount_curve

    @property
    def discount_factor(self):
        return self.discount_curve(self.payment_date)

    @property
    def coupon(self):
        return self.nominal * self.rate * self.discount_factor * self.accrual

    @property
    def accrual(self):
        return self.daycount().year_fraction(
            self.start_accrual_date, self.end_accrual_date
        )

    @property
    def amount(self):
        return self.accrual * self.nominal * self.rate

    @property
    def num_days(self):
        return (
            self.end_accrual_date.serial_number - self.start_accrual_date.serial_number
        )


class FixedRateLeg:
    """
    # TODO: Implement ex coupon dates and varying of coupon rates
    """

    def __init__(
        self,
        fixed_schedule: Schedule,
        nominal: int,
        fixed_rate: float,
        fixed_daycount: Daycounter,
        fixed_convention: BusinessDayConvention,
        calendar: Calendar,
        discount_curve: DiscountCurve,
        payment_lag: Optional[Tenor] = Tenor("0D"),
    ):
        self.fixed_schedule = fixed_schedule
        self.nominal = nominal
        self.fixed_rate = fixed_rate
        self.fixed_daycount = fixed_daycount
        self.fixed_convention = fixed_convention
        self.calendar = calendar
        self.payment_lag = payment_lag
        self.discount_curve = discount_curve
        self.coupons = self._create_fixed_coupons()

    @property
    def cashflows(self):
        _ = {}
        for idx, coupon in enumerate(self.coupons):
            _[idx] = {
                "Notional": self.nominal,
                "Rate": self.fixed_rate,
                "Payment Date": coupon.payment_date,
                "Start Accrual Date": coupon.start_accrual_date,
                "End Accrual Date": coupon.end_accrual_date,
                "Accrual": coupon.accrual,
                "Discount Factor": coupon.discount_factor,
                "Coupon": coupon.coupon,
                "Amount": coupon.amount,
                "Number of Days": coupon.num_days,
            }
        return pd.DataFrame.from_dict(_).T

    def _create_fixed_coupons(self) -> list:
        # Generate the first coupon
        coupons = []
        fixed_schedule_dates = self.fixed_schedule.dates
        start_accrual_date = fixed_schedule_dates[0]
        end_accrual_date = fixed_schedule_dates[1]
        payment_date = self.calendar().advance(
            end_accrual_date, self.payment_lag, self.fixed_convention
        )

        if (self.fixed_schedule.is_regular[1] is not True) and (
            self.fixed_schedule.has_is_regular is True
        ):
            ref_date = self.calendar.advance(
                end_accrual_date, -1 * self.calendar.tenor, self.fixed_convention
            )
        else:
            ref_date = start_accrual_date

        coupons.append(
            FixedRateCoupon(
                payment_date,
                self.nominal,
                self.fixed_rate,
                start_accrual_date,
                end_accrual_date,
                ref_date,
                end_accrual_date,
                self.fixed_daycount,
                self.discount_curve,
            )
        )

        # Generate the rest of the coupons with the exception of the last one
        for i in range(2, len(self.fixed_schedule.dates) - 1):
            start_accrual_date = end_accrual_date
            end_accrual_date = fixed_schedule_dates[i]
            payment_date = self.calendar().advance(
                end_accrual_date, self.payment_lag, self.fixed_convention
            )
            coupons.append(
                FixedRateCoupon(
                    payment_date,
                    self.nominal,
                    self.fixed_rate,
                    start_accrual_date,
                    end_accrual_date,
                    ref_date,
                    end_accrual_date,
                    self.fixed_daycount,
                    self.discount_curve,
                )
            )
        # Generate the last coupon
        if len(fixed_schedule_dates) > 2:
            N = len(self.fixed_schedule.dates)
            start_accrual_date = end_accrual_date
            end_accrual_date = fixed_schedule_dates[N - 1]
            payment_date = self.calendar().advance(
                end_accrual_date, self.payment_lag, self.fixed_convention
            )
            if (self.fixed_schedule.has_is_regular is not True) and (
                self.fixed_schedule.is_regular[N - 1]
            ):
                ref_date = self.calendar.advance(
                    end_accrual_date, -1 * self.calendar.tenor, self.fixed_convention
                )
            else:
                ref_date = start_accrual_date
            coupons.append(
                FixedRateCoupon(
                    payment_date,
                    self.nominal,
                    self.fixed_rate,
                    start_accrual_date,
                    end_accrual_date,
                    ref_date,
                    end_accrual_date,
                    self.fixed_daycount,
                    self.discount_curve,
                )
            )
        return coupons
