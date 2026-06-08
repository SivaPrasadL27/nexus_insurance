from sqlalchemy import Column, String, Float, DateTime
from app.core.database import Base

from datetime import datetime, timezone
datetime.now(timezone.utc)

created_at = Column(DateTime, default=datetime.utcnow)

class Claim(Base):
    __tablename__ = "claims"

    id = Column(String, primary_key=True)
    customer_id = Column(String)
    policy_id = Column(String) 
    amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)