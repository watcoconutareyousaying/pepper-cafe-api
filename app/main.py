from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api import auth, users
from app.database import Base, engine

load_dotenv()

app = FastAPI(
    title="Pepper Cafe",
    version="1.0.0",
    description="API backend for managing cafe operations including orders, inventory, attendance, salaries, and user roles across web and mobile platforms."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to Pepper Cafe"}