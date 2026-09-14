from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GradeCreate, GradeResponse
from app.services import GradeService
from typing import List

router = APIRouter(prefix="/api/grades", tags=["grades"])


@router.post("/{student_id}", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def add_grade(student_id: int, grade: GradeCreate, db: Session = Depends(get_db)):
    """Add a grade for a student"""
    try:
        return GradeService.add_grade(db, student_id, grade)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{student_id}", response_model=List[GradeResponse])
async def get_student_grades(student_id: int, term: str = None, db: Session = Depends(get_db)):
    """Get grades for a student"""
    grades = GradeService.get_student_grades(db, student_id, term)
    if not grades:
        raise HTTPException(status_code=404, detail="No grades found")
    return grades


@router.get("/average/{student_id}")
async def get_average_grade(student_id: int, db: Session = Depends(get_db)):
    """Get average grade for a student"""
    average = GradeService.get_average_grade(db, student_id)
    return {"average_grade": average}
