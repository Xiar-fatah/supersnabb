from supersnabb.time.daycounter import Daycounter
from supersnabb.time.date import Date


class ACT360(Daycounter):
    def __init__(self):
        super().__init__()

    def year_fraction(self, start_date: Date, end_date: Date) -> float:
        print(f"{(end_date.serial_number - start_date.serial_number) = }")
        return (end_date.serial_number - start_date.serial_number) / 360

    def day_count(self, start_date: Date, end_date: Date) -> int:
        return super().day_count(start_date, end_date)

    def __repr__(self):
        return "ACT/360"
