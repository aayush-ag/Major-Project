# --- main.py ---

from fastapi import FastAPI
from contextlib import asynccontextmanager

from models import create_tables
from routes import ingest, chat
from health import start_health_check


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_tables()
    start_health_check()
    yield
    # Optional: shutdown logic


app = FastAPI(lifespan=lifespan)

# Include routers after defining app
app.include_router(ingest.router)
app.include_router(chat.router)
