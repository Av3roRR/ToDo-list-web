from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.notes.router import router as router_notes
from app.users.router import router as router_users

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_notes)
app.include_router(router_users)