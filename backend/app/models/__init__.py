from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # admin, principal, teacher, ngo_worker, social_worker, parent
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    school = relationship("School", back_populates="users")
    alerts = relationship("Alert", back_populates="recipient")


class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    pincode = Column(String)
    state = Column(String)
    district = Column(String)
    phone = Column(String, nullable=True)
    principal_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="school")
    students = relationship("Student", back_populates="school")


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    roll_number = Column(String, unique=True, index=True)
    date_of_birth = Column(String)
    gender = Column(String)  # M, F, Other
    school_id = Column(Integer, ForeignKey("schools.id"))
    class_name = Column(String)  # 6, 7, 8, 9, 10, 11, 12
    
    # Socioeconomic
    family_income = Column(String)  # low, medium, high
    family_size = Column(Integer, nullable=True)
    parents_education = Column(String, nullable=True)
    has_digital_device = Column(Boolean, default=False)
    
    # Additional factors
    caste = Column(String, nullable=True)
    religion = Column(String, nullable=True)
    is_dropout = Column(Boolean, default=False)
    dropout_date = Column(DateTime, nullable=True)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    
    school = relationship("School", back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="student", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="student", cascade="all, delete-orphan")


class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, index=True)
    present = Column(Boolean)  # True = present, False = absent
    reason_absent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="attendance_records")


class Grade(Base):
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    marks = Column(Float)
    total_marks = Column(Float, default=100)
    percentage = Column(Float)
    exam_date = Column(DateTime)
    exam_type = Column(String)  # midterm, final, unit_test
    term = Column(String, nullable=True)  # 1, 2, 3, etc
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="grades")


class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    height = Column(Float, nullable=True)  # cm
    weight = Column(Float, nullable=True)  # kg
    bmi = Column(Float, nullable=True)
    has_menstrual_issues = Column(Boolean, default=False)
    menstrual_absences_count = Column(Integer, default=0)
    malnutrition_status = Column(String, nullable=True)  # normal, malnourished, severely_malnourished
    health_issues = Column(String, nullable=True)  # comma-separated
    checkup_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="health_records")


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    risk_score = Column(Float)  # 0-100
    risk_level = Column(Enum(RiskLevel))
    confidence = Column(Float)  # 0-1
    predicted_at = Column(DateTime, default=datetime.utcnow)
    
    # Contributing factors (JSON-like structure, stored as STRING)
    contributing_factors = Column(String)  # e.g., "low_attendance,poor_grades,health_issues"
    
    student = relationship("Student", back_populates="predictions")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    alert_type = Column(String)  # red_alert, yellow_alert, action_reminder
    title = Column(String)
    message = Column(String)
    channel = Column(String)  # sms, email, whatsapp, in_app
    recipient_phone = Column(String, nullable=True)
    recipient_email = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, sent, failed, read
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    
    student = relationship("Student", back_populates="alerts")
    recipient = relationship("User", back_populates="alerts")


class Intervention(Base):
    __tablename__ = "interventions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    intervention_type = Column(String)  # counseling, financial_aid, home_visit, medical
    description = Column(String)
    status = Column(String)  # planned, in_progress, completed
    assigned_to = Column(String)  # teacher, ngo, social_worker
    expected_completion_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    outcome = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
