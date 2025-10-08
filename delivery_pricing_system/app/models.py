from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    inputs = Column(JSON)
    total_price = Column(Float, nullable=True)
    action_log = Column(JSON, default=list)
    price_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Escalation(Base):
    __tablename__ = "escalations"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Database setup
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

engine = create_async_engine(Config.DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
