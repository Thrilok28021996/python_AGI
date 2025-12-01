from sqlalchemy import Column, Integer, String, Text
from database import Base

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(Text)