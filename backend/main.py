# This is for testing purposes to see if it indeed works
from fastapi import FastAPI
from routers import booking


app = FastAPI()
app.include_router(booking.router)


@app.get("/")
def read_root():
    return {"message": "It works"}
