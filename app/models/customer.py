# from sqlalchemy import Column, String, Integer, Float
# from app.core.database import Base

# class Customer(Base):
#     __tablename__ = "customers"

#     id = Column(String, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)
#     salary = Column(Float)
#     address = Column(String)

from sqlalchemy import Column, String, Integer, Float
from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    salary = Column(Float)
    address = Column(String)