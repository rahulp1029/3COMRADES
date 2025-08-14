#!/usr/bin/env python3
"""
HealthInsight AI - FastAPI Backend
Advanced medical assistant platform with AI-powered health insights
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import json
import uuid
import datetime
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app setup
app = FastAPI(
    title="HealthInsight AI API",
    description="AI-powered health monitoring platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://127.0.0.1:5000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SymptomRequest(BaseModel):
    symptoms: str
    user_id: str

class SkinAnalysisRequest(BaseModel):
    user_id: str
    image_data: str

class ChatRequest(BaseModel):
    message: str
    user_id: str

class VitalSignsRequest(BaseModel):
    user_id: str
    heart_rate: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    respiratory_rate: Optional[float] = None

class PrescriptionAnalysisRequest(BaseModel):
    user_id: str
    image_data: str

# In-memory storage
in_memory_db = {}
in_memory_auth = {}

# Utility functions
def simulate_ai_diagnosis(symptoms: str) -> dict:
    """Simulate AI diagnosis"""
    time.sleep(1)
    diagnoses = [
        {
            "diagnosis": "Common Cold",
            "treatment": ["Rest", "Hydration", "Over-the-counter medications"],
            "recommendations": ["Get plenty of rest", "Stay hydrated", "Monitor symptoms"],
            "disclaimer": "This is preliminary. Consult a healthcare provider."
        },
        {
            "diagnosis": "Seasonal Allergies",
            "treatment": ["Antihistamines", "Nasal sprays", "Avoid triggers"],
            "recommendations": ["Avoid allergens", "Use air purifiers", "Monitor pollen counts"],
            "disclaimer": "This is preliminary. Consult a healthcare provider."
        }
    ]
    return diagnoses[hash(symptoms) % len(diagnoses)]

def simulate_skin_analysis(image_data: str) -> dict:
    """Simulate skin analysis"""
    time.sleep(1.5)
    conditions = [
        {
            "title": "Contact Dermatitis",
            "description": "Red, itchy rash caused by allergic reaction",
            "recommendations": ["Avoid irritants", "Use gentle cleansers", "Apply moisturizer"],
            "disclaimer": "Consult a dermatologist for proper diagnosis."
        },
        {
            "title": "Acne",
            "description": "Common skin condition with pimples and blackheads",
            "recommendations": ["Keep skin clean", "Avoid touching face", "Use non-comedogenic products"],
            "disclaimer": "Consult a dermatologist for proper diagnosis."
        }
    ]
    return conditions[hash(image_data) % len(conditions)]

def simulate_doctor_response(message: str) -> dict:
    """Simulate doctor response"""
    time.sleep(1)
    responses = [
        {
            "response": "Based on your symptoms, I recommend monitoring your condition and consulting a healthcare provider if symptoms persist or worsen.",
            "confidence": 0.85,
            "disclaimer": "This is general advice. Consult a healthcare provider for personalized care."
        },
        {
            "response": "Your symptoms suggest a common condition that typically resolves with rest and proper care. However, if you experience severe symptoms, seek immediate medical attention.",
            "confidence": 0.78,
            "disclaimer": "This is general advice. Consult a healthcare provider for personalized care."
        }
    ]
    return responses[hash(message) % len(responses)]

def simulate_prescription_analysis(image_data: str) -> dict:
    """Simulate prescription analysis using AI/OCR"""
    time.sleep(2)  # Simulate AI processing time
    
    # Simulate extracted prescription data
    analysis = {
        "patient": {
            "name": "John Doe",
            "doctor": "Dr. Sarah Johnson",
            "date": "2024-01-15",
            "pharmacy": "City Pharmacy"
        },
        "medications": [
            {
                "name": "Lisinopril",
                "dosage": "10mg",
                "frequency": "Once daily",
                "duration": "30 days",
                "classification": "ACE Inhibitor",
                "indication": "High blood pressure",
                "side_effects": ["Dizziness", "Dry cough", "Fatigue"],
                "contraindications": ["Pregnancy", "Severe kidney disease"],
                "interactions": ["NSAIDs", "Lithium", "Potassium supplements"],
                "instructions": "Take as prescribed, preferably in the morning"
            },
            {
                "name": "Metformin",
                "dosage": "500mg",
                "frequency": "Twice daily with meals",
                "duration": "90 days",
                "classification": "Biguanide",
                "indication": "Type 2 diabetes",
                "side_effects": ["Nausea", "Diarrhea", "Stomach upset"],
                "contraindications": ["Severe kidney disease", "Metabolic acidosis"],
                "interactions": ["Alcohol", "Contrast dye", "Furosemide"],
                "instructions": "Take with food to minimize stomach upset"
            }
        ],
        "general_instructions": "Take medications as prescribed. Monitor blood pressure and blood sugar regularly. Report any unusual side effects to your doctor immediately.",
        "safety_warnings": [
            "Do not stop taking medications without consulting your doctor",
            "Keep medications out of reach of children",
            "Store in a cool, dry place",
            "Check expiration dates regularly"
        ],
        "disclaimer": "This AI analysis is for informational purposes only. Always consult your healthcare provider or pharmacist for personalized medical advice, especially regarding dosage, side effects, and drug interactions."
    }
    
    return analysis

def analyze_vital_signs(vital_data: dict) -> dict:
    """Analyze vital signs"""
    analysis = {'status': 'normal', 'alerts': [], 'recommendations': []}
    
    if vital_data.get('heart_rate', 0) > 100:
        analysis['status'] = 'abnormal'
        analysis['alerts'].append("Elevated heart rate")
        analysis['recommendations'].append("Consider consulting a cardiologist")
    
    if vital_data.get('blood_pressure_systolic', 0) > 140:
        analysis['status'] = 'abnormal'
        analysis['alerts'].append("High blood pressure")
        analysis['recommendations'].append("Monitor blood pressure regularly")
    
    return analysis

# API Endpoints
@app.get("/")
async def root():
    return {"message": "HealthInsight AI FastAPI Backend", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.utcnow().isoformat()}

@app.post("/api/diagnose")
async def diagnose_symptoms(request: SymptomRequest):
    try:
        if not request.symptoms.strip():
            raise HTTPException(status_code=400, detail="Symptoms required")
        
        diagnosis = simulate_ai_diagnosis(request.symptoms)
        
        # Store in database
        if request.user_id not in in_memory_db:
            in_memory_db[request.user_id] = {'symptom_history': []}
        
        in_memory_db[request.user_id]['symptom_history'].append({
            'symptoms': request.symptoms,
            'diagnosis': diagnosis,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        
        return diagnosis
    except Exception as e:
        logger.error(f"Diagnosis failed: {e}")
        raise HTTPException(status_code=500, detail="Diagnosis failed")

@app.post("/api/analyze-skin-condition")
async def analyze_skin_condition(request: SkinAnalysisRequest):
    try:
        if not request.image_data:
            raise HTTPException(status_code=400, detail="Image data required")
        
        analysis = simulate_skin_analysis(request.image_data)
        
        # Store in database
        if request.user_id not in in_memory_db:
            in_memory_db[request.user_id] = {'skin_history': []}
        
        in_memory_db[request.user_id]['skin_history'] = in_memory_db[request.user_id].get('skin_history', [])
        in_memory_db[request.user_id]['skin_history'].append({
            'analysis': analysis,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        
        return analysis
    except Exception as e:
        logger.error(f"Skin analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Skin analysis failed")

@app.post("/api/chat-with-doctor")
async def chat_with_doctor(request: ChatRequest):
    """AI doctor chat endpoint"""
    try:
        response = simulate_doctor_response(request.message)
        
        # Store in memory
        if request.user_id not in in_memory_db:
            in_memory_db[request.user_id] = {"chat_history": []}
        
        in_memory_db[request.user_id]["chat_history"].append({
            "message": request.message,
            "response": response["response"],
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        return {
            "status": "success",
            "response": response["response"],
            "confidence": response["confidence"],
            "disclaimer": response["disclaimer"]
        }
    except Exception as e:
        logger.error(f"Doctor chat failed: {e}")
        raise HTTPException(status_code=500, detail="Chat failed")

@app.post("/api/analyze-prescription")
async def analyze_prescription(request: PrescriptionAnalysisRequest):
    """AI prescription analysis endpoint"""
    try:
        analysis = simulate_prescription_analysis(request.image_data)
        
        # Store in memory
        if request.user_id not in in_memory_db:
            in_memory_db[request.user_id] = {"prescription_history": []}
        
        in_memory_db[request.user_id]["prescription_history"].append({
            "analysis": analysis,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        return {
            "status": "success",
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Prescription analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@app.post("/api/vital-signs")
async def record_vital_signs(request: VitalSignsRequest):
    try:
        vital_data = {
            'heart_rate': request.heart_rate,
            'blood_pressure_systolic': request.blood_pressure_systolic,
            'blood_pressure_diastolic': request.blood_pressure_diastolic,
            'temperature': request.temperature,
            'oxygen_saturation': request.oxygen_saturation,
            'respiratory_rate': request.respiratory_rate
        }
        
        vital_data = {k: v for k, v in vital_data.items() if v is not None}
        
        if not vital_data:
            raise HTTPException(status_code=400, detail="At least one vital sign required")
        
        analysis = analyze_vital_signs(vital_data)
        
        # Store in database
        if request.user_id not in in_memory_db:
            in_memory_db[request.user_id] = {'vital_signs': []}
        
        in_memory_db[request.user_id]['vital_signs'] = in_memory_db[request.user_id].get('vital_signs', [])
        in_memory_db[request.user_id]['vital_signs'].append({
            **vital_data,
            'analysis': analysis,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
        
        return {
            'status': 'success',
            'analysis': analysis,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Vital signs failed: {e}")
        raise HTTPException(status_code=500, detail="Vital signs recording failed")

@app.get("/api/dashboard/{user_id}")
async def get_dashboard(user_id: str):
    try:
        user_data = in_memory_db.get(user_id, {
            'symptom_history': [],
            'skin_history': [],
            'vital_signs': []
        })
        
        # Ensure all required keys exist
        if 'symptom_history' not in user_data:
            user_data['symptom_history'] = []
        if 'skin_history' not in user_data:
            user_data['skin_history'] = []
        if 'vital_signs' not in user_data:
            user_data['vital_signs'] = []
        
        return {
            'status': 'success',
            'data': user_data,
            'summary': {
                'total_symptoms': len(user_data['symptom_history']),
                'total_skin_analyses': len(user_data['skin_history']),
                'total_vital_records': len(user_data['vital_signs'])
            }
        }
    except Exception as e:
        logger.error(f"Dashboard failed: {e}")
        raise HTTPException(status_code=500, detail="Dashboard retrieval failed")

if __name__ == "__main__":
    print("🚀 Starting HealthInsight AI FastAPI Backend...")
    print("📚 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)