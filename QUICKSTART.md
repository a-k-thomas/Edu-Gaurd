# Quick Start Guide

Get the Dropout Risk Prediction System running in minutes!

## 5-Minute Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### Step 1: Clone/Navigate to Project
```bash
cd "Real Dropout Predicter"
```

### Step 2: Start Services
```bash
docker-compose up -d
```

### Step 3: Wait for Services to Start
```bash
# Check status
docker-compose ps

# Wait ~30 seconds for database to initialize
```

### Step 4: Generate Sample Data
```bash
# Run in a new terminal
docker-compose exec backend python data/synthetic_generator.py
```

### Step 5: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Step 6: Test the System
1. Go to http://localhost:3000
2. View the dashboard with sample data
3. Check API docs at http://localhost:8000/docs

## 30-Minute Complete Setup (Manual)

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Redis 7+

### Backend Setup

#### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Setup Environment
```bash
# Copy example
cp .env.example .env

# Edit .env with your settings
# DATABASE_URL=postgresql://...
```

#### 4. Create Database
```bash
# If PostgreSQL is running locally
createdb dropout_db
createuser dropdown_user
# Set password: dropdown_pass
```

#### 5. Generate Synthetic Data
```bash
python data/synthetic_generator.py
```

#### 6. Start Backend
```bash
uvicorn app.main:app --reload --port 8000
```

Backend is now running on http://localhost:8000

### Frontend Setup

#### 1. Install Dependencies
```bash
cd ../frontend
npm install
```

#### 2. Start Development Server
```bash
npm run dev
```

Frontend is now running on http://localhost:3000

## Accessing the System

### Web Interface
- **URL**: http://localhost:3000
- **Description**: React dashboard showing risk predictions, alerts, and student management
- **Features**:
  - Dashboard with statistics
  - Student list and details
  - Risk visualizations
  - Alert management

### API Endpoints
- **Base URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Get all students (requires auth in production)
curl http://localhost:8000/api/students

# View complete API docs
# Visit http://localhost:8000/docs
```

## File Structure Overview

```
Real Dropout Predicter/
├── PROJECT_PLAN.md           ← Detailed project plan & architecture
├── README.md                 ← Main documentation
├── docker-compose.yml        ← Docker setup
├── .env.example              ← Environment template
│
├── backend/                  ← Python FastAPI Backend
│   ├── app/
│   │   ├── main.py          ← FastAPI app entry point
│   │   ├── models/          ← Database models
│   │   ├── schemas/         ← Request/response schemas
│   │   ├── routes/          ← API endpoints
│   │   ├── ml/              ← ML prediction models
│   │   └── services/        ← Business logic
│   ├── data/
│   │   └── synthetic_generator.py  ← Generate test data
│   ├── requirements.txt      ← Python dependencies
│   └── Dockerfile
│
├── frontend/                 ← React + TypeScript Frontend
│   ├── src/
│   │   ├── App.tsx          ← Main app component
│   │   ├── components/      ← Reusable UI components
│   │   ├── services/        ← API client
│   │   └── styles/          ← Theme & styling
│   ├── package.json         ← NPM dependencies
│   ├── vite.config.ts       ← Build configuration
│   └── Dockerfile
│
└── docs/                    ← Documentation
    ├── DATABASE.md          ← Database schema
    ├── ML_MODEL.md          ← ML model guide
    ├── API.md               ← API reference
    └── DEPLOYMENT.md        ← Deployment instructions
```

## Common Commands

### Backend
```bash
# Start backend (development)
cd backend
uvicorn app.main:app --reload

# Generate synthetic data
python data/synthetic_generator.py

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

### Frontend
```bash
# Start frontend (development)
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run lint
```

### Docker
```bash
# Start all services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild images
docker-compose build --no-cache

# Remove everything
docker-compose down -v
```

## Database

### Connection Info
- **Host**: localhost (Docker: postgres)
- **Port**: 5432
- **User**: dropout_user
- **Password**: dropout_pass
- **Database**: dropout_db

### Accessing Database
```bash
# Using psql
psql -h localhost -U dropout_user -d dropout_db

# Using DBeaver or pgAdmin
# Configure with above connection details
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Database Connection Failed
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check VITE_API_URL in vite.config.ts
- Browser console for CORS errors

### Redis Connection Issues
- Ensure Redis is running
- Check REDIS_URL in .env
- Redis should be on port 6379

## Next Steps

1. **Explore the Dashboard**
   - View risk predictions
   - Check student statistics
   - Review alerts

2. **Test APIs**
   - Use Swagger UI at /docs
   - Try creating students
   - Test predictions

3. **Customize**
   - Update Material UI theme
   - Modify ML model features
   - Add your own alerts

4. **Deploy**
   - See [DEPLOYMENT.md](docs/DEPLOYMENT.md)
   - Configure production environment
   - Setup SSL certificates

## Getting Help

### Documentation
- [PROJECT_PLAN.md](PROJECT_PLAN.md) - Detailed architecture & plan
- [README.md](README.md) - Complete project documentation
- [docs/API.md](docs/API.md) - API endpoint reference
- [docs/DATABASE.md](docs/DATABASE.md) - Database schema
- [docs/ML_MODEL.md](docs/ML_MODEL.md) - ML model info
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide

### Common Issues
- Check logs: `docker-compose logs`
- Verify ports: `netstat -an`
- Test connectivity: `curl http://localhost:8000/health`

### Support
- Open an issue on GitHub
- Check documentation first
- Enable debug mode for more logs

---

**Happy Coding! 🚀**
