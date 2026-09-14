from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import StudentCreate, StudentResponse, StudentDetailResponse, StudentUpdate
from app.services import StudentService
from datetime import datetime

router = APIRouter(prefix="/api/students", tags=["students"])


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    try:
        return StudentService.create_student(db, student)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{student_id}", response_model=StudentDetailResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get student details"""
    student = StudentService.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/", response_model=List[StudentResponse])
async def get_students(school_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all students with optional filtering"""
    return StudentService.get_all_students(db, school_id, skip, limit)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    """Update student information"""
    updated_student = StudentService.update_student(db, student_id, student_update)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student"""
    if not StudentService.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
