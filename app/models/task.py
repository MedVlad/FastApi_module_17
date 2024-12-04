from app_learning.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    completed = Column(Boolean)
    slug = Column(String, index=True)


user = relationship("Task", back_populates="user_id") #объект  связи  таблицы  с  таблицей  Task, где  back_populates = 'user'.



from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))