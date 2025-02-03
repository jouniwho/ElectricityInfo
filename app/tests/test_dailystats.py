"""
Test script.
Made according to fastAPI documentation
https://fastapi.tiangolo.com/how-to/testing-database/
"""
from sqlalchemy.orm import Session
from app.models import ElectricityData
from datetime import datetime
from decimal import Decimal

def add_test_data(db: Session):
    """
    Function to add test data to the database
    """
    sample_data = [
        ElectricityData(
            date=datetime(2025, 2, 1).date(),
            startTime=datetime(2025, 2, 1, 12, 0, 0),
            productionAmount=Decimal("1234.56789"),
            consumptionAmount=Decimal("567.890"),
            hourlyPrice=Decimal("1.234"),
        ),
        ElectricityData(
            date=datetime(2024, 2, 2).date(),
            startTime=datetime(2024, 2, 2, 14, 30, 0),
            productionAmount=Decimal("2345.67891"),
            consumptionAmount=Decimal("678.901"),
            hourlyPrice=Decimal("45.678"),
        ),
    ]
    db.add_all(sample_data)
    db.commit()

def test_daily_stats(client, test_db_session):
    add_test_data(test_db_session) 
    response = client.get(
        "/api/daily-stats/"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_one_day(client, test_db_session):
    add_test_data(test_db_session)
    response = client.get(
        "/api/day-stats/2024-02-02"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_daily_stats_filter(client, test_db_session):
    add_test_data(test_db_session) 
    response = client.get(
        "/api/daily-stats/?date_from=2024-02-02&date_to=2025-02-01"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_daily_stats_filter_wrong(client, test_db_session):
    add_test_data(test_db_session) 
    response = client.get(
        "/api/daily-stats/?date_from=2025-2-1&date_to=2024-02-02"
    )

    assert response.status_code == 400


def test_daily_stats_not_found(client, test_db_session):
    add_test_data(test_db_session) 
    response = client.get(
        "/api/daily-stats/?date_from=2026-2-1&date_to=2027-02-02"
    )

    assert response.status_code == 404


def test_one_day_not_found(client, test_db_session):
    add_test_data(test_db_session)
    response = client.get(
        "/api/day-stats/1234-02-02"
    )

    assert response.status_code == 404
