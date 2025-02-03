"""
Schema for database
"""

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ElectricityDataSchema(BaseModel):
    id: int
    date: date
    startTime: datetime
    productionAmount: Optional[float] = None
    consumptionAmount: Optional[float] = None
    hourlyPrice: Optional[float] = None

    class Config:
        from_attributes = True
