import sqlite3


def delete_appointment(appointment_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        return None
    return True
