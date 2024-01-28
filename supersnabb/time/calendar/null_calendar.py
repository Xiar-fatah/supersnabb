from calendar import Calendar
from supersnabb.time.date import Date


class NullCalendar(Calendar):
    def is_business_day(self, dt: Date):
        """
        A null calendar to calculate dates for schedule. Contains no holidays but check for weekends.
        Thus, if it is a business day it should return True else False
        """
        return True
