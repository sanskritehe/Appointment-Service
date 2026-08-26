from typing import Optional, List, Tuple, Dict
import sqlite3

# Database connection settings
DATABASE_PATH = "data/appointments.db"

DEFAULT_LIMIT = 10
MAX_LIMIT = 100

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # To return results as dictionaries
    return conn

async def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

async def get_appointments_paginated(offset: int, limit: int) -> Tuple[List[Dict], int]:
    if offset < 0 or limit < 1 or limit > MAX_LIMIT:
        raise ValueError("Invalid pagination parameters. Offset must be >= 0, limit must be between 1 and 100.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch paginated results
        cursor.execute("SELECT * FROM appointments LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        # Fetch total count to calculate pagination
        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_count = cursor.fetchone()[0]

        return [dict(row) for row in rows], total_count
    finally:
        conn.close()
