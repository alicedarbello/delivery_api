from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import Base, db

from auth_routes import auth_router
from order_routes import order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(db)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(order_router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Delivery API is running - Made with FastAPI.",
        "docs": "Access the API documentation at /docs or /redoc",
        "endpoints": {
            "/auth": "Authentication routes",
            "/orders": "Need to be authenticated to access order routes",
        },
    }
