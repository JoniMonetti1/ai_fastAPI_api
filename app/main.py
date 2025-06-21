from fastapi import FastAPI
from .models import database
from .database.connection import engine
from .routers import userRoutes, notesRoutes

app = FastAPI()

database.Base.metadata.create_all(bind=engine)

app.include_router(userRoutes.router)
app.include_router(notesRoutes.router)