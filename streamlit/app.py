# Import required libraries
import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, date
import uuid

# Get the API URL from environment variables or use a default fallback
API = os.getenv("API_URL", "http://localhost:8000")

# Set the app title
st.title("📈 Blood‑Pressure Tracker")

# ---------------------- Cached API Calls ------------------------------ #
# Cache the list of patients for 5 minutes to reduce API load
@st.cache_data(ttl=300)
def fetch_patients():
    return requests.get(f"{API}/patients").json()

# Cache the measurements data for 1 minute, optionally filtered by patient ID
@st.cache_data(ttl=60)
def fetch_measurements(pid: int | None = None):
    url = f"{API}/measurements"
    if pid:
        url += f"?pid={pid}"
    return requests.get(url).json()


# -------------------- Sidebar: Add New Patient ------------------------ #
with st.sidebar:
    st.header("➕ New patient")  # Sidebar heading
    with st.form("add_patient"):  # Form to submit new patient info
        np_name = st.text_input("Name")
        np_dob = st.date_input("Date of birth", value=date(1990, 1, 1),
                               max_value=date.today())
        np_gender = st.selectbox("Gender", ["", "F", "M", "Other"])
        submitted = st.form_submit_button("Create")
        if submitted and np_name.strip():
            # Submit new patient data to the backend API
            r = requests.post(f"{API}/patients",
                              json={"name": np_name, "dob": str(np_dob),
                                    "gender": np_gender or None})
            if r.ok:
                # Store new patient ID to auto-select later
                new_patient = r.json()
                st.session_state["new_patient_id"] = new_patient["id"]
                st.cache_data.clear()  # Clear cached patient list
                st.rerun()  # Refresh app to show new data

# -------------------- Main Interface: Patient Select ------------------ #
patients = fetch_patients()  # Get patient list
names = {p["id"]: p["name"] for p in patients}  # Map patient ID to name

# Two-column layout for selecting patient and extra space
colL, colR = st.columns(2)
with colL:
    if "new_patient_id" in st.session_state:
        # Auto-select newly added patient
        patient_id = st.session_state.pop("new_patient_id")
    else:
        # Dropdown for selecting patient (or all patients)
        patient_id = st.selectbox("Patient", [0] + list(names),
                                  format_func=lambda x: "All patients"
                                  if x == 0 else names[x])

with colR:
    st.empty()  # Placeholder if needed later

# ------------- Form to Add New Measurement (if patient selected) ------ #
if patient_id:
    with st.expander("Add new measurement"):  # Collapsible input section
        sys = st.number_input("Systolic", 60, 260, 120)
        dia = st.number_input("Diastolic", 30, 180, 80)
        hr = st.number_input("Heart rate", 30, 220, 70)
        if st.button("Save"):
            # Create a measurement entry and send to backend
            body = {
                "systolic": sys,
                "diastolic": dia,
                "heart_rate": hr,
                "timestamp": datetime.utcnow().isoformat()
            }
            r = requests.post(
                f"{API}/patients/{patient_id}/measurements", json=body)
            if r.ok:
                st.success("Recorded!")
                st.cache_data.clear()  # Invalidate measurement cache
                st.rerun()
            else:
                st.error(f"Failed to save: {r.status_code} - {r.text}")

# ---------------------- Load Measurement Data ------------------------- #
data = fetch_measurements(patient_id or None)  # Get data for selected patient
if not data:
    st.info("No measurements yet.")  # Inform if no records
    st.stop()

# Convert to pandas DataFrame and parse timestamps
df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ---------------------- Plotly Line Chart ----------------------------- #
fig = px.line(df, x="timestamp", y=["systolic", "diastolic"],
              color_discrete_sequence=["#EF553B", "#636EFA"],
              markers=True,
              facet_row="patient_id" if not patient_id else None,
              title="Blood‑pressure trend")
fig.update_yaxes(title="mm Hg")  # Y-axis label
st.plotly_chart(fig, use_container_width=True)

# ------------------- Aggregated View: Last BP ------------------------- #
st.subheader("Last recorded BP per patient")
try:
    # Add random UUID to prevent caching (force fresh data)
    resp = requests.get(f"{API}/stats/last_bp?ts={uuid.uuid4()}")
    latest = resp.json()
    if isinstance(latest, list) and latest:
        # Display the latest stats in a data table
        st.dataframe(pd.DataFrame(latest))
    else:
        st.info("No recent blood-pressure data.")
except Exception as e:
    st.error(f"Could not load last BP stats: {e}")
