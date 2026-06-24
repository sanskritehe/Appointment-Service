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
        if row:
            return {
                "id": row[0],
                "user": row[1],
                "time": row[2],
                "status": row[3]
            }
        else:
            return None
