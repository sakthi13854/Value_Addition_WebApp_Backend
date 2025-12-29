from sqlalchemy import Column , Integer ,String , Date ,ForeignKey
from sqlalchemy.orm import relationship
from Backend.databases.db import Base

class Consumers(Base):
    __tablename__ = "Consumers"
    Id = Column(Integer,primary_key =True, index = True)
    Name = Column(String(200),nullable = False)
    Email = Column(String(200),unique = True, nullable = False)
    Password = Column(String(255),nullable = False)
