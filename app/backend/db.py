from sqlalchemy import  Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///taskmanager.db" , echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass