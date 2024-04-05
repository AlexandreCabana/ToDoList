from sqlalchemy import Boolean, Column, Integer, String
from database import Base
class ToDo(Base):
    __tablename__ = 'TaskList'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50),unique=False)
    is_completed = Column(Boolean,unique=False)
    duedate = Column(String(20),unique=False)

