<div align="center">
  <h1>🎓 EduGuard</h1>
  <p><strong>AI-Powered Student Dropout Risk Prediction System</strong></p>

  ![CI](https://github.com/a-k-thomas/Edu-Gaurd/actions/workflows/ci.yml/badge.svg)
  ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
  ![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
  ![License](https://img.shields.io/badge/License-MIT-green)
</div>

---

EduGuard is a full-stack early-alert platform that identifies students at risk of dropping out using an AI-powered heuristic scoring engine. Teachers, principals, and NGO workers get real-time dashboards, per-student risk diagnostics, and actionable intervention suggestions.

## ✨ Features

| Area | Details |
|---|---|
| **Dashboard** | Live KPI cards, risk-level donut chart, attendance/risk trend charts, high-risk radar table |
| **Student Management** | Add/edit profiles, track attendance & grades, view full history |
| **AI Risk Prediction** | Real-time per-student prediction + batch analysis for entire school |
| **Student Detail** | 5 tabbed analysis (Diagnostics, Academics, Attendance, Socio-Economic, Interventions) |
| **Reports** | Stacked bar charts by class, risk-factor breakdown, export/print |
| **Dark Mode** | System-preference-aware with manual toggle, persisted in `localStorage` |

## 🖥️ Tech Stack

**Backend** · FastAPI · SQLAlchemy · SQLite (dev) / PostgreSQL (prod) · Heuristic ML Scoring Engine

**Frontend** · React 18 · TypeScript · Vite · Material UI v5 · Recharts · Axios

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Clone the repository
```bash
git clone https://github.com/a-k-thomas/Edu-Gaurd.git
cd Edu-Gaurd
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Seed the database with synthetic data
python init_db.py

# Start the API server
uvicorn app.main:app --reload --port 8000
```

Backend runs at **http://localhost:8000** · Swagger docs at **http://localhost:8000/docs**

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:3000**

### 4. Using Docker Compose (alternative)
```bash
docker-compose up -d
```

## 📁 Project Structure

```
Edu-Gaurd/
├── .github/workflows/   # GitHub Actions CI (backend + frontend)
├── backend/
│   ├── app/
│   │   ├── main.py      # FastAPI entry point
│   │   ├── models/      # SQLAlchemy ORM models
│   │   ├── schemas/     # Pydantic request/response schemas
│   │   ├── routes/      # API endpoints
│   │   ├── services/    # Business logic
│   │   └── ml/          # Dropout risk scoring engine
│   ├── init_db.py       # Database seeder (synthetic data)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/  # Dashboard, Students, Reports, etc.
│       ├── context/     # Dark-mode context
│       ├── services/    # Axios API wrappers
│       └── styles/      # MUI theme (light/dark)
├── docs/                # API, ML model, deployment docs
└── docker-compose.yml
```

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create student |
| GET | `/api/students/{id}` | Get student |
| GET | `/api/dashboard/stats` | Dashboard KPIs |
| GET | `/api/dashboard/risk-distribution` | Risk breakdown |
| POST | `/api/predictions/predict` | Predict risk for one student |
| POST | `/api/predictions/batch-predict` | Batch predict all students |
| GET | `/api/attendance/{student_id}` | Attendance records |
| GET | `/api/grades/{student_id}` | Grade records |

Full docs available at `/docs` (Swagger UI) and `/redoc`.

## 🧠 How the Risk Score Works

The scoring engine (`backend/app/ml/__init__.py`) computes a **0–100 risk score** using weighted heuristics:

| Factor | Weight |
|---|---|
| Attendance rate | High |
| Average grade | High |
| Grade decline trend | Medium |
| Socioeconomic indicators (income, family size) | Medium |
| Digital device access | Low |
| Parental education level | Low |

**Risk Levels:** 🟢 Low (0–33) · 🟡 Medium (34–66) · 🔴 High (67–100)

## ⚙️ Configuration

Copy `backend/.env.example` to `backend/.env`:

```bash
cp backend/.env.example backend/.env
```

Key variables:

```env
DATABASE_URL=sqlite:///./dropout_db.db   # Default: SQLite (no extra setup)
SECRET_KEY=your-secret-key
DEBUG=True
```

See `.env.example` for optional PostgreSQL, Redis, Twilio, and SMTP settings.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'feat: add my feature'`)
4. Push and open a Pull Request

## 📄 License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
  Built with ❤️ to keep every student in school.
</div>
