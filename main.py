from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException, Path

from fastapi.concurrency import asynccontextmanager
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from database import init
from tv_show_routes import show_router
from auth_routes import auth_router
from user_routes import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init()
    print("Database connected")

    yield

    # Shutdown logic (optional)
    print("Shutting down...")


app = FastAPI(
    title="TV Show List",
    version="0.135.1",
    lifespan=lifespan
)


@app.get("/")
async def home() -> dict:
    return FileResponse("./frontend/login.html")


app.include_router(show_router, tags=["Shows"], prefix="/shows")
app.include_router(auth_router, tags=["Auth"], prefix="/auth")
app.include_router(user_router, tags=["Users"], prefix="/users")


# the router needs to be before the mount otherwise the routes cannot be found
app.mount("/", StaticFiles(directory="frontend"), name="static")
