from datetime import date, datetime
from typing import List
from pydantic import BaseModel, Field

# Shared fields for a measurement
class MeasurementBase(BaseModel):
    systolic:   int = Field(..., ge=60,  le=260)
    diastolic:  int = Field(..., ge=30,  le=180)
    heart_rate: int | None = Field(None, ge=30, le=220)

# Input schema for creating a measurement
class MeasurementCreate(MeasurementBase):
    timestamp: datetime | None = None

# Output schema for a measurement (includes DB fields)
class Measurement(MeasurementBase):
    id:        int
    timestamp: datetime
    patient_id: int

    class Config:
        orm_mode = True  # allows ORM model compatibility

# Shared fields for a patient
class PatientBase(BaseModel):
    name:   str
    dob:    date
    gender: str | None = None

# Input schema for creating a patient
class PatientCreate(PatientBase):
    pass

# Output schema for a patient (includes measurements)
class Patient(PatientBase):
    id:           int
    measurements: List[Measurement] = []

    class Config:
        orm_mode = True
