from fastapi import FastAPI
from app.api import tournament

app = FastAPI(
    title="Mini Tournament System",
    version="1.0.0"
)

app.include_router(tournament.router)
