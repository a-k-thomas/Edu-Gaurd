# Dropout Risk Prediction System

A comprehensive AI/ML-powered early alert system to predict dropout risk in school students and enable timely intervention through automated alerts and stakeholder dashboards.

## Overview

This system helps identify at-risk students using machine learning based on:
- Attendance patterns
- Academic performance
- Socioeconomic factors
- Health indicators
- Regional/cultural factors

## Quick Start

### Prerequisites
- Docker & Docker Compose
- OR:
  - Python 3.9+
  - Node.js 18+
  - PostgreSQL 13+
  - Redis 7+

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Swagger Docs: http://localhost:8000/docs
```

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate synthetic data
python -m app.data.synthetic_generator

# Start the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
Real Dropout Predicter/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── ml/             # ML models
│   │   └── main.py         # App entry point
│   ├── data/               # Data & synthetic data generator
│   └── requirements.txt
│
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API calls
│   │   ├── styles/        # Theme & styles
│   │   └── App.tsx        # Main App component
│   └── package.json
│
├── docker-compose.yml      # Docker setup
├── PROJECT_PLAN.md        # Detailed project plan
└── README.md (this file)
```

## API Endpoints

### Students
- `POST /api/students` - Create student
- `GET /api/students` - List students
- `GET /api/students/{id}` - Get student
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Attendance
- `POST /api/attendance/{student_id}` - Add attendance
- `GET /api/attendance/{student_id}` - Get attendance (last 90 days)
- `GET /api/attendance/percentage/{student_id}` - Get attendance %

### Grades
- `POST /api/grades/{student_id}` - Add grade
- `GET /api/grades/{student_id}` - Get grades
- `GET /api/grades/average/{student_id}` - Get average grade

### Health Records
- `POST /api/health/{student_id}` - Add health record
- `GET /api/health/{student_id}` - Get latest health record

### Predictions
- `POST /api/predictions/predict` - Predict risk for student
- `POST /api/predictions/batch-predict` - Predict for all students
- `GET /api/predictions/{student_id}` - Get prediction history

### Dashboard
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/risk-distribution` - Risk distribution
- `GET /api/dashboard/student-details/{student_id}` - Student details

## Data Sources

### For Development (Synthetic Data)
```bash
cd backend
python data/synthetic_generator.py
```

Generates:
- 500 students with realistic Indian school context
- 6 months of attendance records
- Grade data across subjects and terms
- Health records with BMI and malnutrition indicators

### For Production
1. **ASER (Annual Status of Education Report)**
   - URL: https://www.asercentre.org/
   - Public survey data on Indian education

2. **NFHS (National Family Health Survey)**
   - URL: https://dhsprogram.com/
   - Health & demographic data

3. **Government Education Portals**
   - State education department databases
   - School management systems
   - Government DISE portal

4. **Kaggle Datasets**
   - Student dropout prediction datasets
   - Education performance datasets

5. **Direct Integration**
   - School management systems
   - Biometric attendance systems
   - Health clinic records

## Machine Learning Model

### Model Architecture
**Algorithm:** XGBoost / LightGBM
**Input Features:**
- Attendance percentage (0-100%)
- Average grades (0-100)
- Menstrual health issues (binary)
- Malnutrition indicators
- Family income level
- Digital device access
- Grade drop rate
- Family size
- Parental education

**Output:**
- Risk Score: 0-100
- Risk Level: Low (0-33), Medium (34-66), High (67-100)
- Confidence: 0-1
- Contributing Factors: List of risk indicators

### Model Training
```bash
# After loading data
cd backend
python -m app.ml.trainer
```

## Features

### 1. Dashboard
- KPI cards (total students, at-risk counts)
- Risk distribution visualization
- Attendance & grade trends
- Student detail views
- Filterable by school/class/risk level

### 2. Student Management
- Add/edit student profiles
- Record attendance
- Track grades
- Health records
- View student history

### 3. Risk Prediction
- Real-time individual predictions
- Batch predictions for school
- Contributing factors analysis
- Prediction history

### 4. Alert System
- SM8 notifications (via Twilio)
- WhatsApp alerts
- Email notifications
- In-app notifications
- Alert history & status tracking

### 5. Reports
- School-level summary reports
- Student risk analysis
- Intervention tracking
- Exportable to PDF/Excel

### 6. Multi-User Access
- Role-based permissions
- Admin dashboard
- Principal reports
- Teacher class monitoring
- NGO/Social worker coordination
- Parent portal

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/db

# JWT
SECRET_KEY=your-secret-key

# Redis
REDIS_URL=redis://localhost:6379/0

# SMS (Twilio)
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=...

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
```

## Deployment

### Docker
```bash
docker-compose up -d
```

### AWS/Azure
1. RDS for PostgreSQL
2. ElastiCache for Redis
3. EC2/App Service for Backend
4. CloudFront/CDN for Frontend

### Scaling
- Use load balancers for backend
- CDN for static frontend assets
- Database replication
- Redis clustering

## Security

- ✅ HTTPS/TLS encryption
- ✅ JWT authentication & authorization
- ✅ Role-based access control (RBAC)
- ✅ Data anonymization & privacy
- ✅ Rate limiting on APIs
- ✅ Input validation & sanitization
- ✅ SQL injection prevention (SQLAlchemy ORM)

## Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit PR

## Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Advanced ML models (LSTM for time series)
- [ ] Real-time notifications
- [ ] Integration with school ERP systems
- [ ] Intervention outcome tracking
- [ ] Multi-language support
- [ ] Offline-first mobile app
- [ ] Video counseling integration

## Support & Contact

For issues, questions, or suggestions, please open an issue on GitHub.

## License

MIT License - See LICENSE file

---

**Last Updated:** March 5, 2026
**Version:** 1.0.0 (MVP)
