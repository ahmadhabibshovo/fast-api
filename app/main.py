from fastapi import FastAPI
from . import models
from .database import engine
from .routers import courses, users, auth

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AIQuest Course API")

# Root routes
@app.get("/")
def home():
    return {"message": "Welcome to AIQuest FastAPI"}

@app.get("/about")
def about():
    return {"about": "This is a test API for managing courses"}

# Include routers
app.include_router(courses.router)
app.include_router(users.router)
app.include_router(auth.router)
