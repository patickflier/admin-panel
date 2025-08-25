import sqlalchemy as s
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, sessionmaker, mapped_column as mc
from settings import settings

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
