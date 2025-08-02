# 🩺 Blood Pressure Tracker

A full-stack web application for tracking patient blood pressure readings. Built with **FastAPI** for the backend, **Streamlit** for the frontend, and **Redis** for caching. Data is stored in a local **SQLite** database. The application supports patient creation, measurement logging, and viewing of latest blood pressure statistics per patient.

---

## 🧩 Project Structure

```
.
├── api/                    # FastAPI backend
│   ├── main.py             # API routes and app entry
│   ├── crud.py             # Database logic
│   ├── database.py         # SQLAlchemy setup
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── cache.py            # Redis JSON caching helpers
│   └── seed.py             # DB initializer with sample data
│
├── streamlit/              # Frontend
│   └── app.py              # Streamlit UI (assumed main entry)
│
├── requirements_api.txt
├── requirements_streamlit.txt
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml
└── README.md
```

---

## 🚀 Features

- Create and list patients
- Add and retrieve blood pressure measurements
- View latest blood pressure per patient
- Data persistence via SQLite
- Redis caching for stats
- Full-stack deployment using Docker

---

## 🛠️ Setup Instructions

### 1. Requirements

- Docker and Docker Compose installed
- (Optional) Python 3.11+ for manual local setup

### 2. Clone the Repo

```bash
git clone https://github.com/<yourusername>/bp-tracker.git
cd bp-tracker
```

### 3. Start the App with Docker

```bash
docker-compose up --build
```

- FastAPI API: http://localhost:8000
- Streamlit UI: http://localhost:8501

---

## 📦 API Endpoints

Once running, access the FastAPI docs at [http://localhost:8000/docs](http://localhost:8000/docs)

### 🔹 Patients

| Method | Endpoint  | Description          |
| ------ | --------- | -------------------- |
| GET    | /patients | List all patients    |
| POST   | /patients | Create a new patient |

### 🔹 Measurements

| Method | Endpoint                     | Description                         |
| ------ | ---------------------------- | ----------------------------------- |
| GET    | /measurements?pid={id}       | List measurements (optional filter) |
| POST   | /patients/{pid}/measurements | Add measurement for a patient       |

### 🔹 Stats

| Method | Endpoint       | Description                       |
| ------ | -------------- | --------------------------------- |
| GET    | /stats/last_bp | Latest blood pressure per patient |

---

## 🧪 Sample Data

The application is preloaded with two sample patients:

- Alice Smith (F), born 1980-05-12
- Bob Jones (M), born 1975-01-03

Each has 10 blood pressure readings spanning the last 10 days.

---

## ⚙️ Configuration

Environment variables are managed in Docker Compose:

```yaml
environment:
  REDIS_HOST: redis
  REDIS_PORT: 6379
```

No `.env` file is required unless running manually.

---

## 📄 License

This project is licensed under the MIT License.

---

## ✨ Credits

Developed using:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Redis](https://redis.io/)

---

## 🗣️ Feedback

Feel free to open issues or submit pull requests to contribute to the project!
