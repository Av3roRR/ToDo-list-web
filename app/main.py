from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.notes.router import router as router_notes

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_notes)
