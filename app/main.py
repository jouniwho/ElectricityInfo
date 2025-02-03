"""
Basic api implementation made by following fastAPI documentation.
https://fastapi.tiangolo.com/#installation
https://fastapi.tiangolo.com/tutorial/sql-databases/#create-models
Cors was handled with this:
https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.routes import daily_stats
from app.routes import healthcheck

app.include_router(daily_stats.router)

app.include_router(healthcheck.router)
