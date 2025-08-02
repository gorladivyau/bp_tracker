from sqlalchemy.orm import Session
from . import models, schemas, cache

# Patients -------------------------------------------------
# Get all patients from the database
def get_patients(db: Session):
    return db.query(models.Patient).all()

# Create a new patient and update cache
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    cache.invalidate_stats(db)  # clear related cached data
    return db_patient

# Measurements --------------------------------------------
# Add a new measurement for a patient
def add_measurement(db: Session, patient_id: int,
                    meas: schemas.MeasurementCreate):
    db_meas = models.Measurement(**meas.dict(exclude_unset=True),
                                 patient_id=patient_id)
    db.add(db_meas)
    db.commit()
    db.refresh(db_meas)
    cache.invalidate_stats(db)
    return db_meas

# Get measurements, optionally filtered by patient
def get_measurements(db: Session, patient_id: int | None = None):
    q = db.query(models.Measurement)
    if patient_id:
        q = q.filter(models.Measurement.patient_id == patient_id)
    return q.order_by(models.Measurement.timestamp).all()

# Aggregated (cached) statistics --------------------------
# Return latest BP reading per patient, using Redis cache
def last_bp_per_patient(db: Session):
    key = "last_bp_by_patient"
    if (cached := cache.redis_get_json(key)):
        return cached

    rows = (db.query(models.Patient.name,
                     models.Measurement.systolic,
                     models.Measurement.diastolic,
                     models.Measurement.timestamp)
            .join(models.Measurement)
            .order_by(models.Measurement.timestamp.desc())
            .all())

    seen = set()
    result = []
    for r in rows:
        if r.name not in seen:
            result.append({
                "name": r.name,
                "systolic": r.systolic,
                "diastolic": r.diastolic,
                "timestamp": r.timestamp.isoformat()
            })
            seen.add(r.name)

    cache.redis_set_json(key, result, ttl=300)
    return result
