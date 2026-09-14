"""
Synthetic Data Generator for Dropout Risk Prediction
Generates realistic but anonymized student data for testing and development
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


class SyntheticDataGenerator:
    """Generate synthetic student datasets"""
    
    def __init__(self, seed=42):
        random.seed(seed)
        np.random.seed(seed)
    
    def generate_students(self, n_students=100, school_id=1):
        """Generate student records"""
        students = []
        
        for i in range(n_students):
            dob_year = random.randint(2005, 2015)
            dob_month = random.randint(1, 12)
            dob_day = random.randint(1, 28)
            
            student = {
                'name': f"Student_{i+1}",
                'roll_number': f"S{school_id}{i+1:05d}",
                'date_of_birth': f"{dob_year}-{dob_month:02d}-{dob_day:02d}",
                'gender': random.choice(['M', 'F']),
                'school_id': school_id,
                'class_name': random.choice(['6', '7', '8', '9', '10', '11', '12']),
                'family_income': random.choice(['low', 'medium', 'high']),
                'family_size': random.randint(2, 10),
                'parents_education': random.choice(['illiterate', 'primary', 'secondary', 'higher_secondary', 'college']),
                'has_digital_device': random.choice([True, False]),
                'caste': random.choice(['SC', 'ST', 'OBC', 'General', None]),
                'religion': random.choice(['Hindu', 'Muslim', 'Christian', 'Sikh', 'Buddhist']),
            }
            students.append(student)
        
        return pd.DataFrame(students)
    
    def generate_attendance(self, n_students=100, days_back=200):
        """Generate attendance records"""
        attendance_records = []
        
        for student_id in range(1, n_students + 1):
            # Some students have better attendance than others
            attendance_rate = random.uniform(0.5, 0.95)
            school_days = 0
            
            for day_offset in range(days_back):
                date = datetime.utcnow() - timedelta(days=day_offset)
                
                # Skip holidays/weekends
                if date.weekday() >= 5:
                    continue
                
                school_days += 1
                present = random.random() < attendance_rate
                
                record = {
                    'student_id': student_id,
                    'date': date.isoformat(),
                    'present': present,
                    'reason_absent': 'illness' if not present and random.random() < 0.3 else None
                }
                attendance_records.append(record)
        
        return pd.DataFrame(attendance_records)
    
    def generate_grades(self, n_students=100, terms=3):
        """Generate grade records"""
        grade_records = []
        subjects = ['Mathematics', 'Science', 'English', 'Social Studies', 'Hindi']
        
        for student_id in range(1, n_students + 1):
            # Some students perform better than others
            base_score = random.uniform(30, 95)
            
            for term in range(1, terms + 1):
                exam_date = datetime.utcnow() - timedelta(days=random.randint(30, 200))
                
                for subject in subjects:
                    # Add some variance
                    marks = max(0, min(100, base_score + np.random.normal(0, 10)))
                    
                    record = {
                        'student_id': student_id,
                        'subject': subject,
                        'marks': marks,
                        'total_marks': 100,
                        'percentage': marks,
                        'exam_date': exam_date.isoformat(),
                        'exam_type': 'midterm' if term < 3 else 'final',
                        'term': str(term)
                    }
                    grade_records.append(record)
        
        return pd.DataFrame(grade_records)
    
    def generate_health_records(self, n_students=100):
        """Generate health records"""
        health_records = []
        
        for student_id in range(1, n_students + 1):
            height = random.uniform(140, 180)  # cm
            weight = random.uniform(35, 75)     # kg
            bmi = weight / ((height / 100) ** 2)
            
            # Determine malnutrition status
            if bmi < 16.0:
                malnutrition = 'severely_malnourished'
            elif bmi < 18.5:
                malnutrition = 'malnourished'
            else:
                malnutrition = 'normal'
            
            # Menstrual-related (for female students)
            has_issues = random.choice([True, False]) if random.random() < 0.3 else False
            
            checkup_date = datetime.utcnow() - timedelta(days=random.randint(1, 100))
            
            record = {
                'student_id': student_id,
                'height': height,
                'weight': weight,
                'bmi': bmi,
                'has_menstrual_issues': has_issues,
                'menstrual_absences_count': random.randint(0, 6) if has_issues else 0,
                'malnutrition_status': malnutrition,
                'health_issues': None,
                'checkup_date': checkup_date.isoformat()
            }
            health_records.append(record)
        
        return pd.DataFrame(health_records)
    
    def generate_all_data(self, n_students=100, output_dir='backend/data'):
        """Generate all synthetic datasets"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating {n_students} students...")
        students_df = self.generate_students(n_students)
        students_df.to_csv(output_path / 'students.csv', index=False)
        print(f"✓ Generated students.csv")
        
        print(f"Generating attendance records...")
        attendance_df = self.generate_attendance(n_students)
        attendance_df.to_csv(output_path / 'attendance.csv', index=False)
        print(f"✓ Generated attendance.csv")
        
        print(f"Generating grades...")
        grades_df = self.generate_grades(n_students)
        grades_df.to_csv(output_path / 'grades.csv', index=False)
        print(f"✓ Generated grades.csv")
        
        print(f"Generating health records...")
        health_df = self.generate_health_records(n_students)
        health_df.to_csv(output_path / 'health_records.csv', index=False)
        print(f"✓ Generated health_records.csv")
        
        print(f"\nAll synthetic data generated successfully in {output_path}/")
        return {
            'students': students_df,
            'attendance': attendance_df,
            'grades': grades_df,
            'health': health_df
        }


if __name__ == '__main__':
    # Generate sample data
    generator = SyntheticDataGenerator()
    generator.generate_all_data(n_students=500)
