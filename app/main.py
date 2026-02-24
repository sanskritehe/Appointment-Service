from fastapi import FastAPI
from app.routes import appointments

app = FastAPI(title="Appointment Service")

app.include_router(appointments.router)