from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base  

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    num_pages = Column(Integer)
    content = Column(Text)  
    summary = Column(Text)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())