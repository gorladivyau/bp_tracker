from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import schemas, database, crud, seed
from fastapi.responses import JSONResponse

# Initialize DB with sample data
seed.run()

# Create FastAPI app
app = FastAPI(title="Blood‑Pressure Tracker API")

# Enable CORS for all origins (useful during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Patients -----------------------------------------------------------
# Get list of all patients
@app.get("/patients", response_model=list[schemas.Patient])
def list_patients(db: Session = Depends(get_db)):
    return crud.get_patients(db)

# Create a new patient
@app.post("/patients", response_model=schemas.Patient, status_code=201)
def create_patient(p: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, p)

# --- Measurements -------------------------------------------------------
# Add a new measurement for a patient
@app.post("/patients/{pid}/measurements", response_model=schemas.Measurement,
          status_code=201)
def add_meas(pid: int, meas: schemas.MeasurementCreate,
             db: Session = Depends(get_db)):
    return crud.add_measurement(db, pid, meas)

# List measurements, optionally by patient ID
@app.get("/measurements", response_model=list[schemas.Measurement])
def list_measurements(pid: int | None = None, db: Session = Depends(get_db)):
    return crud.get_measurements(db, patient_id=pid)

# --- Aggregate stats ----------------------------------------------------
# Get latest blood pressure per patient, cached
@app.get("/stats/last_bp")
def latest_bp(db: Session = Depends(get_db)):
    try:
        return crud.last_bp_per_patient(db)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"error": str(e)})
