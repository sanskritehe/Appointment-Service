import databases
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
database = databases.Database(DATABASE_URL)

class DBClient:
    def __init__(self):
        self.database = database

    async def fetch_one(self, query: str, values: dict) -> dict:
        """
        Fetch a single record matching the query from the database.
        """
        return await self.database.fetch_one(query=query, values=values)
