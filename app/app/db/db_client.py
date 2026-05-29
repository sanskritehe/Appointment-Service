from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

class DBClient:
    def __init__(self, session: AsyncSession):
        self.session = session

    def query(self, model):
        """
        Create an async query for the given model.

        Args:
            model: The SQLAlchemy model to query.

        Returns:
            sqlalchemy.future.select: The async query object.
        """
        return select(model)  # Use SQLAlchemy's `select` for async queries.

    async def execute(self, query):
        """
        Execute an asynchronous query.

        Args:
            query: The query object.

        Returns:
            result: The result of query execution.
        """
        try:
            result = await self.session.execute(query)
            return result
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database execution error: {e}")

    async def commit(self):
        """
        Commit the current transaction.
        """
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database commit error: {e}")

