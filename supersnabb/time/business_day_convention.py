from enum import StrEnum, auto


class BusinessDayConvention(StrEnum):
    FOLLOWING = auto()
    MODIFIEDFOLLOWING = auto()
    PRECEDING = auto()
    MODIFIEDPRECEDING = auto()
    UNADJUSTED = auto()
    HALFMONTHMODIFIEDFOLLOWING = auto()
    NEAREST = auto()
