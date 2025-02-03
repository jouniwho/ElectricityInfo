"""
Model for databse
"""

from sqlalchemy import Column, Integer, Date, Numeric, TIMESTAMP
from app.database import Base

class ElectricityData(Base):
    __tablename__ = "electricitydata"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, name="date")
    startTime = Column(TIMESTAMP, nullable=False, name="starttime")
    productionAmount = Column(Numeric(11,5), nullable=True, name="productionamount")  # Explicit lowercase
    consumptionAmount = Column(Numeric(11,3), nullable=True, name="consumptionamount")
    hourlyPrice = Column(Numeric(6,3), nullable=True, name="hourlyprice")

