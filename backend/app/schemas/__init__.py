from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ======================== User Schemas ========================
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    school_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ======================== School Schemas ========================
class SchoolBase(BaseModel):
    name: str
    location: str
    pincode: str
    state: str
    district: str
    phone: Optional[str] = None
    principal_name: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ======================== Student Schemas ========================
class StudentBase(BaseModel):
    name: str
    roll_number: str
    date_of_birth: str
    gender: str
    class_name: str
    school_id: int
    family_income: str
    family_size: Optional[int] = None
    parents_education: Optional[str] = None
    has_digital_device: bool = False
    caste: Optional[str] = None
    religion: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    family_income: Optional[str] = None
    family_size: Optional[int] = None
    parents_education: Optional[str] = None
    has_digital_device: Optional[bool] = None
    is_dropout: Optional[bool] = None
    dropout_date: Optional[datetime] = None

class StudentResponse(StudentBase):
    id: int
    is_dropout: bool
    enrollment_date: datetime
    
    class Config:
        from_attributes = True

class StudentDetailResponse(StudentResponse):
    attendance_records: List = []
    grades: List = []
    health_records: List = []
    predictions: List = []
    alerts: List = []


# ======================== Attendance Schemas ========================
class AttendanceCreate(BaseModel):
    date: datetime
    present: bool
    reason_absent: Optional[str] = None

class AttendanceResponse(AttendanceCreate):
    id: int
    student_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ======================== Grade Schemas ========================
class GradeCreate(BaseModel):
    subject: str
    marks: float
    total_marks: float = 100
    exam_date: datetime
    exam_type: str
    term: Optional[str] = None

class GradeResponse(GradeCreate):
    id: int
    student_id: int
    percentage: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# ======================== Health Record Schemas ========================
class HealthRecordCreate(BaseModel):
    height: Optional[float] = None
    weight: Optional[float] = None
    has_menstrual_issues: bool = False
    menstrual_absences_count: int = 0
    malnutrition_status: Optional[str] = None
    health_issues: Optional[str] = None
    checkup_date: datetime

class HealthRecordResponse(HealthRecordCreate):
    id: int
    student_id: int
    bmi: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ======================== Prediction Schemas ========================
class PredictionResponse(BaseModel):
    id: int
    student_id: int
    risk_score: float
    risk_level: str
    confidence: float
    contributing_factors: str
    predicted_at: datetime
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    student_id: int


# ======================== Alert Schemas ========================
class AlertCreate(BaseModel):
    student_id: int
    alert_type: str
    title: str
    message: str
    channel: str
    recipient_phone: Optional[str] = None
    recipient_email: Optional[str] = None

class AlertResponse(AlertCreate):
    id: int
    status: str
    is_read: bool
    created_at: datetime
    sent_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ======================== Dashboard Schemas ========================
class DashboardStats(BaseModel):
    total_students: int
    total_high_risk: int
    total_medium_risk: int
    total_low_risk: int
    average_attendance: float
    average_grades: float
    recent_alerts_count: int
    intervention_success_rate: float


class RiskDistribution(BaseModel):
    low_count: int
    medium_count: int
    high_count: int
    low_percentage: float
    medium_percentage: float
    high_percentage: float
