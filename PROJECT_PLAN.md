# Dropout Risk Prediction System - Project Plan

## 1. Executive Summary
An AI/ML-powered early alert system to predict girl student dropout risk and enable timely intervention through automated alerts and stakeholder dashboards.

---

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    End Users                                │
│  (Teachers, Principals, NGOs, Social Workers, Parents)      │
└──────────────┬──────────────────────────────────────────────┘
               │
     ┌─────────┴──────────┬──────────────┐
     │                    │              │
┌────▼─────┐    ┌────────▼────────┐   ┌─▼────────────┐
│  Web App  │    │  Mobile App     │   │ SMS/WhatsApp │
│ (React.js)│    │ (React Native)  │   │   Alerts     │
└────┬─────┘    └────────┬────────┘   └──────────────┘
     │                    │
     └─────────┬──────────┘
               │
        ┌──────▼──────────┐
        │  API Gateway    │
        │  (FastAPI)      │
        └──────┬──────────┘
               │
     ┌─────────┴────────────────┬─────────────────────┐
     │                          │                     │
┌────▼────────────┐    ┌────────▼────────┐   ┌──────▼──────────┐
│ Prediction      │    │ Alert Service   │   │ Data Pipeline   │
│ Service         │    │ (Celery Queue)  │   │ (ETL)           │
│ (ML Models)     │    │                 │   │                 │
└────┬────────────┘    └────────┬────────┘   └──────┬──────────┘
     │                          │                     │
     └──────────────┬───────────┴─────────────────────┘
                    │
        ┌───────────▼──────────┬─────────────┐
        │                      │             │
    ┌───▼──────┐       ┌──────▼─────┐   ┌──▼──────────┐
    │ Database │       │ Redis Cache │   │ File Storage│
    │(PostgreSQL)      │ (Sessions)  │   │ (Reports)   │
    └──────────┘       └─────────────┘   └─────────────┘
```

### 2.2 Technology Stack

**Frontend:**
- React.js 18+ with TypeScript
- Material-UI (MUI) - Component Library
- Redux/Context API - State Management
- Material-Table - Data Tables
- Chart.js/Recharts - Visualizations
- Axios - HTTP Client
- React Native (for mobile) - Cross-platform

**Backend:**
- Python 3.9+
- FastAPI - Web Framework
- SQLAlchemy - ORM
- Scikit-learn / XGBoost - ML Models
- Celery - Task Queue for Alerts
- PostgreSQL - Database
- Redis - Cache & Message Broker
- Pandas - Data Processing

**DevOps & Deployment:**
- Docker & Docker Compose
- GitHub/GitLab - Version Control
- CI/CD Pipeline (GitHub Actions)
- AWS/Azure - Cloud Hosting

---

## 3. Project Structure

```
Real Dropout Predicter/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── student.py             # DB Models
│   │   │   ├── alert.py
│   │   │   └── school.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── student.py             # Pydantic Schemas
│   │   │   ├── prediction.py
│   │   │   └── alert.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── students.py            # API Endpoints
│   │   │   ├── predictions.py
│   │   │   ├── alerts.py
│   │   │   ├── dashboard.py
│   │   │   └── auth.py
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── model.py               # ML Model Loading
│   │   │   ├── preprocessor.py        # Data Preprocessing
│   │   │   ├── trainer.py             # Model Training
│   │   │   └── models/
│   │   │       └── dropout_model.pkl  # Trained Model
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── alert_service.py       # Alert Logic
│   │   │   ├── prediction_service.py  # Prediction Logic
│   │   │   ├── sms_service.py         # SMS/WhatsApp
│   │   │   └── email_service.py
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   └── celery_tasks.py        # Background Tasks
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_predictions.py
│   │   └── test_api.py
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── datasets/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── index.tsx
│   │   │   │   ├── RiskHeatmap.tsx
│   │   │   │   ├── AlertsList.tsx
│   │   │   │   └── StatisticsCards.tsx
│   │   │   ├── StudentManagement/
│   │   │   │   ├── StudentTable.tsx
│   │   │   │   ├── StudentDetail.tsx
│   │   │   │   └── AddStudent.tsx
│   │   │   ├── Predictions/
│   │   │   │   ├── PredictionChart.tsx
│   │   │   │   └── RiskIndicator.tsx
│   │   │   ├── Reports/
│   │   │   │   ├── GenerateReport.tsx
│   │   │   │   └── ReportViewer.tsx
│   │   │   ├── Auth/
│   │   │   │   ├── Login.tsx
│   │   │   │   └── Register.tsx
│   │   │   ├── Alerts/
│   │   │   │   ├── AlertCenter.tsx
│   │   │   │   └── AlertConfig.tsx
│   │   │   └── Common/
│   │   │       ├── Navbar.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── Loading.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── StudentsPage.tsx
│   │   │   ├── ReportsPage.tsx
│   │   │   └── SettingsPage.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── auth.ts
│   │   ├── store/
│   │   │   ├── actions/
│   │   │   ├── reducers/
│   │   │   └── index.ts
│   │   ├── styles/
│   │   │   ├── theme.ts
│   │   │   └── globals.css
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── Dockerfile
│
├── mobile/
│   └── (React Native project - optional)
│
├── docs/
│   ├── API.md
│   ├── DATABASE.md
│   ├── DEPLOYMENT.md
│   └── ML_MODEL.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 4. Core Features & Implementation Plan

