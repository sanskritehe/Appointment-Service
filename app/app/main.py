from fastapi import FastAPI
from app.routes import appointments

app = FastAPI()

app.include_router(appointments.router)
