import pandas as pd
from supersnabb.cashflows.coupon import Coupon
from supersnabb.time.schedule import Schedule
from supersnabb.time.daycounter import Daycounter
from supersnabb.time.business_day_convention import BusinessDayConvention
from supersnabb.time.calendar import Calendar
from supersnabb.time.date import Tenor, Date
from supersnabb.termstructure.curve import DiscountCurve
from supersnabb.indices.ibor_index import IborIndex
from typing import Optional


class FloatRateCoupon(Coupon):
    def __init__(
        self,
        payment_date: Date,
        nominal: int,
        start_accrual_date: Date,
        end_accrual_date: Date,
        start_ref_date: Date,
        end_ref_date: Date,
        daycount: Daycounter,
        discount_curve: DiscountCurve,
        ibor_index: IborIndex,
    ):
        self.payment_date = payment_date
        self.nominal = nominal
        self.start_accrual_date = start_accrual_date
        self.end_accrual_date = end_accrual_date
        self.start_ref_date = start_ref_date
        self.end_ref_date = end_ref_date
        self.daycount = daycount
        self.discount_curve = discount_curve
        self.ibor_index = ibor_index

    @property
    def forward_rate(self) -> float:
        return self.ibor_index.forecast_fixing_with_dates(
            self.start_accrual_date, self.end_accrual_date
        )

    @property
    def discount_factor(self) -> float:
        return self.discount_curve(self.payment_date)

    @property
    def coupon(self):
        return self.nominal * self.forward_rate * self.discount_factor * self.accrual

    @property
    def accrual(self):
        return self.daycount().year_fraction(
            self.start_accrual_date, self.end_accrual_date
        )

    @property
    def amount(self):
        return self.accrual * self.nominal * self.forward_rate

    @property
    def num_days(self):
        return (
            self.end_accrual_date.serial_number - self.start_accrual_date.serial_number
        )


class FloatRateLeg:
    def __init__(
        self,
        float_schedule: Schedule,
        nominal: int,
        ibor_index: IborIndex,
        float_daycount: Daycounter,
        float_convention: BusinessDayConvention,
        discount_curve: DiscountCurve,
        payment_lag: Optional[Tenor] = Tenor("0D"),
    ):
        self.float_schedule = float_schedule
        self.nominal = nominal
        self.float_daycount = float_daycount
        self.float_convention = float_convention
        self.discount_curve = discount_curve
        self.payment_lag = payment_lag
        self.ibor_index = ibor_index
        self.calendar = self.ibor_index.fixing_calendar
        self.coupons = self._create_float_coupons()

    @property
    def cashflows(self):
        _ = {}
        for idx, coupon in enumerate(self.coupons):
            _[idx] = {
                "Notional": self.nominal,
                "Payment Date": coupon.payment_date,
                "Start Accrual Date": coupon.start_accrual_date,
                "End Accrual Date": coupon.end_accrual_date,
                "Accrual": coupon.accrual,
                "Discount Factor": coupon.discount_factor,
                "Coupon": coupon.coupon,
                "Amount": coupon.amount,
                "Number of Days": coupon.num_days,
                "Forward Rate": coupon.forward_rate,
            }
        return pd.DataFrame.from_dict(_).T

    def _create_float_coupons(self) -> list:
        # Generate the first coupon
        coupons = []
        float_schedule_dates = self.float_schedule.dates
        start_accrual_date = float_schedule_dates[0]
        end_accrual_date = float_schedule_dates[1]
        payment_date = self.calendar().advance(
            end_accrual_date, self.payment_lag, self.float_convention
        )

        if (self.float_schedule.is_regular[1] is not True) and (
            self.float_schedule.has_is_regular is True
        ):
            ref_date = self.calendar.advance(
                end_accrual_date, -1 * self.calendar.tenor, self.float_convention
            )
        else:
            ref_date = start_accrual_date

        coupons.append(
            FloatRateCoupon(
                payment_date,
                self.nominal,
                start_accrual_date,
                end_accrual_date,
                ref_date,
                end_accrual_date,
                self.float_daycount,
                self.discount_curve,
                self.ibor_index,
            )
        )

        # Generate the rest of the coupons with the exception of the last one
        for i in range(2, len(self.float_schedule.dates) - 1):
            start_accrual_date = end_accrual_date
            end_accrual_date = float_schedule_dates[i]
            payment_date = self.calendar().advance(
                end_accrual_date, self.payment_lag, self.float_convention
            )
            coupons.append(
                FloatRateCoupon(
                    payment_date,
                    self.nominal,
                    start_accrual_date,
                    end_accrual_date,
                    ref_date,
                    end_accrual_date,
                    self.float_daycount,
                    self.discount_curve,
                    self.ibor_index,
                )
            )
        # Generate the last coupon
        if len(float_schedule_dates) > 2:
            N = len(self.float_schedule.dates)
            start_accrual_date = end_accrual_date
            end_accrual_date = float_schedule_dates[N - 1]
            payment_date = self.calendar().advance(
                end_accrual_date, self.payment_lag, self.float_convention
            )
            if (self.float_schedule.has_is_regular is not True) and (
                self.float_schedule.is_regular[N - 1]
            ):
                ref_date = self.calendar.advance(
                    end_accrual_date, -1 * self.calendar.tenor, self.float_convention
                )
            else:
                ref_date = start_accrual_date
            coupons.append(
                FloatRateCoupon(
                    payment_date,
                    self.nominal,
                    start_accrual_date,
                    end_accrual_date,
                    ref_date,
                    end_accrual_date,
                    self.float_daycount,
                    self.discount_curve,
                    self.ibor_index,
                )
            )
        return coupons
