from fastapi import FastAPI
from .models import database
from .database.connection import engine

app = FastAPI()

database.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
