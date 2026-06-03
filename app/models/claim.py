# class Claim(Base):
#     __tablename__ = "claims"

#     id = Column(String, primary_key=True)
#     customer_id = Column(String)
#     amount = Column(Float)
#     status = Column(String)

from sqlalchemy import Column, String, Float
from app.core.database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(String, primary_key=True)
    customer_id = Column(String)
    amount = Column(Float)
    status = Column(String)