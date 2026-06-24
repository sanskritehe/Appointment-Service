from strawberry.fastapi import GraphQLRouter
from app.schemas import schema

graphql_app = GraphQLRouter(schema)
