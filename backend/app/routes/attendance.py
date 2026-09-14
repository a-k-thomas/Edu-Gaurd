from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AttendanceCreate, AttendanceResponse
from app.services import AttendanceService
from typing import List

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("/{student_id}", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def add_attendance(student_id: int, attendance: AttendanceCreate, db: Session = Depends(get_db)):
    """Add attendance record for a student"""
    try:
        return AttendanceService.add_attendance(db, student_id, attendance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{student_id}", response_model=List[AttendanceResponse])
async def get_student_attendance(student_id: int, days: int = 90, db: Session = Depends(get_db)):
    """Get attendance records for a student"""
    records = AttendanceService.get_student_attendance(db, student_id, days)
    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found")
    return records


@router.get("/percentage/{student_id}")
async def get_attendance_percentage(student_id: int, days: int = 90, db: Session = Depends(get_db)):
    """Get attendance percentage for a student"""
    percentage = AttendanceService.get_attendance_percentage(db, student_id, days)
    return {"attendance_percentage": percentage}
