from sqlalchemy import Column, String, Integer, DateTime
from Backend.databases.db import Base
from sqlalchemy.sql import func

class Products(Base):
    __tablename__ = 'products'
    Id = Column(Integer,primary_key= True, index = True)
    Name = Column(String(200),nullable = False)
    Description = Column(String(500),nullable = True)
    Category = Column(Integer,nullable = False)
    Price = Column(String(20),nullable=False)
    Status = Column(String(20))
    Created_at =Column(DateTime(timezone = True),server_default = func.now())
    updated_on =Column(DateTime(timezone = True),onupdate = func.now())
