from sqlalchemy import Column, Integer, String, Text
from app.database.connection import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    symptoms = Column(Text)
    precautions = Column(Text)
    treatment = Column(Text)
