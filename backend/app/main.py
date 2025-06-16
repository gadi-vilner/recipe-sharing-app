# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import users, recipes, auth

# This command tells SQLAlchemy to create all the tables defined in our models
# if they don't already exist in the database.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Sharing App API",
    description="API for managing and sharing culinary recipes.",
    version="1.0.0"
)

#Define the allowed origins
origins = [
    "http://localhost:3000",
    # You could add your deployed frontend URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # This is the key for preflight requests
    allow_headers=["*"],  # This is the key for preflight requests
)

# Include the users router
# This is the line that makes your /users endpoint available.
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recipes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Recipe Sharing API!"}