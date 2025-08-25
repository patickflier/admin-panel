from fastapi import APIRouter

# adapt these to your project, but keep them as RELATIVE imports
from db import SessionLocal

router = APIRouter(prefix="/booking", tags=["booking"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_booking():
    return {"id": "person.id"}
