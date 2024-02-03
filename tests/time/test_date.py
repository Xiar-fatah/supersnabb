import QuantLib as ql
from supersnabb.time.date import Tenor, Date
from datetime import date
from dateutil.relativedelta import relativedelta
import pytest


def test_tenor_date_with_ql():
    ql_dt = ql.Date(1, 1, 2000)
    ss_dt = Date(2000, 1, 1)
    assert (Tenor("1D") + ss_dt).ISO() == (ql_dt + ql.Period("1D")).ISO()
    assert (Tenor("1W") + ss_dt).ISO() == (ql_dt + ql.Period("1W")).ISO()
    assert (Tenor("1M") + ss_dt).ISO() == (ql_dt + ql.Period("1M")).ISO()
    assert (Tenor("1Y") + ss_dt).ISO() == (ql_dt + ql.Period("1Y")).ISO()

    assert (Tenor("1D") - ss_dt).ISO() == (ql_dt - ql.Period("1D")).ISO()
    assert (Tenor("1W") - ss_dt).ISO() == (ql_dt - ql.Period("1W")).ISO()
    assert (Tenor("1M") - ss_dt).ISO() == (ql_dt - ql.Period("1M")).ISO()
    assert (Tenor("1Y") - ss_dt).ISO() == (ql_dt - ql.Period("1Y")).ISO()

    assert ((Tenor("1D") * 3) - ss_dt).ISO() == (ql_dt - (3 * ql.Period("1D"))).ISO()
    assert ((Tenor("1W") * 3) - ss_dt).ISO() == (ql_dt - (3 * ql.Period("1W"))).ISO()
    assert ((Tenor("1M") * 3) - ss_dt).ISO() == (ql_dt - (3 * ql.Period("1M"))).ISO()
    assert ((Tenor("1Y") * 3) - ss_dt).ISO() == (ql_dt - (3 * ql.Period("1Y"))).ISO()


def test_tenor_with_ql():
    num_dates = 10000
    dt = date(2000, 1, 1)
    for idx in range(num_dates):
        dt = dt + relativedelta(days=1)
        ss_dt = Date(dt.year, dt.month, dt.day)
        ql_dt = ql.Date(dt.day, dt.month, dt.year)
        assert (Tenor("1D") + ss_dt).ISO() == (ql_dt + ql.Period("1D")).ISO()
        assert (Tenor("1W") + ss_dt).ISO() == (ql_dt + ql.Period("1W")).ISO()
        assert (Tenor("1M") + ss_dt).ISO() == (ql_dt + ql.Period("1M")).ISO()
        assert (Tenor("1Y") + ss_dt).ISO() == (ql_dt + ql.Period("1Y")).ISO()

        assert (Tenor("1D") - ss_dt).ISO() == (ql_dt - ql.Period("1D")).ISO()
        assert (Tenor("1W") - ss_dt).ISO() == (ql_dt - ql.Period("1W")).ISO()
        assert (Tenor("1M") - ss_dt).ISO() == (ql_dt - ql.Period("1M")).ISO()
        assert (Tenor("1Y") - ss_dt).ISO() == (ql_dt - ql.Period("1Y")).ISO()

        assert ((Tenor("1D") * 3) - ss_dt).ISO() == (
            ql_dt - (3 * ql.Period("1D"))
        ).ISO()
        assert ((Tenor("1W") * 3) - ss_dt).ISO() == (
            ql_dt - (3 * ql.Period("1W"))
        ).ISO()
        assert ((Tenor("1M") * 3) - ss_dt).ISO() == (
            ql_dt - (3 * ql.Period("1M"))
        ).ISO()
        assert ((Tenor("1Y") * 3) - ss_dt).ISO() == (
            ql_dt - (3 * ql.Period("1Y"))
        ).ISO()


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
    assert (Tenor("1d") + Date(2022, 12, 31)).ISO() == Date(2023, 1, 1).ISO()
    assert (Tenor("1d") - Date(2022, 12, 31)).ISO() == Date(2022, 12, 30).ISO()
    assert (Tenor("-1d") + Date(2022, 12, 31)).ISO() == Date(2022, 12, 30).ISO()
    assert (Tenor("-1d") - Date(2022, 12, 31)).ISO() == Date(2023, 1, 1).ISO()

    assert (Tenor("1M") + Date(2022, 12, 31)).ISO() == Date(2023, 1, 31).ISO()
    assert (Tenor("-1M") + Date(2022, 12, 31)).ISO() == Date(2022, 11, 30).ISO()
    assert (Tenor("-1M") - Date(2022, 12, 31)).ISO() == Date(2023, 1, 31).ISO()
    assert (Tenor("1M") - Date(2022, 12, 31)).ISO() == Date(2022, 11, 30).ISO()
