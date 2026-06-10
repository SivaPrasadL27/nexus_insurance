from sqlalchemy import Column, String, Float
from app.core.database import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True)
    customer_id = Column(String)
    premium = Column(Float)
    status = Column(String)
    coverage_amount = Column(Float)  # max claim allowed
    policy_type = Column(String)     # e.g. medica
