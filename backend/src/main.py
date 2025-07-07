# This is for testing purposes to see if it indeed works
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "It works"}
