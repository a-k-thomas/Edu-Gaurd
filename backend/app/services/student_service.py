"""Student service for database operations"""
from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


class StudentService:
    """Service for student-related operations"""
    
    @staticmethod
    def create_student(db: Session, student: StudentCreate):
        """Create a new student"""
        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def get_student(db: Session, student_id: int):
        """Get student by ID"""
        return db.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def get_all_students(db: Session, school_id: int = None, skip: int = 0, limit: int = 100):
        """Get all students with optional filtering"""
        query = db.query(Student)
        
        if school_id:
            query = query.filter(Student.school_id == school_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_update: StudentUpdate):
        """Update student information"""
        db_student = db.query(Student).filter(Student.id == student_id).first()
        
        if not db_student:
            return None
        
        update_data = student_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def delete_student(db: Session, student_id: int):
        """Delete a student"""
        db_student = db.query(Student).filter(Student.id == student_id).first()
        
        if not db_student:
            return False
        
        db.delete(db_student)
        db.commit()
        return True
