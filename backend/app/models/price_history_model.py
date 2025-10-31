from sqlalchemy import Column, Integer, Float, TIMESTAMP, ForeignKey
from .database import Base
from datetime import datetime

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    price = Column(Float, nullable=False)
    date = Column(TIMESTAMP, default=datetime.utcnow)
