from fastapi import FastAPI

from app import models
from app.api.users import router as users_router
from app.api.products import router as products_router
from app.database import Base, engine
from app.api.orders import router as orders_router
from fastapi.staticfiles import StaticFiles


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce QA Automation Application",
    description="Mock e-commerce application for UI, API and database testing.",
    version="1.0.0",
)
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend",
)

app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "E-Commerce QA Automation Application",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }