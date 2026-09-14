from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import HealthRecordCreate, HealthRecordResponse
from app.services import HealthService

router = APIRouter(prefix="/api/health", tags=["health"])


@router.post("/{student_id}", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED)
async def add_health_record(student_id: int, health_record: HealthRecordCreate, db: Session = Depends(get_db)):
    """Add health record for a student"""
    try:
        return HealthService.add_health_record(db, student_id, health_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{student_id}", response_model=HealthRecordResponse)
async def get_latest_health_record(student_id: int, db: Session = Depends(get_db)):
    """Get latest health record for a student"""
    record = HealthService.get_latest_health_record(db, student_id)
    if not record:
        raise HTTPException(status_code=404, detail="No health records found")
    return record
