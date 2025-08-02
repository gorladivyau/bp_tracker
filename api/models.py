from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Patient table model
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    dob = Column(Date, nullable=False)
    gender = Column(String, nullable=True)

    # Relationship to measurements
    measurements = relationship("Measurement", back_populates="patient",
                                cascade="all, delete-orphan")

# Measurement table model
class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    systolic = Column(Integer, nullable=False)
    diastolic = Column(Integer, nullable=False)
    heart_rate = Column(Integer, nullable=True)

    # Back-reference to patient
    patient = relationship("Patient", back_populates="measurements")
