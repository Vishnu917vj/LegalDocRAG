from fastapi import FastAPI

from app.api.routes import router as ask_router


app = FastAPI(
    title="Legal QA API"
)

app.include_router(
    ask_router
)