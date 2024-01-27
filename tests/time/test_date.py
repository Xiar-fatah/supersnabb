import QuantLib as ql
from supersnabb import Tenor
from datetime import date
from dateutil.relativedelta import relativedelta
import pytest


def test_tenor_with_ql():
    num_dates = 10000
    dt = date(2000, 1, 1)
    for idx in range(num_dates):
        dt = dt + relativedelta(days=1)
        ql_dt = ql.Date(dt.day, dt.month, dt.year)
        assert Tenor("1D") + dt == (ql_dt + ql.Period("1D")).to_date()
        assert Tenor("1W") + dt == (ql_dt + ql.Period("1W")).to_date()
        assert Tenor("1M") + dt == (ql_dt + ql.Period("1M")).to_date()
        assert Tenor("1Y") + dt == (ql_dt + ql.Period("1Y")).to_date()

        assert Tenor("1D") - dt == (ql_dt - ql.Period("1D")).to_date()
        assert Tenor("1W") - dt == (ql_dt - ql.Period("1W")).to_date()
        assert Tenor("1M") - dt == (ql_dt - ql.Period("1M")).to_date()
        assert Tenor("1Y") - dt == (ql_dt - ql.Period("1Y")).to_date()

        assert (Tenor("1D") * 3) - dt == (ql_dt - (3 * ql.Period("1D"))).to_date()
        assert (Tenor("1W") * 3) - dt == (ql_dt - (3 * ql.Period("1W"))).to_date()
        assert (Tenor("1M") * 3) - dt == (ql_dt - (3 * ql.Period("1M"))).to_date()
        assert (Tenor("1Y") * 3) - dt == (ql_dt - (3 * ql.Period("1Y"))).to_date()


def test_tenor():
    # Testing time units
    assert Tenor("6D").unit == "D"
    assert Tenor("6D").length == 6

    assert Tenor("6d").unit == "D"
    assert Tenor("6d").length == 6

    assert Tenor("6W").unit == "W"
    assert Tenor("6W").length == 6

    assert Tenor("6M").unit == "M"
    assert Tenor("6M").length == 6

    assert Tenor("6Y").unit == "Y"
    assert Tenor("6Y").length == 6

    # Testing math operators
    assert str(Tenor("6D") + Tenor("6D")) == str(Tenor("12D"))
    assert str(Tenor("6d") - Tenor("6D")) == str(Tenor("0D"))
    assert str(Tenor("1D") * -1) == str(Tenor("-1D"))

    with pytest.raises(
        ValueError, match="Tenor needs to be multiplied with an integer"
    ):
        Tenor("3M") * 0.2
    assert Tenor("1d") + date(2022, 12, 31) == date(2023, 1, 1)
    assert Tenor("-1d") + date(2022, 12, 31) == date(2022, 12, 30)
    assert Tenor("-1d") - date(2022, 12, 31) == date(2023, 1, 1)
    assert Tenor("1d") - date(2022, 12, 31) == date(2022, 12, 30)

    assert (Tenor("1M") + date(2022, 12, 31)) == date(2023, 1, 31)
    assert (Tenor("-1M") + date(2022, 12, 31)) == date(2022, 11, 30)
    assert (Tenor("-1M") - date(2022, 12, 31)) == date(2023, 1, 31)
    assert (Tenor("1M") - date(2022, 12, 31)) == date(2022, 11, 30)
