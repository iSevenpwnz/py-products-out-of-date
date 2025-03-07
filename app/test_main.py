import datetime
import pytest
from app.main import outdated_products


def fake_date_factory(today_value: datetime.date) -> type[datetime.date]:
    class fake_date(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return today_value
    return fake_date


@pytest.mark.parametrize(
    "today_value, products, expected",
    [
        (
            datetime.date(2022, 2, 5),
            [
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120,
                }
            ],
            [],
        ),
        (
            datetime.date(2022, 2, 5),
            [
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 4),
                    "price": 160,
                }
            ],
            ["duck"],
        ),
        (
            datetime.date(2022, 2, 5),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600,
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 3),
                    "price": 120,
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160,
                },
            ],
            ["chicken", "duck"],
        ),
    ],
)
def test_outdated_products(
    monkeypatch, today_value, products, expected
) -> None:
    fake_date = fake_date_factory(today_value)
    monkeypatch.setattr("app.main.datetime.date", fake_date)
    result = outdated_products(products)
    assert sorted(result) == sorted(expected)
