from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import User, Student, Attendance, Grade, HealthRecord, Prediction, Alert
from app.schemas import (
    StudentCreate, StudentUpdate, AttendanceCreate, GradeCreate, HealthRecordCreate
)
from datetime import datetime
from app.utils.helpers import calculate_attendance_percentage, calculate_average_grade


class StudentService:
    """Service for student-related operations"""
    
    @staticmethod
    def create_student(db: Session, student: StudentCreate) -> Student:
        """Create a new student"""
        db_student = Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def get_student(db: Session, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        return db.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def get_all_students(db: Session, school_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Student]:
        """Get all students with optional filtering"""
        query = db.query(Student)
        if school_id:
            query = query.filter(Student.school_id == school_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_update: StudentUpdate) -> Optional[Student]:
        """Update student data"""
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            return None
        
        update_data = student_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def delete_student(db: Session, student_id: int) -> bool:
        """Delete student"""
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            return False
        
        db.delete(db_student)
        db.commit()
        return True


class AttendanceService:
    """Service for attendance-related operations"""
    
    @staticmethod
    def add_attendance(db: Session, student_id: int, attendance: AttendanceCreate) -> Attendance:
        """Add attendance record"""
        db_attendance = Attendance(student_id=student_id, **attendance.model_dump())
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    
    @staticmethod
    def get_student_attendance(db: Session, student_id: int, days: int = 90) -> List[Attendance]:
        """Get recent attendance for student"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date >= cutoff_date
        ).all()
    
    @staticmethod
    def get_attendance_percentage(db: Session, student_id: int, days: int = 90) -> float:
        """Calculate attendance percentage"""
        records = AttendanceService.get_student_attendance(db, student_id, days)
        return calculate_attendance_percentage(records)


class GradeService:
    """Service for grade-related operations"""
    
    @staticmethod
    def add_grade(db: Session, student_id: int, grade: GradeCreate) -> Grade:
        """Add grade record"""
        percentage = (grade.marks / grade.total_marks) * 100
        db_grade = Grade(
            student_id=student_id,
            percentage=percentage,
            **grade.model_dump()
        )
        db.add(db_grade)
        db.commit()
        db.refresh(db_grade)
        return db_grade
    
    @staticmethod
    def get_student_grades(db: Session, student_id: int, term: Optional[str] = None) -> List[Grade]:
        """Get grades for student"""
        query = db.query(Grade).filter(Grade.student_id == student_id)
        if term:
            query = query.filter(Grade.term == term)
        return query.all()
    
    @staticmethod
    def get_average_grade(db: Session, student_id: int) -> float:
        """Calculate average grade"""
        grades = GradeService.get_student_grades(db, student_id)
        return calculate_average_grade(grades)


class HealthService:
    """Service for health records"""
    
    @staticmethod
    def add_health_record(db: Session, student_id: int, health_record: HealthRecordCreate) -> HealthRecord:
        """Add health record"""
        from app.utils.helpers import calculate_bmi, get_malnutrition_status
        
        bmi = None
        if health_record.height and health_record.weight:
            bmi = calculate_bmi(health_record.height, health_record.weight)
        
        malnutrition_status = "unknown"
        if bmi:
            malnutrition_status = get_malnutrition_status(bmi)
        
        db_health = HealthRecord(
            student_id=student_id,
            bmi=bmi,
            malnutrition_status=malnutrition_status,
            **health_record.model_dump()
        )
        db.add(db_health)
        db.commit()
        db.refresh(db_health)
        return db_health
    
    @staticmethod
    def get_latest_health_record(db: Session, student_id: int) -> Optional[HealthRecord]:
        """Get latest health record"""
        return db.query(HealthRecord).filter(
            HealthRecord.student_id == student_id
        ).order_by(HealthRecord.checkup_date.desc()).first()


class AlertService:
    """Service for alert operations"""
    
    @staticmethod
    def create_alert(db: Session, alert_data: dict) -> Alert:
        """Create alert for student"""
        db_alert = Alert(**alert_data)
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
    
    @staticmethod
    def get_pending_alerts(db: Session) -> List[Alert]:
        """Get all pending alerts"""
        return db.query(Alert).filter(Alert.status == "pending").all()
    
    @staticmethod
    def mark_alert_sent(db: Session, alert_id: int) -> Optional[Alert]:
        """Mark alert as sent"""
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.status = "sent"
            alert.sent_at = datetime.utcnow()
            db.add(alert)
            db.commit()
            db.refresh(alert)
        return alert
