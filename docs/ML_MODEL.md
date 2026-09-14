# Machine Learning Model Guide

## Overview

The ML model predicts dropout risk by analyzing student data and assigning a risk score (0-100) along with contributing factors.

## Model Pipeline

### 1. Data Collection
```python
for student in students:
    data = {
        'attendance_percentage': calculate_attendance(student),
        'average_grade': calculate_avg_grades(student),
        'menstrual_absences_count': count_menstrual_absences(student),
        'malnutrition_status': assess_nutrition(student),
        'family_income': student.family_income,
        'has_digital_device': student.has_digital_device,
        ...
    }
```

### 2. Feature Engineering
```python
- Normalize attendance (0-100%)
- Encode categorical variables (family_income: high=0, medium=1, low=2)
- Calculate BMI from height/weight
- Determine malnutrition status (0=normal, 1=malnourished, 2=severe)
- Compute grade trends (improvement/decline)
- Calculate grade drop rate
```

### 3. Model Training

**Algorithm:** XGBoost (Gradient Boosting)

**Why XGBoost?**
- High speed and efficiency
- Handles non-linear relationships
- Feature importance ranking
- Handles missing values well
- Production-ready

**Hyperparameters:**
```python
xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss'
)
```

**Training Code:**
```python
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = XGBClassifier(n_estimators=100, max_depth=6)
model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"Accuracy: {score:.2%}")

# Save model
import pickle
with open('dropout_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

### 4. Risk Scoring Logic

**Weight Distribution:**
```
Attendance:           30%
Grades:              30%
Malnutrition:        15%
Family Income:       15%
Menstrual Issues:     5%
Grade Drop Rate:      5%
```

**Calculation:**
```python
risk_score = (
    (100 - attendance) * 0.30 +
    (100 - grades) * 0.30 +
    malnutrition_score * 0.15 +
    family_income_score * 0.15 +
    menstrual_issues * 0.05 +
    grade_drop_rate * 0.05
)

# Normalize to 0-100
risk_score = max(0, min(risk_score, 100))
```

### 5. Risk Level Classification
```
risk_score < 33:   LOW RISK        🟢
33 <= score < 67:  MEDIUM RISK     🟡
score >= 67:       HIGH RISK       🔴
```

## Contributing Factors Analysis

```python
factors = []

if attendance < 70:
    factors.append("low_attendance")

if avg_grade < 50:
    factors.append("poor_grades")

if menstrual_issues:
    factors.append("menstrual_health_issues")

if malnutrition_score > 0:
    factors.append("malnutrition")

if family_income == 'low':
    factors.append("low_family_income")

if not digital_device:
    factors.append("no_digital_device")

# Return top 3 factors
return sorted(factors)[:3]
```

## Model Performance Metrics

### Classification Metrics
```python
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))

# Expected Performance (MVP target):
# - Precision: > 80%
# - Recall: > 75%
# - F1-Score: > 0.77
```

### Target Performance
- Identify >80% of at-risk students (Recall)
- Minimize false positives (Precision)
- Handle imbalanced data effectively

## Model Improvements

### Phase 2 Enhancements
1. **LSTM for Time Series**
   - Capture temporal patterns
   - Predict future dropout risk
   - Input: Last 90 days of data

2. **Ensemble Methods**
   - Combine XGBoost + LightGBM + Random Forest
   - Improved robustness
   - Better risk calibration

3. **Regional Customization**
   - Train separate models per region
   - Account for local cultural factors
   - Adapt to local dropout patterns

4. **Feature Engineering**
   - Parent occupation indicators
   - School infrastructure factors
   - Child marriage prevalence indicator
   - Safety/distance metrics

## Deployment

### Model Serving
```python
# Load model
import pickle
with open('dropout_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Predict
prediction = model.predict(features)
probability = model.predict_proba(features)
```

### Real-time Prediction
```python
@app.post("/api/predictions/predict")
async def predict(request: PredictionRequest, db: Session):
    student = db.query(Student).filter(...).first()
    features = prepare_features(student, db)
    risk_score = model.predict(features)[0]
    return PredictionResponse(risk_score=risk_score)
```

## Re-training Schedule

```
Monthly: Full retraining on accumulated data
Weekly: Validation against holdout set
Daily: Monitor prediction accuracy
```

## Monitoring & Drift Detection

```python
# Monitor prediction distribution
# Alert if sudden shift in risk scores
# Track model accuracy over time
# Log misclassifications for analysis
```

## Data Privacy

- Remove PII before training
- Use anonymized student IDs
- Encrypt sensitive health data
- GDPR-compliant data retention

## Model Explainability

```python
import shap

# SHAP values for feature importance
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# Visualize impact of each feature
shap.dependence_plot("attendance_percentage", shap_values, X)
```

---

*ML Guide Version: 1.0.0*
