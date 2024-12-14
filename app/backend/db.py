from sqlalchemy import  Column, Integer, String, create_engine,  select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

engine = create_engine("sqlite:///../taskmanager.db" , echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

