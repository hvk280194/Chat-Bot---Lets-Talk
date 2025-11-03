from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.routers import health, chat

logger = setup_logging()
app = FastAPI(title="Lets Talk")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"service": "Lets Talk", "status": "ok"}
