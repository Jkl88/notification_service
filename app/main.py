from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.db.init import init_db
from app.routers import auth, notifications
from app.core.logger import logger

app = FastAPI(title="Notification Service")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url} - {response.status_code}")
    return response


@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