### 4.1 Feature 1: Student Data Management
**Description:** Manage student records with demographic, attendance, academic, and health data

**Database Schema:**
```sql
Users (id, email, password, role, school_id)
Schools (id, name, location, pincode, state)
Students (id, name, dob, gender, school_id, family_income, caste, religion)
Attendance (id, student_id, date, present, reason_absent)
Grades (id, student_id, subject, marks, date)
HealthRecords (id, student_id, height, weight, menstrual_issues, date)
Dropouts (id, student_id, date, reason)
Predictions (id, student_id, risk_score, risk_level, created_at)
Alerts (id, student_id, alert_type, recipient_phone, status, created_at)
```

**API Endpoints:**
- `POST /api/students` - Add new student
- `GET /api/students` - List all students
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student
- `POST /api/students/{id}/attendance` - Record attendance
- `POST /api/students/{id}/grades` - Add grade
- `GET /api/students/{id}/health` - Get health records

### 4.2 Feature 2: ML Prediction Engine
**Description:** Predict dropout risk based on student data

**ML Model Pipeline:**
1. **Data Processing:**
   - Normalize numerical features
   - Encode categorical variables
   - Handle missing values
   - Feature engineering (rolling averages, trends)

2. **Model Architecture:**
   - Algorithm: XGBoost or LightGBM (high performance + interpretability)
   - Input Features: Attendance %, grade average, absence patterns, health indicators, socioeconomic factors
   - Output: Risk Score (0-100) & Risk Level (Low/Medium/High)

3. **Risk Levels:**
   - Low: 0-33 (Green)
   - Medium: 34-66 (Yellow)
   - High: 67-100 (Red)

**API Endpoints:**
- `POST /api/predictions/predict` - Predict for single student
- `POST /api/predictions/batch` - Predict for all students
- `GET /api/predictions/{student_id}` - Get prediction history
- `GET /api/predictions/stats` - Overall statistics

### 4.3 Feature 3: Interactive Dashboard
**Description:** Visualize student data and risk predictions

**Dashboard Components:**
1. **KPI Cards:**
   - Total Students
   - Students at Risk (High)
   - Intervention Success Rate
   - Recent Alerts

2. **Visualizations:**
   - Risk Distribution (Pie/Bar Chart)
   - Attendance vs Risk Correlation (Scatter)
   - Grade Trends (Line Chart)
   - Risk Heatmap by School/Class
   - Time Series: New At-Risk Students

3. **Filters:**
   - School/Class
   - Risk Level
   - Date Range
   - Intervention Status

### 4.4 Feature 4: Alert System
**Description:** Send automated alerts to stakeholders

