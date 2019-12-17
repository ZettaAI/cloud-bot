from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Challenge(BaseModel):
    token: str
    challenge: str
    type: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/events")
def challenge(data: Challenge):
    print(data)
    return data.challenge
