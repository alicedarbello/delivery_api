from fastapi import FastAPI

app = FastAPI()


from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
async def root() -> dict:
    return {
        "message": "Delivery API is running - Made with FastAPI.",
        "docs": "Access the API documentation at /docs or /redoc",
        "endpoints": {
            "/auth": "Authentication routes",
            "/orders": "Need to be authenticated to access order routes"
            }
        }