from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    user: str
    time: str

class AppointmentBookingCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    time_slot: str

class AppointmentUpdate(BaseModel):
    time: str
    status: str

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str


class PatientCreate(BaseModel):
    name: str
    age: int
    blood_group: str
    contact: str


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    blood_group: str
    contact: str