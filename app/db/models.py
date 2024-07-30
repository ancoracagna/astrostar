import os
from dotenv import load_dotenv
from sqlalchemy import ForeignKey, String, BigInteger, Integer, inspect
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

DB_URL = os.getenv('DB_URL')

engine  = create_async_engine(url=DB_URL, echo=True)

async_session = async_sessionmaker(engine)
class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    refs: Mapped[int]
    refer_id: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)

class Check(Base):
    __tablename__ = 'checks'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    desc: Mapped[str] = mapped_column(String)
    res: Mapped[str] = mapped_column(String)
    unique: Mapped[str] = mapped_column(String)

class Forecast(Base):
    __tablename__ = 'forecasts'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String)
    count: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)

class EventRef(Base):
    __tablename__ = 'ref_event'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    event: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    ref_name: Mapped[str] = mapped_column(String)

class Ref_Code(Base):
    __tablename__ = 'ref_codes'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    ref_name: Mapped[str] = mapped_column(String)
    price: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)

class OP(Base):
    __tablename__ = 'ops'

    id:Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger) # Кто создал
    op_name: Mapped[str] = mapped_column(String)
    op_username: Mapped[str] = mapped_column(String)
    op_link: Mapped[str] = mapped_column(String)
    op_status: Mapped[str] = mapped_column(String)
    op_count: Mapped[int]
    op_date: Mapped[str] = mapped_column(String)
    op_tgs: Mapped[str] = mapped_column(String) # список telegram_id из бота, которые подписались

class Setting(Base):
    __tablename__ = 'settings'

    id: Mapped[int] = mapped_column(primary_key=True)
    op_enabled: Mapped[int]
    reff_enabled: Mapped[int]

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
