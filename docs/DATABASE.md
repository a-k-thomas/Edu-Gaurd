# Database Schema & Design

## Entity Relationship Diagram

```
Users ← → Schools
  ↑              ↓
  ├─ Alerts ← Students
  │             ├─ Attendance
  │             ├─ Grades
  │             ├─ HealthRecords
  │             ├─ Predictions
  │             └─ Alerts → Interventions
  │
  └─ Interventions
```

## Tables

### Users
User authentication and role management

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  role VARCHAR(50),  -- admin, principal, teacher, ngo_worker, social_worker, parent
  school_id INTEGER REFERENCES schools(id),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_school_id ON users(school_id);
```

### Schools
School information and metadata

```sql
CREATE TABLE schools (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  location VARCHAR(255),
  pincode VARCHAR(10),
  state VARCHAR(100),
  district VARCHAR(100),
  phone VARCHAR(20),
  principal_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_schools_state ON schools(state);
CREATE INDEX idx_schools_district ON schools(district);
```

### Students
Student demographic and enrollment data

```sql
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  roll_number VARCHAR(100) UNIQUE NOT NULL,
  date_of_birth VARCHAR(10),
  gender VARCHAR(10),  -- M, F, Other
  school_id INTEGER NOT NULL REFERENCES schools(id),
  class_name VARCHAR(5),  -- 6, 7, 8, 9, 10, 11, 12
  family_income VARCHAR(50),  -- low, medium, high
  family_size INTEGER,
  parents_education VARCHAR(100),
  has_digital_device BOOLEAN DEFAULT false,
  caste VARCHAR(100),
  religion VARCHAR(100),
  is_dropout BOOLEAN DEFAULT false,
  dropout_date TIMESTAMP,
  enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_school_id ON students(school_id);
CREATE INDEX idx_students_class ON students(class_name);
CREATE INDEX idx_students_is_dropout ON students(is_dropout);
```

### Attendance
Daily attendance records

```sql
CREATE TABLE attendance (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  date TIMESTAMP NOT NULL,
  present BOOLEAN,
  reason_absent VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attendance_student_id ON attendance(student_id);
CREATE INDEX idx_attendance_date ON attendance(date);
```

### Grades
Academic grades and exam records

```sql
CREATE TABLE grades (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  subject VARCHAR(100) NOT NULL,
  marks FLOAT NOT NULL,
  total_marks FLOAT DEFAULT 100,
  percentage FLOAT,
  exam_date TIMESTAMP,
  exam_type VARCHAR(50),  -- midterm, final, unit_test
  term VARCHAR(10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_grades_exam_date ON grades(exam_date);
```

### HealthRecords
Student health indicators and medical data

```sql
CREATE TABLE health_records (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  height FLOAT,  -- cm
  weight FLOAT,  -- kg
  bmi FLOAT,
  has_menstrual_issues BOOLEAN DEFAULT false,
  menstrual_absences_count INTEGER DEFAULT 0,
  malnutrition_status VARCHAR(50),  -- normal, malnourished, severely_malnourished
  health_issues TEXT,
  checkup_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_health_records_student_id ON health_records(student_id);
```

### Predictions
ML model predictions and risk scores

```sql
CREATE TABLE predictions (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  risk_score FLOAT,  -- 0-100
  risk_level VARCHAR(20),  -- low, medium, high
  confidence FLOAT,  -- 0-1
  contributing_factors TEXT,  -- comma-separated: low_attendance,poor_grades,...
  predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictions_student_id ON predictions(student_id);
CREATE INDEX idx_predictions_risk_level ON predictions(risk_level);
```

### Alerts
System alerts sent to stakeholders

```sql
CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  recipient_id INTEGER REFERENCES users(id),
  alert_type VARCHAR(50),  -- red_alert, yellow_alert, action_reminder
  title VARCHAR(255),
  message TEXT,
  channel VARCHAR(50),  -- sms, email, whatsapp, in_app
  recipient_phone VARCHAR(20),
  recipient_email VARCHAR(255),
  status VARCHAR(20) DEFAULT 'pending',  -- pending, sent, failed, read
  is_read BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sent_at TIMESTAMP
);

CREATE INDEX idx_alerts_student_id ON alerts(student_id);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
```

### Interventions
Tracking of interventions and follow-ups

```sql
CREATE TABLE interventions (
  id SERIAL PRIMARY KEY,
  student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
  alert_id INTEGER REFERENCES alerts(id),
  intervention_type VARCHAR(100),  -- counseling, financial_aid, home_visit, medical
  description TEXT,
  status VARCHAR(50),  -- planned, in_progress, completed
  assigned_to VARCHAR(100),  -- teacher, ngo, social_worker
  expected_completion_date TIMESTAMP,
  completion_date TIMESTAMP,
  outcome TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_interventions_student_id ON interventions(student_id);
CREATE INDEX idx_interventions_status ON interventions(status);
```

## Data Types & Constraints

- **Email**: Must be unique and valid
- **Dates**: Stored as TIMESTAMP with timezone
- **Risk Score**: 0-100 Float
- **Attendance Percentage**: 0-100 Float
- **Boolean fields**: True/False
- **Text fields**: Support special characters and Unicode

## Performance Considerations

1. **Indexing Strategy**
   - Index foreign keys for fast joins
   - Index frequently filtered fields (school_id, student_id, risk_level)
   - Index date fields for range queries

2. **Partitioning (Future)**
   - Partition attendance/grades by student_id
   - Partition alerts by created_date
   - Enables better query performance at scale

3. **Materialized Views (Future)**
   - Student statistics view
   - School-level summary view
   - Prediction statistics view

## Backup & Disaster Recovery

```bash
# Backup
pg_dump -U dropout_user dropout_db > backup.sql

# Restore
psql -U dropout_user dropout_db < backup.sql

# Automated backups
# Use AWS RDS automated backups or pg_basebackup
```

## Data Privacy & Security

- Store hashed passwords (bcrypt)
- Encrypt PII at rest (optional)
- Row-level security for multi-tenant features
- GDPR-compliant data retention policies
- Regular security audits

---

*Schema Version: 1.0.0*
