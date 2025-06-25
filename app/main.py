from contextlib import asynccontextmanager

from fastapi import FastAPI
from .models import database
from .database.connection import engine
from .routers import userRoutes, notesRoutes
from .services.ai_functions import cleanup_llm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Smart Notes API...")
    database.Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    print("Shutting down Smart Notes API...")
    await cleanup_llm_service()

app = FastAPI(
    title="Smart Notes API",
    description="A note-taking API with AI-powered summaries and categorization",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(userRoutes.router)
app.include_router(notesRoutes.router)