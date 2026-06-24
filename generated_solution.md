### FILE: app/schemas.py
```python
import strawberry
import strawberry.federation
from app.database import DatabaseClient
from fastapi import HTTPException

db = DatabaseClient()

@strawberry.federation.type(keys=['id'])
class Appointment:
    id: strawberry.ID
    user: str
    time: str
    status: str

@strawberry.type
class Query:
    @strawberry.field
    def appointment(self, id: strawberry.ID) -> Appointment:
        row = db.get_appointment(int(id))
        if row:
            return Appointment(
                id=strawberry.ID(str(row['id'])),
                user=row['user'],
                time=row['time'],
                status=row['status'],
            )
        else:
            raise HTTPException(status_code=404, detail="Appointment not found")

schema = strawberry.federation.Schema(query=Query)
```

### FILE: app/graphql.py
```python
from strawberry.fastapi import GraphQLRouter
from app.schemas import schema

graphql_app = GraphQLRouter(schema)
```

### FILE: main.py
```python
from fastapi import FastAPI
from app.graphql import graphql_app
from app.database import DatabaseClient
from fastapi import HTTPException

app = FastAPI()
app.include_router(graphql_app, prefix='/graphql')

@app.get("/appointments/{id}")
async def read_appointment(id: int):
    db = DatabaseClient()
    appointment = db.get_appointment(id)
    if appointment:
        return appointment
    else:
        raise HTTPException(status_code=404, detail="Appointment not found")

```

### FILE: app/database.py
```python
import sqlite3

class DatabaseClient:
    def __init__(self, db_path: str = 'appointments.db'):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_appointment(self, id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "user": row[1],
                "time": row[2],
                "status": row[3],
            }
        else:
            return None

```

### FILE: export_schema.py
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.schemas import schema
print(schema.as_str())

```