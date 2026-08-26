from fastapi import FastAPI
from app.db.db_client import database
from app.routes import appointments

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(appointments.router)
