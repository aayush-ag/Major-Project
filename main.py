# --- main.py ---

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from health import start_health_check
from routes import nodes, neighbours, chat, voicechat


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    start_health_check()
    yield
    # Optional: shutdown logic


app = FastAPI(lifespan=lifespan)

# Include routers after defining app
app.include_router(nodes.router)
app.include_router(neighbours.router)
app.include_router(chat.router)
app.include_router(voicechat.router)
