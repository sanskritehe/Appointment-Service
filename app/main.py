from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.routes import appointments
from app.graphql_schema import schema

app = FastAPI(title="Appointment Service")

app.include_router(appointments.router)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
