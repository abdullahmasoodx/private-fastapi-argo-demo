import os
import socket

from fastapi import FastAPI

app = FastAPI(
    title="Basic GitOps App",
    version="1.0.0",
)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Hello from GitOps and Argo CD!",
        "version": os.getenv("APP_VERSION", "v2"),
        "pod": socket.gethostname(),
    }



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
