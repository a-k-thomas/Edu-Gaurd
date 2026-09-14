from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, Prediction
from app.schemas import PredictionResponse, PredictionRequest
from app.ml import DropoutPredictor
from app.services import AttendanceService, GradeService, HealthService
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

# Initialize predictor
predictor = DropoutPredictor()


@router.post("/predict", response_model=PredictionResponse)
async def predict_student_risk(request: PredictionRequest, db: Session = Depends(get_db)):
    """Predict dropout risk for a single student"""
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Gather student data
    attendance_pct = AttendanceService.get_attendance_percentage(db, student.id)
    average_grade = GradeService.get_average_grade(db, student.id)
    health_record = HealthService.get_latest_health_record(db, student.id)
    
    student_data = {
        "attendance_percentage": attendance_pct,
        "average_grade": average_grade,
        "menstrual_absences_count": health_record.menstrual_absences_count if health_record else 0,
        "has_menstrual_issues": health_record.has_menstrual_issues if health_record else False,
        "malnutrition_status": health_record.malnutrition_status if health_record else "normal",
        "family_income": student.family_income,
        "has_digital_device": student.has_digital_device,
        "family_size": student.family_size or 5,
        "parents_education": student.parents_education,
        "grade_drop_rate": 0  # TODO: Calculate from grade trends
    }
    
    # Get prediction
    risk_score, risk_level, confidence, factors = predictor.predict_risk(student_data)
    
    # Save to database
    prediction = Prediction(
        student_id=student.id,
        risk_score=risk_score,
        risk_level=risk_level,
        confidence=confidence,
        contributing_factors=",".join(factors),
        predicted_at=datetime.utcnow()
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return prediction


@router.post("/batch-predict")
async def batch_predict_all(school_id: int = None, db: Session = Depends(get_db)):
    """Predict risk for all students in a school"""
    query = db.query(Student)
    if school_id:
        query = query.filter(Student.school_id == school_id)
    
    students = query.all()
    predictions = []
    
    for student in students:
        attendance_pct = AttendanceService.get_attendance_percentage(db, student.id)
        average_grade = GradeService.get_average_grade(db, student.id)
        health_record = HealthService.get_latest_health_record(db, student.id)
        
        student_data = {
            "attendance_percentage": attendance_pct,
            "average_grade": average_grade,
            "menstrual_absences_count": health_record.menstrual_absences_count if health_record else 0,
            "has_menstrual_issues": health_record.has_menstrual_issues if health_record else False,
            "malnutrition_status": health_record.malnutrition_status if health_record else "normal",
            "family_income": student.family_income,
            "has_digital_device": student.has_digital_device,
            "family_size": student.family_size or 5,
            "parents_education": student.parents_education
        }
        
        risk_score, risk_level, confidence, factors = predictor.predict_risk(student_data)
        
        # Delete old prediction if exists
        old_prediction = db.query(Prediction).filter(Prediction.student_id == student.id).first()
        if old_prediction:
            db.delete(old_prediction)
        
        # Create new prediction
        prediction = Prediction(
            student_id=student.id,
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=confidence,
            contributing_factors=",".join(factors)
        )
        db.add(prediction)
        predictions.append(prediction)
    
    db.commit()
    return {"message": f"Batch prediction completed for {len(predictions)} students"}


@router.get("/{student_id}", response_model=List[PredictionResponse])
async def get_prediction_history(student_id: int, db: Session = Depends(get_db)):
    """Get prediction history for a student"""
    predictions = db.query(Prediction).filter(Prediction.student_id == student_id).all()
    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found")
    return predictions
