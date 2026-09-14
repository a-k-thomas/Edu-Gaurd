from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Student, Prediction, Alert
from app.schemas import DashboardStats, RiskDistribution
from typing import Dict, Any
from app.services import AttendanceService, GradeService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(school_id: int = None, db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    query = db.query(Student)
    if school_id:
        query = query.filter(Student.school_id == school_id)
    
    students = query.all()
    total_students = len(students)
    
    # Calculate risk distribution
    high_risk = db.query(Prediction).filter(Prediction.risk_level == "high").count()
    medium_risk = db.query(Prediction).filter(Prediction.risk_level == "medium").count()
    low_risk = db.query(Prediction).filter(Prediction.risk_level == "low").count()
    
    # Calculate average attendance and grades
    total_attendance = 0
    total_grades = 0
    count_attendance = 0
    count_grades = 0
    
    for student in students:
        attendance_pct = AttendanceService.get_attendance_percentage(db, student.id)
        if attendance_pct > 0:
            total_attendance += attendance_pct
            count_attendance += 1
        
        avg_grade = GradeService.get_average_grade(db, student.id)
        if avg_grade > 0:
            total_grades += avg_grade
            count_grades += 1
    
    average_attendance = total_attendance / count_attendance if count_attendance > 0 else 0
    average_grades = total_grades / count_grades if count_grades > 0 else 0
    
    # Recent alerts
    recent_alerts = db.query(Alert).filter(Alert.status == "pending").count()
    
    return DashboardStats(
        total_students=total_students,
        total_high_risk=high_risk,
        total_medium_risk=medium_risk,
        total_low_risk=low_risk,
        average_attendance=average_attendance,
        average_grades=average_grades,
        recent_alerts_count=recent_alerts,
        intervention_success_rate=0.0  # TODO: Calculate from interventions
    )


@router.get("/risk-distribution", response_model=RiskDistribution)
async def get_risk_distribution(school_id: int = None, db: Session = Depends(get_db)):
    """Get risk distribution across students"""
    query = db.query(Prediction)
    
    if school_id:
        query = query.join(Student).filter(Student.school_id == school_id)
    
    total = query.count()
    if total == 0:
        return RiskDistribution(
            low_count=0, medium_count=0, high_count=0,
            low_percentage=0, medium_percentage=0, high_percentage=0
        )
    
    low_count = query.filter(Prediction.risk_level == "low").count()
    medium_count = query.filter(Prediction.risk_level == "medium").count()
    high_count = query.filter(Prediction.risk_level == "high").count()
    
    return RiskDistribution(
        low_count=low_count,
        medium_count=medium_count,
        high_count=high_count,
        low_percentage=(low_count / total) * 100,
        medium_percentage=(medium_count / total) * 100,
        high_percentage=(high_count / total) * 100
    )


@router.get("/student-details/{student_id}")
async def get_student_dashboard_details(student_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed dashboard information for a specific student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    attendance_pct = AttendanceService.get_attendance_percentage(db, student_id)
    average_grade = GradeService.get_average_grade(db, student_id)
    
    prediction = db.query(Prediction).filter(Prediction.student_id == student_id).first()
    
    return {
        "student_id": student_id,
        "name": student.name,
        "attendance_percentage": attendance_pct,
        "average_grade": average_grade,
        "risk_score": prediction.risk_score if prediction else 0,
        "risk_level": prediction.risk_level if prediction else "unknown",
        "family_income": student.family_income,
        "has_digital_device": student.has_digital_device
    }
