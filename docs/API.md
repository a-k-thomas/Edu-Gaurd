# API Documentation

Complete API reference for the Dropout Risk Prediction System.

## Base URL

**Development:** `http://localhost:8000`
**Production:** `https://api.dropout-predictor.com`

## Authentication

All endpoints (except `/health`) require JWT authentication.

```bash
# Get token
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}

# Use token
Authorization: Bearer {access_token}
```

## Endpoints

### Health Check
```
GET /health
No authentication required

Response (200 OK):
{
  "status": "ok",
  "app": "Dropout Risk Prediction System"
}
```

### Students

#### Create Student
```
POST /api/students
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "name": "Priya Sharma",
  "roll_number": "S11003456",
  "date_of_birth": "2008-03-15",
  "gender": "F",
  "school_id": 1,
  "class_name": "10",
  "family_income": "low",
  "family_size": 6,
  "parents_education": "secondary",
  "has_digital_device": false,
  "caste": "OBC",
  "religion": "Hindu"
}

Response (201 Created):
{
  "id": 1,
  "name": "Priya Sharma",
  "roll_number": "S11003456",
  "enrollment_date": "2024-03-05T10:30:00",
  ...
}
```

#### Get All Students
```
GET /api/students?school_id=1&skip=0&limit=100
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "name": "Priya Sharma",
    ...
  },
  ...
]
```

#### Get Single Student
```
GET /api/students/{student_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "name": "Priya Sharma",
  "attendance_records": [...],
  "grades": [...],
  "health_records": [...],
  ...
}
```

#### Update Student
```
PUT /api/students/{student_id}
Authorization: Bearer {token}

Request:
{
  "family_income": "medium",
  "has_digital_device": true
}

Response (200 OK):
{
  "id": 1,
  "name": "Priya Sharma",
  "family_income": "medium",
  "has_digital_device": true,
  ...
}
```

#### Delete Student
```
DELETE /api/students/{student_id}
Authorization: Bearer {token}

Response (204 No Content)
```

### Attendance

#### Add Attendance
```
POST /api/attendance/{student_id}
Authorization: Bearer {token}

Request:
{
  "date": "2024-03-05T09:00:00",
  "present": true,
  "reason_absent": null
}

Response (201 Created):
{
  "id": 1,
  "student_id": 1,
  "date": "2024-03-05T09:00:00",
  "present": true,
  ...
}
```

#### Get Attendance
```
GET /api/attendance/{student_id}?days=90
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "student_id": 1,
    "date": "2024-03-05",
    "present": true,
    ...
  },
  ...
]
```

#### Get Attendance Percentage
```
GET /api/attendance/percentage/{student_id}?days=90
Authorization: Bearer {token}

Response (200 OK):
{
  "attendance_percentage": 75.5
}
```

### Grades

#### Add Grade
```
POST /api/grades/{student_id}
Authorization: Bearer {token}

Request:
{
  "subject": "Mathematics",
  "marks": 85,
  "total_marks": 100,
  "exam_date": "2024-02-15T10:00:00",
  "exam_type": "midterm",
  "term": "1"
}

Response (201 Created):
{
  "id": 1,
  "student_id": 1,
  "subject": "Mathematics",
  "percentage": 85.0,
  ...
}
```

#### Get Grades
```
GET /api/grades/{student_id}?term=1
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "subject": "Mathematics",
    "marks": 85,
    "percentage": 85.0,
    ...
  },
  ...
]
```

#### Get Average Grade
```
GET /api/grades/average/{student_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "average_grade": 78.5
}
```

### Health Records

#### Add Health Record
```
POST /api/health/{student_id}
Authorization: Bearer {token}

Request:
{
  "height": 155.5,
  "weight": 48.0,
  "has_menstrual_issues": false,
  "menstrual_absences_count": 0,
  "health_issues": null,
  "checkup_date": "2024-02-28T14:00:00"
}

Response (201 Created):
{
  "id": 1,
  "student_id": 1,
  "height": 155.5,
  "weight": 48.0,
  "bmi": 19.87,
  "malnutrition_status": "normal",
  ...
}
```

#### Get Latest Health Record
```
GET /api/health/{student_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "student_id": 1,
  "bmi": 19.87,
  "malnutrition_status": "normal",
  ...
}
```

### Predictions

#### Predict Risk
```
POST /api/predictions/predict
Authorization: Bearer {token}

Request:
{
  "student_id": 1
}

Response (200 OK):
{
  "id": 1,
  "student_id": 1,
  "risk_score": 58.3,
  "risk_level": "medium",
  "confidence": 0.78,
  "contributing_factors": "low_attendance,poor_grades",
  "predicted_at": "2024-03-05T10:35:00Z"
}
```

#### Batch Predict
```
POST /api/predictions/batch-predict?school_id=1
Authorization: Bearer {token}

Response (200 OK):
{
  "message": "Batch prediction completed for 150 students"
}
```

#### Get Prediction History
```
GET /api/predictions/{student_id}
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "student_id": 1,
    "risk_score": 58.3,
    "risk_level": "medium",
    ...
  },
  ...
]
```

### Dashboard

#### Get Statistics
```
GET /api/dashboard/stats?school_id=1
Authorization: Bearer {token}

Response (200 OK):
{
  "total_students": 500,
  "total_high_risk": 125,
  "total_medium_risk": 225,
  "total_low_risk": 150,
  "average_attendance": 72.5,
  "average_grades": 65.3,
  "recent_alerts_count": 42,
  "intervention_success_rate": 0.68
}
```

#### Get Risk Distribution
```
GET /api/dashboard/risk-distribution?school_id=1
Authorization: Bearer {token}

Response (200 OK):
{
  "low_count": 150,
  "medium_count": 225,
  "high_count": 125,
  "low_percentage": 25.0,
  "medium_percentage": 45.0,
  "high_percentage": 25.0
}
```

#### Get Student Dashboard Details
```
GET /api/dashboard/student-details/{student_id}
Authorization: Bearer {token}

Response (200 OK):
{
  "student_id": 1,
  "name": "Priya Sharma",
  "attendance_percentage": 75.5,
  "average_grade": 78.5,
  "risk_score": 42.3,
  "risk_level": "medium",
  "family_income": "low",
  "has_digital_device": false
}
```

## Error Handling

All errors return appropriate HTTP status codes:

```
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity
500 Internal Server Error
```

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

```
- 100 requests per minute per IP
- 1000 requests per hour per token
- Batch endpoints: 10 per hour
```

## Pagination

```
GET /api/students?skip=0&limit=50

Parameters:
- skip: Number of records to skip (default: 0)
- limit: Number of records to return (default: 100, max: 500)

Response header:
X-Total-Count: 500  # Total number of records
```

## Data Formats

### Dates
ISO 8601 format with timezone:
```
"2024-03-05T10:30:00Z"
```

### Numbers
- Float: 75.5
- Integer: 1

### Booleans
```
true / false
```

## Testing Endpoints

### Using curl
```bash
curl -X POST http://localhost:8000/api/students \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "roll_number": "T001",
    ...
  }'
```

### Using Postman
1. Import base URL
2. Set Authorization > Bearer Token
3. Create requests for each endpoint

### Using Python
```python
import requests

headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:8000/api/students",
    headers=headers,
    json={
        "name": "Test User",
        ...
    }
)
```

---

*API Version: 1.0.0*
*Last Updated: March 5, 2026*
