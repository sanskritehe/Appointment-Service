import db_client


async def delete_appointment(appointment_id: int):
    return db_client.delete_appointment(appointment_id)
