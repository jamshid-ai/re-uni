from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from typing_extensions import Annotated
import datetime

from config import DB_URL


# Create a Po in-memory database engine
engine = create_async_engine(DB_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(engine, expire_on_commit=False, autoflush=True ,class_=AsyncSession)

Base = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True)]

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[intpk]

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow, nullable=True)