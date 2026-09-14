"""Initialize database with mock data and train ML model"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Student, Attendance, Grade, HealthRecord, School, Prediction, RiskLevel
from data.synthetic_generator import SyntheticDataGenerator
import pickle
import pandas as pd
import numpy as np


def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def populate_mock_data():
    """Generate and populate mock data"""
    print("\nGenerating synthetic data...")
    
    # Generate synthetic data
    generator = SyntheticDataGenerator(seed=42)
    students_df = generator.generate_students(n_students=50, school_id=1)
    attendance_df = generator.generate_attendance(n_students=50, days_back=200)
    grades_df = generator.generate_grades(n_students=50, terms=3)
    health_df = generator.generate_health_records(n_students=50)
    
    db = SessionLocal()
    
    try:
        # Create school first
        school = School(
            name="Sample High School",
            location="Mumbai",
            pincode="400001",
            state="Maharashtra",
            district="Mumbai",
            phone="+91-9999999999",
            principal_name="Dr. Ramesh Kumar"
        )
        db.add(school)
        db.commit()
        print("✓ School created")
        
        # Insert students
        print("Inserting students...")
        for _, row in students_df.iterrows():
            student = Student(
                name=row['name'],
                roll_number=row['roll_number'],
                date_of_birth=row['date_of_birth'],
                gender=row['gender'],
                school_id=school.id,
                class_name=row['class_name'],
                family_income=row['family_income'],
                family_size=row['family_size'],
                parents_education=row['parents_education'],
                has_digital_device=row['has_digital_device'],
                caste=row['caste'],
                religion=row['religion'],
                is_dropout=False,
                enrollment_date=datetime.utcnow() - timedelta(days=180)
            )
            db.add(student)
        
        db.commit()
        print(f"✓ {len(students_df)} students inserted")
        
        # Get student IDs for references
        students = db.query(Student).all()
        student_id_map = {s.roll_number: s.id for s in students}
        
        # Insert attendance records
        print("Inserting attendance records...")
        for _, row in attendance_df.iterrows():
            student_roll = f"S1{row['student_id']:05d}"
            if row['student_id'] <= len(students):
                attendance = Attendance(
                    student_id=row['student_id'],
                    date=datetime.fromisoformat(row['date']),
                    present=row['present'],
                    reason_absent=row['reason_absent']
                )
                db.add(attendance)
        
        db.commit()
        print(f"✓ {len(attendance_df)} attendance records inserted")
        
        # Insert grades
        print("Inserting grades...")
        for _, row in grades_df.iterrows():
            if row['student_id'] <= len(students):
                grade = Grade(
                    student_id=row['student_id'],
                    subject=row['subject'],
                    marks=row['marks'],
                    total_marks=row['total_marks'],
                    percentage=row['percentage'],
                    exam_date=datetime.fromisoformat(row['exam_date']),
                    exam_type=row['exam_type'],
                    term=row['term']
                )
                db.add(grade)
        
        db.commit()
        print(f"✓ {len(grades_df)} grade records inserted")
        
        # Insert health records
        print("Inserting health records...")
        for _, row in health_df.iterrows():
            if row['student_id'] <= len(students):
                health = HealthRecord(
                    student_id=row['student_id'],
                    height=row['height'],
                    weight=row['weight'],
                    bmi=row['bmi'],
                    has_menstrual_issues=row['has_menstrual_issues'],
                    menstrual_absences_count=row['menstrual_absences_count'],
                    malnutrition_status=row['malnutrition_status'],
                    health_issues=row['health_issues'],
                    checkup_date=datetime.fromisoformat(row['checkup_date'])
                )
                db.add(health)
        
        db.commit()
        print(f"✓ {len(health_df)} health records inserted")
        
    finally:
        db.close()


def train_ml_model():
    """Generate predictions based on simple rules (without sklearn)"""
    print("\nGenerating predictions...")
    
    db = SessionLocal()
    
    try:
        # Get all students with their features
        students = db.query(Student).all()
        
        if not students:
            print("No students found. Skipping prediction generation.")
            return
        
        # Generate predictions for all students
        for student in students:
            # Get attendance percentage
            attendance_records = db.query(Attendance).filter(
                Attendance.student_id == student.id
            ).all()
            attendance_pct = len([a for a in attendance_records if a.present]) / max(len(attendance_records), 1) if attendance_records else 0.5
            
            # Get grades
            grades = db.query(Grade).filter(Grade.student_id == student.id).all()
            avg_grade = np.mean([g.percentage for g in grades]) if grades else 50
            
            # Get health info
            health = db.query(HealthRecord).filter(
                HealthRecord.student_id == student.id
            ).order_by(HealthRecord.checkup_date.desc()).first()
            
            is_malnourished = 1 if health and health.malnutrition_status in ['malnourished', 'severely_malnourished'] else 0
            
            # Simple risk scoring: based on attendance, grades, and health
            risk_score = 0
            
            if attendance_pct < 0.60:
                risk_score += 40
            elif attendance_pct < 0.75:
                risk_score += 20
            
            if avg_grade < 40:
                risk_score += 40
            elif avg_grade < 60:
                risk_score += 20
            
            if is_malnourished:
                risk_score += 15
            
            if student.family_income == 'low':
                risk_score += 10
            
            # Cap at 100
            risk_score = min(risk_score, 100)
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = RiskLevel.HIGH
                confidence = 0.85
            elif risk_score >= 40:
                risk_level = RiskLevel.MEDIUM
                confidence = 0.70
            else:
                risk_level = RiskLevel.LOW
                confidence = 0.75
            
            # Create prediction record
            prediction = Prediction(
                student_id=student.id,
                risk_score=risk_score,
                risk_level=risk_level,
                confidence=confidence,
                contributing_factors="attendance,grades,health"
            )
            db.add(prediction)
        
        db.commit()
        print(f"✓ Predictions generated for {len(students)} students")
        
    finally:
        db.close()


def main():
    """Run initialization"""
    print("=" * 50)
    print("Dropout Risk Prediction System - Initialization")
    print("=" * 50)
    
    try:
        init_database()
        populate_mock_data()
        train_ml_model()
        
        print("\n" + "=" * 50)
        print("✓ Initialization complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
