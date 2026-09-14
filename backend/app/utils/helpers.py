from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def calculate_attendance_percentage(attendance_records: list) -> float:
    """Calculate attendance percentage from records"""
    if not attendance_records:
        return 0.0
    
    present_count = sum(1 for record in attendance_records if record.present)
    return (present_count / len(attendance_records)) * 100


def calculate_average_grade(grades: list) -> float:
    """Calculate average grade from grade records"""
    if not grades:
        return 0.0
    
    return sum(grade.percentage for grade in grades) / len(grades)


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate BMI (height in cm, weight in kg)"""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def get_malnutrition_status(bmi: float, age: int = None) -> str:
    """
    Determine malnutrition status based on BMI
    For school-age children, BMI values are age and sex-dependent
    Simplified version using general guidelines
    """
    if bmi < 16.0:
        return "severely_malnourished"
    elif bmi < 18.5:
        return "malnourished"
    else:
        return "normal"


def extract_risk_factors(student_data: dict, prediction: dict) -> list:
    """Extract contributing factors for risk prediction"""
    factors = []
    
    # Check attendance
    if student_data.get('attendance_percentage', 100) < 70:
        factors.append("low_attendance")
    
    # Check grades
    if student_data.get('average_grade', 100) < 50:
        factors.append("poor_grades")
    
    # Check health
    if student_data.get('has_menstrual_issues'):
        factors.append("menstrual_health_issues")
    if student_data.get('malnutrition_status') != 'normal':
        factors.append("malnutrition")
    
    # Check socioeconomic
    if student_data.get('family_income') == 'low':
        factors.append("low_family_income")
    if not student_data.get('has_digital_device'):
        factors.append("no_digital_device")
    
    return factors
