import sqlalchemy as s
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, sessionmaker, mapped_column as mc
from .settings import settings
from datetime import datetime

engine = s.create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class CrmPerson(Base):
    __tablename__ = "crm_person"

    id: Mapped[int] = mc(primary_key=True, autoincrement=True)
    email: Mapped[str] = mc(s.String(100))
    fullname: Mapped[str] = mc(s.String(100))
    first: Mapped[str] = mc(s.String(100), nullable=True)
    infix: Mapped[str] = mc(s.String(100), nullable=True)
    last: Mapped[str] = mc(s.String(100), nullable=True)


class CrmPersonBills(Base):
    __tablename__ = "crm_person_bills"

    id: Mapped[int] = mc(primary_key=True, autoincrement=True)
    owner: Mapped[int] = mc(s.ForeignKey("crm_person.id"))
    price: Mapped[int] = mc(s.String(), default="00.00")
    payment_date: Mapped[datetime] = mc(nullable=True)
    is_paid: Mapped[bool] = mc(default=False, server_default="false")
