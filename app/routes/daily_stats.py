from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from app.database import get_db
from app.models import ElectricityData
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.routes.utils import longest_negative_streak

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

@router.get("/daily-stats/")
def get_daily_stats(
    page: int = Query(1, alias="page"),
    size: int = Query(10, alias="size"),
    date_from: str = Query(None, alias="date_from"),
    date_to: str = Query(None, alias="date_to"),
    db: Session = Depends(get_db)
):

    # total production and consumption and avg price
    query = db.query(
        ElectricityData.date,
        func.sum(ElectricityData.productionAmount).label("total_production"),
        func.sum(ElectricityData.consumptionAmount).label("total_consumption"),
        func.avg(ElectricityData.hourlyPrice).label("avg_price")
    ).group_by(ElectricityData.date).order_by(ElectricityData.date).all()

    # query for longest negative price
    query_hourly = db.query(
        ElectricityData.date,
        ElectricityData.startTime,
        ElectricityData.hourlyPrice
        ).order_by(ElectricityData.date, ElectricityData.startTime).all()

    # Check that dates are correct
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from cannot be later than date_to")

    longest_streaks = longest_negative_streak(query_hourly)
    
    # data for checking filters and count
    all_data = []
    for row in query:
        all_data.append({
            "date": row[0],
            "total_production": row[1],
            "total_consumption": row[2],
            "avg_price": row[3],
        })


    # Apply Filters
    if date_from:
        all_data = [data for data in all_data if data['date'].strftime("%Y-%m-%d") >= date_from]
    if date_to:
        all_data = [data for data in all_data if data['date'].strftime("%Y-%m-%d") <= date_to]

    # Total Count
    total = total = len(all_data)

    if total == 0:
        raise HTTPException(status_code=404, detail="No data found for the given filters")

    # Pagination
    # for pagination, I got help from this thread and chatgpt
    # https://gist.github.com/jas-haria/a993d4ef213b3c0dd1500f86d31ad749
    # results = query.offset((page - 1) * size).limit(size).all()
    start = (page - 1) * size
    end = start + size
    results = all_data[start:end]

    final_data = []
    for data in results:
        total_consumption = None
        avg_price = None
        if data["total_consumption"] is not None:
            # Convert consumption from kilo to mega
            total_consumption = float(data["total_consumption"]) * 0.001

        if data["avg_price"] is not None:
            # Convert consumption from kilo to mega
            avg_price = round(data["avg_price"], 3)

        final_data.append({
            "date": data["date"],
            "total_production": data["total_production"],
            "total_consumption": total_consumption,
            "avg_price": avg_price,
            "longest_negative_hours": longest_streaks.get(data["date"], 0)
        })

    return {"page": page, "size": size, "total": total, "data": final_data}

@router.get("/day-stats/{date}/")
def get_single_day_stats(date: str, db: Session = Depends(get_db)):
    all_day_stats = db.query(ElectricityData).filter(ElectricityData.date == date).all()

    if not all_day_stats:
        raise HTTPException(status_code=404, detail="Data not found")

    final_data = []

    for row in all_day_stats:
        total_consumption = None
        if row.consumptionAmount != None:
            # Convert consumption from kilo to mega
            total_consumption = round(float(row.consumptionAmount) * 0.001)
        data = {
            "consumptionAmount": total_consumption,
            "id": row.id,
            "date": row.date,
            "startTime": row.startTime,
            "productionAmount": row.productionAmount,
            "hourlyPrice": row.hourlyPrice,
        }
        final_data.append(data)

    return final_data
