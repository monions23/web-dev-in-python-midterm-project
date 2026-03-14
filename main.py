from typing import Annotated

from fastapi import APIRouter, FastAPI, HTTPException, Path

from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from tv_show_routes import show_router

app = FastAPI(
    title="TV Show List",
    version="0.135.1",
)


@app.get("/")
async def home() -> dict:
    return FileResponse("./frontend/index.html")


app.include_router(show_router, tags=["Shows"], prefix="/shows")

# the router needs to be before the mount otherwise the routes cannot be found
app.mount("/", StaticFiles(directory="frontend"), name="static")
