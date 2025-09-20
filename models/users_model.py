from sqlalchemy import Column, Integer, String
from db import Base

class User():
    __tablename__ ="user"
    id = Column(Integer,primary_key=True,index=True,nullable=False)
    username = Column(String(50), unique=True, index=True,nullable=False)
    password = Column(String(255), nullable=False)
    