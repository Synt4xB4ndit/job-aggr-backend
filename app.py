from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_NAME, APP_VERSION
from routers.jobs import router as jobs_router

import os

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

FRONTEND_URL = os.getenv("FRONTEND_URL")

origins = [
    "http://localhost:3000",
]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "message": "Job Aggregator API"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


app.include_router(jobs_router)