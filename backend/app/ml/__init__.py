import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
import os

# Path to saved model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "dropout_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")


class DropoutPredictor:
    """ML Model for predicting dropout risk"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = [
            'attendance_percentage',
            'average_grade',
            'menstrual_absences_count',
            'has_menstrual_issues',
            'malnutrition_score',  # 0: normal, 1: malnourished, 2: severely
            'family_income_score',  # 0: high, 1: medium, 2: low
            'has_digital_device',
            'grade_drop_rate',  # Percentage change in grades over time
            'family_size',
            'parents_education_score'  # 0: high, 1: medium, 2: low/none
        ]
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model"""
        # For MVP, we'll create a simple model if file doesn't exist
        # In production, load actual trained model
        pass
    
    def preprocess_features(self, student_data: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Convert student data to ML features
        Returns: processed features array and feature dict for interpretation
        """
        features_dict = {}
        
        # Attendance (0-100%)
        features_dict['attendance_percentage'] = student_data.get('attendance_percentage', 50)
        
        # Average grade (0-100)
        features_dict['average_grade'] = student_data.get('average_grade', 50)
        
        # Health factors
        features_dict['menstrual_absences_count'] = student_data.get('menstrual_absences_count', 0)
        features_dict['has_menstrual_issues'] = float(student_data.get('has_menstrual_issues', False))
        
        # Malnutrition mapping
        malnutrition_map = {
            'normal': 0,
            'malnourished': 1,
            'severely_malnourished': 2,
            None: 0.5
        }
        malnutrition_status = student_data.get('malnutrition_status', 'normal')
        features_dict['malnutrition_score'] = malnutrition_map.get(malnutrition_status, 0.5)
        
        # Family income mapping
        income_map = {
            'high': 0,
            'medium': 1,
            'low': 2
        }
        family_income = student_data.get('family_income', 'medium')
        features_dict['family_income_score'] = income_map.get(family_income, 1)
        
        # Digital device
        features_dict['has_digital_device'] = float(student_data.get('has_digital_device', False))
        
        # Grade drop rate (negative value if grades improving)
        features_dict['grade_drop_rate'] = student_data.get('grade_drop_rate', 0)
        
        # Family size
        features_dict['family_size'] = student_data.get('family_size', 5)
        
        # Parents education mapping
        education_map = {
            'illiterate': 2,
            'primary': 2,
            'secondary': 1,
            'higher_secondary': 1,
            'college': 0,
            'postgraduate': 0,
            None: 1
        }
        parents_education = student_data.get('parents_education', None)
        features_dict['parents_education_score'] = education_map.get(parents_education, 1)
        
        # Create feature vector
        feature_vector = np.array([features_dict[name] for name in self.feature_names]).reshape(1, -1)
        
        return feature_vector, features_dict
    
    def predict_risk(self, student_data: Dict[str, Any]) -> Tuple[float, str, float, list]:
        """
        Predict dropout risk for a student
        Returns: (risk_score, risk_level, confidence, contributing_factors)
        """
        feature_vector, features_dict = self.preprocess_features(student_data)
        
        # Simple heuristic-based scoring (MVP version)
        # In production, use actual ML model prediction
        risk_score = self._calculate_risk_score(features_dict)
        
        # Determine risk level
        if risk_score >= 67:
            risk_level = "high"
        elif risk_score >= 34:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Confidence is higher for extreme scores
        confidence = min(abs(risk_score - 50) / 50 + 0.5, 1.0)
        
        # Get contributing factors
        factors = self._get_contributing_factors(features_dict)
        
        return risk_score, risk_level, confidence, factors
    
    def _calculate_risk_score(self, features: Dict[str, float]) -> float:
        """Calculate risk score using weighted formula"""
        score = 0.0
        
        # Attendance impact (30% weight)
        attendance = features.get('attendance_percentage', 50)
        score += (100 - attendance) * 0.30 / 100
        
        # Grade impact (30% weight)
        grades = features.get('average_grade', 50)
        score += (100 - grades) * 0.30 / 100
        
        # Malnutrition (15% weight)
        malnutrition = features.get('malnutrition_score', 0)
        score += malnutrition * 15 / 2 / 100
        
        # Family income (15% weight)
        income = features.get('family_income_score', 1)
        score += income * 15 / 2 / 100
        
        # Menstrual issues bonus (5% weight)
        menstrual = features.get('has_menstrual_issues', 0)
        score += menstrual * 5
        
        # Grade drop rate (5% weight)
        grade_drop = features.get('grade_drop_rate', 0)
        score += min(grade_drop * 0.05, 5)
        
        # No digital device (slightly increases risk)
        device = features.get('has_digital_device', 0)
        if device == 0:
            score += 2
        
        # Normalize to 0-100
        return min(score * 100, 100)
    
    def _get_contributing_factors(self, features: Dict[str, float]) -> list:
        """Extract top contributing factors"""
        factors = []
        
        if features.get('attendance_percentage', 100) < 70:
            factors.append("low_attendance")
        
        if features.get('average_grade', 100) < 50:
            factors.append("poor_grades")
        
        if features.get('has_menstrual_issues'):
            factors.append("menstrual_health_issues")
        
        if features.get('malnutrition_score', 0) > 0:
            factors.append("malnutrition")
        
        if features.get('family_income_score', 1) >= 1:
            factors.append("low_family_income")
        
        if not features.get('has_digital_device'):
            factors.append("no_digital_device")
        
        return factors
