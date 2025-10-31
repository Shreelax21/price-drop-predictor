from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.models.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    previous_price = Column(Float, nullable=True)
    highest_price = Column(Float, nullable=True)
    lowest_price = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
