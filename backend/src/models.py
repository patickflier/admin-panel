from sqlalchemy.orm import Mapped, mapped_column as mc
from db import Base
from datetime import datetime
import sqlalchemy as s


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
    is_paid: Mapped[bool] = mc(default=False, server_default=False)