**Alert Types:**
- **Red Alert (High Risk):** Immediate intervention needed
- **Yellow Alert (Medium Risk):** Monitor and counsel
- **Action Reminder:** Follow-up on previous alerts

**Notification Channels:**
- SMS (using Twilio or AWS SNS)
- WhatsApp (using Twilio WhatsApp API)
- Email
- In-app notifications

**Alert Recipients:**
- Teachers
- Principals
- NGO Workers
- Social Workers
- Parents

### 4.5 Feature 5: Reports & Analytics
**Description:** Generate detailed reports for stakeholders

**Report Types:**
1. **School-Level Report**
   - Students at risk summary
   - Intervention status
   - Success metrics

2. **Student-Risk Analysis**
   - Risk factors contributing
   - Recommendation for intervention
   - Historical trends

3. **Intervention Tracker**
   - Action taken
   - Outcome
   - Follow-up schedule

### 4.6 Feature 6: Multi-User Roles & Permissions
**Roles:**
1. **Admin** - Full system access
2. **Principal** - School-level operations
3. **Teacher** - Class-level student data
4. **NGO Worker** - Community intervention
5. **Social Worker** - Family support services
6. **Parent** - View child's profile

---

## 5. Data Sources & Solutions

### 5.1 Synthetic Data for Prototype
Since real student data is sensitive and hard to obtain:
- Generate realistic synthetic data using Python libraries
- Use parameters realistic to rural India context
- File: `backend/data/synthetic_generator.py`

### 5.2 Public Datasets
1. **ASER (Annual Status of Education Report)** - Survey data on Indian education
2. **NFHS (National Family Health Survey)** - Health & demographic data
3. **Government Education Statistics** - Public education datasets
4. **Kaggle Datasets:**
   - Student Dropout Prediction datasets
   - Education analytics datasets

### 5.3 Integration Points for Real Data
Once deployed:
- Direct integration with school management systems
- Data from government education portals
- Health records from school clinics
- Attendance systems (biometric/manual)

---

## 6. Implementation Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Phase 1: Setup** | 1-2 days | Project structure, DB schema, API skeleton |
| **Phase 2: Backend** | 3-4 days | APIs, ML pipeline, synthetic data |
| **Phase 3: Frontend** | 3-4 days | Dashboard, Auth, Student management |
| **Phase 4: Integration** | 2-3 days | Connect frontend-backend, testing |
| **Phase 5: Advanced Features** | 2-3 days | Alerts, Reports, Mobile responsiveness |
| **Phase 6: Deployment** | 1-2 days | Docker, CI/CD, cloud setup |

**Total: ~2-3 weeks for MVP**

---

## 7. Deployment Strategy

### 7.1 Development Environment
```bash
docker-compose up  # Starts all services locally
```

### 7.2 Production Deployment
- **Backend:** AWS EC2 / Azure App Service
- **Frontend:** Vercel / AWS CloudFront
- **Database:** AWS RDS PostgreSQL
- **Cache:** AWS ElastiCache (Redis)
- **Alerts Queue:** AWS SQS or self-hosted Redis

### 7.3 Security Considerations
- HTTPS/TLS for all communications
- JWT authentication
- Role-based access control (RBAC)
- Data anonymization
- GDPR/privacy compliance
- Rate limiting on APIs

---

## 8. Success Metrics
1. **Prediction Accuracy:** >85% precision for high-risk students
2. **Alert Response Time:** <5 minutes from detection to notification
3. **System Uptime:** 99.9% availability
4. **User Adoption:** >70% of teachers using dashboard
5. **Intervention Impact:** Measure dropout reduction (target 20% improvement)

---

## 9. Next Steps
1. ✅ Create project scaffolding
2. ⬜ Setup Backend - Python FastAPI
3. ⬜ Create synthetic dataset
4. ⬜ Train ML model
5. ⬜ Setup Frontend - React TypeScript
6. ⬜ Build dashboard components
7. ⬜ Implement alert system
8. ⬜ Testing & deployment

---

*Last Updated: 2026-03-05*
