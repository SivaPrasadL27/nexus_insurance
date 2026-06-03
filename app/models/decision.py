# class Decision(Base):
#     __tablename__ = "decisions"

#     id = Column(String, primary_key=True)
#     entity_id = Column(String)
#     decision = Column(String)
#     confidence = Column(Float)
#     evidence = Column(String)

from sqlalchemy import Column, String, Float
from app.core.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(String, primary_key=True)
    entity_id = Column(String)
    decision = Column(String)
    confidence = Column(Float)
    evidence = Column(String)