import os
from fastapi import FastAPI

app = FastAPI(title="Private FastAPI Argo Demo")

APP_ENV = os.getenv("APP_ENV", "local")
APP_VERSION = os.getenv("APP_VERSION", "local")


@app.get("/")
def home():
    return {
        "message": "Private FastAPI Argo Demo is running",
        "environment": APP_ENV,
        "version": APP_VERSION,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/version")
def version():
    return {
        "environment": APP_ENV,
        "version": APP_VERSION,
    }


@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}


@app.get("/sub")
def subtract(a: int, b: int):
    return {"result": a - b}


@app.get("/mul")
def multiply(a: int, b: int):
    return {"result": a * b}
