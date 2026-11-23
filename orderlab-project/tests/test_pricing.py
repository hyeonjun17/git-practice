import pytest

from orderlab.pricing import final_total, subtotal


def test_subtotal_normal():
    price = 10_000
    quantity = 2
    result = subtotal(price, quantity)
    assert result == 20_000


def test_subtotal_zero():
    assert subtotal(0, 3) == 0


def test_subtotal_negative():
    with pytest.raises(ValueError, match="negative input"):
        subtotal(-100, 2)


def test_discount_below_zero():
    with pytest.raises(ValueError, match="invalid discount"):
        final_total(10_000, 2, -1)


def test_discount_over_100():
    with pytest.raises(ValueError, match="invalid discount"):
        final_total(10_000, 2, 101)


@pytest.mark.parametrize(
    ("price", "qty", "discount", "expected"),
    [
        (10_000, 2, 0, 23_000),
        (49_999, 1, 0, 52_999),
        (50_000, 1, 0, 50_000),
        (50_001, 1, 0, 50_001),
        (10_000, 2, 10, 21_000),
        (50_000, 1, 1, 52_500),
        (0, 3, 0, 0),
        (10_000, 2, 100, 0),
    ],
)
def test_final_total(price, qty, discount, expected):
    assert final_total(price, qty, discount) == expected
