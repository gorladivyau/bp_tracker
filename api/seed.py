from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from . import models, database, crud, schemas

# Initialize DB schema and seed with sample data
def run():
    models.Base.metadata.create_all(bind=database.engine)  # create tables

    db: Session = database.SessionLocal()
    if db.query(models.Patient).count():
        return  # skip if already seeded

    # Create two sample patients
    p1 = crud.create_patient(db, schemas.PatientCreate(
        name="Alice Smith", dob=date(1980, 5, 12), gender="F"))
    p2 = crud.create_patient(db, schemas.PatientCreate(
        name="Bob Jones", dob=date(1975, 1, 3), gender="M"))

    # Add 10 measurements per patient
    now = datetime.utcnow()
    for idx, pt in enumerate([p1, p2]):
        for i in range(10):
            crud.add_measurement(
                db, pt.id,
                schemas.MeasurementCreate(
                    systolic=120 + idx * 5 + i,
                    diastolic=80 + idx * 3 + i,
                    heart_rate=70 + i,
                    timestamp=now - timedelta(days=10 - i)))
    db.close()
