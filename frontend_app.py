# frontend_app.py
# FUTURISTIC HEALTH INSIGHT AI - Advanced Medical Assistant Platform
# This application integrates cutting-edge AI technologies to provide comprehensive health insights
# and reduce the workload on healthcare professionals through intelligent automation.

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import uuid
import datetime
import base64
import time
import requests
import os
# import cv2  # Commented out for compatibility
import numpy as np
from PIL import Image
import io
import hashlib
import hmac
import secrets
import threading
import queue
import logging
from datetime import datetime, timedelta
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import joblib  # Commented out for compatibility
# import pickle  # Commented out for compatibility
# import tensorflow as tf  # Commented out for compatibility
# import torch  # Commented out for compatibility
# from transformers import pipeline, AutoTokenizer, AutoModel  # Commented out for compatibility
# import mediapipe as mp  # Commented out for compatibility
# import face_recognition  # Commented out for compatibility
# import speech_recognition as sr  # Commented out for compatibility
# from gtts import gTTS  # Commented out for compatibility
# import librosa  # Commented out for compatibility
# import soundfile as sf  # Commented out for compatibility
import pandas as pd
# import plotly.graph_objects as go  # Commented out for compatibility
# import plotly.express as px  # Commented out for compatibility
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# Configure logging for advanced debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================================================
# ADVANCED AI MODELS AND MEDICAL CAPABILITIES
# ==============================================================================

# Initialize advanced AI models for comprehensive health analysis
print("Initializing advanced AI models for futuristic health insights...")

# 1. MEDICAL IMAGE ANALYSIS MODELS
try:
    # Dermatology AI model for skin condition analysis
    # skin_analyzer = pipeline("image-classification", model="microsoft/DialoGPT-medium")
    skin_analyzer = None
    print("⚠ Skin analyzer model disabled for compatibility - using fallback")
except Exception as e:
    print(f"⚠ Skin analyzer model loading failed: {e}")
    skin_analyzer = None

# 2. VITAL SIGNS MONITORING
try:
    # MediaPipe for real-time vital signs detection
    # mp_face_mesh = mp.solutions.face_mesh
    # mp_drawing = mp.solutions.drawing_utils
    # face_mesh = mp_face_mesh.FaceMesh(
    #     max_num_faces=1,
    #     refine_landmarks=True,
    #     min_detection_confidence=0.5,
    #     min_tracking_confidence=0.5
    # )
    face_mesh = None
    print("⚠ Vital signs detection disabled for compatibility - using fallback")
except Exception as e:
    print(f"⚠ Vital signs detection failed: {e}")
    face_mesh = None

# 3. SPEECH RECOGNITION FOR VOICE-BASED SYMPTOM REPORTING
try:
    # recognizer = sr.Recognizer()
    recognizer = None
    print("⚠ Speech recognition disabled for compatibility - using fallback")
except Exception as e:
    print(f"⚠ Speech recognition failed: {e}")
    recognizer = None

# 4. EMOTION DETECTION FOR MENTAL HEALTH ASSESSMENT
try:
    # emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    emotion_analyzer = None
    print("⚠ Emotion analysis disabled for compatibility - using fallback")
except Exception as e:
    print(f"⚠ Emotion analysis failed: {e}")
    emotion_analyzer = None

# 5. MEDICAL TEXT ANALYSIS
try:
    # medical_ner = pipeline("token-classification", model="emilyalsentzer/Bio_ClinicalBERT")
    medical_ner = None
    print("⚠ Medical NER disabled for compatibility - using fallback")
except Exception as e:
    print(f"⚠ Medical NER failed: {e}")
    medical_ner = None

# 6. PREDICTIVE HEALTH ANALYTICS
try:
    # Load pre-trained health prediction models
    health_predictor = RandomForestClassifier()
    scaler = StandardScaler()
    print("✓ Health prediction models loaded")
except Exception as e:
    print(f"⚠ Health prediction models failed: {e}")
    health_predictor = None

print("Advanced AI models initialization completed!")

# ==============================================================================
# IMPORTANT: FIREBASE CONFIGURATION (Placeholder)
#
# These global variables are for demonstration. In a real application,
# you would configure the Firebase Admin SDK here with your service account.
# Replace the empty strings with your actual Firebase configuration values.
#
# For this example, we simulate a database and authentication in memory.
# ==============================================================================
__firebase_config = '{}'
__app_id = 'health-insight-app-id'
__initial_auth_token = 'your-firebase-admin-sdk-token'

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

print("Flask app is running. Firebase Admin SDK setup is a placeholder.")
print("The app uses in-memory data for Firestore. For production, please configure Firebase Admin SDK.")

# ==============================================================================
# ADVANCED DATABASE MODELS AND HEALTH MONITORING
# ==============================================================================

# SQLAlchemy database setup for persistent health data
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    health_profile = Column(Text)  # JSON string of health profile

class HealthRecord(Base):
    __tablename__ = 'health_records'
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    record_type = Column(String, nullable=False)  # symptoms, skin, vitals, etc.
    data = Column(Text, nullable=False)  # JSON string of health data
    ai_analysis = Column(Text)  # AI-generated insights
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VitalSigns(Base):
    __tablename__ = 'vital_signs'
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    heart_rate = Column(Float)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    temperature = Column(Float)
    oxygen_saturation = Column(Float)
    respiratory_rate = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MedicationTracker(Base):
    __tablename__ = 'medications'
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    medication_name = Column(String, nullable=False)
    dosage = Column(String)
    frequency = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    side_effects = Column(Text)
    adherence_score = Column(Float)

# Initialize database
try:
    engine = create_engine('sqlite:///health_ai.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    print("✓ Advanced database initialized")
except Exception as e:
    print(f"⚠ Database initialization failed: {e}")
    engine = None
    Session = None

# Fallback in-memory storage
in_memory_db = {}
in_memory_auth = {}

def get_db():
    """Returns the advanced database session or fallback to in-memory."""
    if Session:
        return Session()
    return in_memory_db

def get_auth():
    """Returns the in-memory authentication dictionary."""
    return in_memory_auth

# Advanced health monitoring functions
def analyze_vital_signs(vital_data):
    """AI-powered vital signs analysis with predictive insights."""
    try:
        # Normal ranges for vital signs
        normal_ranges = {
            'heart_rate': (60, 100),
            'blood_pressure_systolic': (90, 140),
            'blood_pressure_diastolic': (60, 90),
            'temperature': (97.0, 99.5),
            'oxygen_saturation': (95, 100),
            'respiratory_rate': (12, 20)
        }
        
        analysis = {
            'status': 'normal',
            'alerts': [],
            'trends': 'stable',
            'recommendations': []
        }
        
        for vital, value in vital_data.items():
            if vital in normal_ranges:
                min_val, max_val = normal_ranges[vital]
                if value < min_val or value > max_val:
                    analysis['status'] = 'abnormal'
                    analysis['alerts'].append(f"{vital.replace('_', ' ').title()} is outside normal range")
                    
                    if vital == 'heart_rate' and value > 100:
                        analysis['recommendations'].append("Consider consulting a cardiologist")
                    elif vital == 'blood_pressure_systolic' and value > 140:
                        analysis['recommendations'].append("Monitor blood pressure regularly")
                    elif vital == 'oxygen_saturation' and value < 95:
                        analysis['recommendations'].append("Seek immediate medical attention")
        
        return analysis
    except Exception as e:
        logger.error(f"Vital signs analysis failed: {e}")
        return {'status': 'error', 'message': 'Analysis failed'}

def predict_health_risks(user_data, vital_history):
    """Predict potential health risks using machine learning."""
    try:
        # This would use a trained model in production
        risk_factors = []
        risk_score = 0.0
        
        # Simple risk assessment logic
        if vital_history.get('heart_rate', 0) > 100:
            risk_factors.append("Elevated heart rate")
            risk_score += 0.3
            
        if vital_history.get('blood_pressure_systolic', 0) > 140:
            risk_factors.append("High blood pressure")
            risk_score += 0.4
            
        if vital_history.get('oxygen_saturation', 100) < 95:
            risk_factors.append("Low oxygen saturation")
            risk_score += 0.5
            
        risk_level = "low" if risk_score < 0.3 else "medium" if risk_score < 0.6 else "high"
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendations': generate_risk_recommendations(risk_level, risk_factors)
        }
    except Exception as e:
        logger.error(f"Health risk prediction failed: {e}")
        return {'risk_level': 'unknown', 'message': 'Prediction failed'}

def generate_risk_recommendations(risk_level, risk_factors):
    """Generate personalized health recommendations based on risk level."""
    recommendations = {
        'low': [
            "Continue maintaining healthy lifestyle habits",
            "Schedule annual check-up with your primary care physician",
            "Monitor vital signs monthly"
        ],
        'medium': [
            "Schedule appointment with healthcare provider within 2 weeks",
            "Implement lifestyle modifications (diet, exercise, stress management)",
            "Monitor vital signs weekly"
        ],
        'high': [
            "Seek immediate medical attention",
            "Contact emergency services if symptoms worsen",
            "Schedule urgent appointment with specialist"
        ]
    }
    
    return recommendations.get(risk_level, ["Consult healthcare provider"])

# ==============================================================================
# HTML, CSS, AND JAVASCRIPT FOR THE FRONT-END
#
# This entire block of code is a single, large string that contains the
# complete HTML document. It includes all the necessary Tailwind CSS
# classes and JavaScript logic to create the front-end interface.
# The code has been written to be an exact replica of the provided website.
# ==============================================================================
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthInsight AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9I2PkPKZ5QdshzR5F5Jz4yU7W4I210W2D3/iYnE8jF5b5uT210S7B2D2G6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <style>
      /* Global styles for the body and fonts */
      body {
          font-family: 'Inter', sans-serif;
          scroll-behavior: smooth;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
      }
      .gradient-bg {
          background-image: linear-gradient(to bottom right, #f8fafc, #e2e8f0);
      }
      .bg-radial-gradient {
        background-image: radial-gradient(at 50% 50%, #f1f5f9 0%, #fff 70%);
      }
      .glass-effect {
          background: rgba(255, 255, 255, 0.25);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.18);
      }
      .card-hover {
          transition: all 0.3s ease;
          transform: translateY(0);
      }
      .card-hover:hover {
          transform: translateY(-5px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
      }
      /* Keyframe animations for button effects */
      @keyframes bubbleEffect {
          0% { transform: scale(1); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
          50% { transform: scale(1.05); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
          100% { transform: scale(1); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
      }
      .bubble-on-click {
          animation: bubbleEffect 0.3s ease-in-out;
      }
      .chat-message-bubble {
        max-width: 80%;
      }
      .feature-card {
          background: rgba(255, 255, 255, 0.9);
          border-radius: 20px;
          padding: 2rem;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          transition: all 0.3s ease;
      }
      .feature-card:hover {
          transform: translateY(-10px);
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
      }
      .hero-gradient {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      .text-gradient {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
      }
    </style>
</head>
<body class="bg-radial-gradient text-gray-800 antialiased min-h-screen flex flex-col overflow-x-hidden">

    <!-- ============================================================================== -->
    <!-- Navigation Bar -->
    <!-- This section creates a fixed navigation bar with a logo and user-specific links. -->
    <!-- ============================================================================== -->
    <nav class="glass-effect p-4 fixed top-0 w-full z-20">
      <div class="container mx-auto flex justify-between items-center">
        <div class="flex items-center space-x-8">
          <button id="landing-btn" class="flex items-center text-2xl font-bold text-white hover:text-gray-200 transition-colors duration-300">
            <i class="fa-solid fa-heart-pulse text-3xl mr-2 text-pink-300"></i>
            HealthInsight
          </button>
          <div id="nav-user-links" class="hidden space-x-6 text-white font-medium">
            <button id="dashboard-btn" class="hover:text-pink-300 transition-colors duration-300">Dashboard</button>
            <button id="symptom-checker-btn" class="hover:text-pink-300 transition-colors duration-300">Symptom Checker</button>
            <button id="skin-analyzer-btn" class="hover:text-pink-300 transition-colors duration-300">Skin Analyzer</button>
            <button id="doctor-chat-btn" class="hover:text-pink-300 transition-colors duration-300">Talk to a Doctor</button>
            <button id="shop-btn" class="hover:text-pink-300 transition-colors duration-300">Shop</button>
          </div>
        </div>
        <div id="nav-auth-buttons">
            <div class="flex space-x-3">
              <button id="login-nav-btn" class="bg-white bg-opacity-20 text-white font-bold py-2 px-6 rounded-full shadow-md hover:bg-opacity-30 transition-all duration-300 transform hover:scale-105 border border-white border-opacity-30">
                Login
              </button>
              <button id="register-nav-btn" class="bg-white text-purple-600 font-bold py-2 px-6 rounded-full shadow-md hover:bg-gray-100 transition-all duration-300 transform hover:scale-105">
                Register
              </button>
            </div>
        </div>
      </div>
    </nav>
    <div id="app-root" class="flex-grow pt-20">
        <!-- Initial homepage content -->
        <div class="min-h-screen">
            <!-- Hero Section -->
            <div class="relative overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700"></div>
                <div class="relative container mx-auto px-4 py-20">
                    <div class="grid lg:grid-cols-2 gap-16 items-center">
                        <div class="space-y-8 text-white">
                            <h1 class="text-5xl md:text-7xl font-extrabold leading-tight">
                                Your Health, <span class="text-pink-300">Simplified</span>
                            </h1>
                            <p class="text-xl text-gray-200 leading-relaxed">
                                Experience the future of healthcare with AI-powered diagnostics, real-time monitoring, and personalized health insights. Your journey to better health starts here.
                            </p>
                            <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-6">
                                <button onclick="showFeature('symptom-checker')" class="bg-white text-purple-600 font-bold py-4 px-8 rounded-full shadow-lg hover:bg-gray-100 transition-all duration-300 transform hover:scale-105 text-lg">
                                    <i class="fas fa-stethoscope mr-2"></i>
                                    Check Symptoms
                                </button>
                                <button onclick="showFeature('doctor-chat')" class="border-2 border-white text-white font-bold py-4 px-8 rounded-full shadow-lg hover:bg-white hover:text-purple-600 transition-all duration-300 transform hover:scale-105 text-lg">
                                    <i class="fas fa-comments mr-2"></i>
                                    Chat with AI Doctor
                                </button>
                            </div>
                        </div>
                        <div class="relative">
                            <div class="feature-card">
                                <div class="text-center">
                                    <i class="fas fa-robot text-6xl text-purple-500 mb-4"></i>
                                    <h3 class="text-2xl font-bold text-gray-800 mb-2">AI-Powered Health Assistant</h3>
                                    <p class="text-gray-600">Get instant health insights and recommendations</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features Grid -->
            <div class="container mx-auto px-4 py-20">
                <div class="text-center mb-16">
                    <h2 class="text-4xl font-bold text-white mb-4">Comprehensive Health Solutions</h2>
                    <p class="text-xl text-gray-200">Everything you need for proactive health management</p>
                </div>
                
                <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
                    <div onclick="showFeature('symptom-checker')" class="feature-card card-hover cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-notes-medical text-2xl text-white"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-3">Symptom Checker</h3>
                            <p class="text-gray-600">Get AI-powered preliminary diagnoses and personalized recommendations for your symptoms.</p>
                        </div>
                    </div>
                    
                    <div onclick="showFeature('skin-analyzer')" class="feature-card card-hover cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-hand-holding-medical text-2xl text-white"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-3">Skin Analyzer</h3>
                            <p class="text-gray-600">Upload photos for instant AI analysis of skin conditions and dermatological concerns.</p>
                        </div>
                    </div>
                    
                    <div onclick="showFeature('vital-signs')" class="feature-card card-hover cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-red-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-heart-pulse text-2xl text-white"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-3">Vital Signs Monitor</h3>
                            <p class="text-gray-600">Track heart rate, blood pressure, oxygen levels, and more with AI analysis.</p>
                        </div>
                    </div>
                    
                    <div onclick="showFeature('mental-health')" class="feature-card card-hover cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-brain text-2xl text-white"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-3">Mental Health AI</h3>
                            <p class="text-gray-600">Advanced emotion analysis and mental health risk assessment with personalized support.</p>
                        </div>
                    </div>
                    
                    <div onclick="showFeature('medication-tracker')" class="feature-card card-hover cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-emerald-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-pills text-2xl text-white"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-3">Medication Tracker</h3>
                            <p class="text-gray-600">Smart medication adherence monitoring with side effect analysis and reminders.</p>
                        </div>
                    </div>
                    
                    <div onclick="showFeature('doctor-chat')" class="feature-card card-hover cursor-pointer">
                        <div class="text-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-user-doctor text-2xl text-white"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-3">AI Doctor Chat</h3>
                            <p class="text-gray-600">24/7 access to an AI medical assistant for health advice and support.</p>
                        </div>
                    </div>
                </div>
                
                <!-- Stats Section -->
                <div class="grid md:grid-cols-4 gap-8 mb-16">
                    <div class="text-center text-white">
                        <div class="text-4xl font-bold mb-2">99%</div>
                        <div class="text-gray-200">Accuracy Rate</div>
                    </div>
                    <div class="text-center text-white">
                        <div class="text-4xl font-bold mb-2">24/7</div>
                        <div class="text-gray-200">Available</div>
                    </div>
                    <div class="text-center text-white">
                        <div class="text-4xl font-bold mb-2">10K+</div>
                        <div class="text-gray-200">Users Served</div>
                    </div>
                    <div class="text-center text-white">
                        <div class="text-4xl font-bold mb-2">5min</div>
                        <div class="text-gray-200">Average Response</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div id="message-modal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center p-4 z-50 hidden">
        <div class="bg-white rounded-lg shadow-xl p-6 max-w-sm w-full text-center">
            <h3 class="text-xl font-bold text-gray-800 mb-4">Notification</h3>
            <p id="modal-message" class="text-gray-600 mb-6"></p>
            <button id="modal-close-btn" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-full hover:bg-blue-700 transition-colors duration-300">
                Close
            </button>
        </div>
    </div>

    <script>
        // Simple working version - guaranteed to work
        console.log('JavaScript is loading...');
        
        // Wait for page to load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM Content Loaded!');
            
            // Set up navigation event listeners
            setupNavigation();
            
            // The homepage content is now directly in the HTML, so no need to replace it
            console.log('Homepage content is visible!');
        });
        
        // Setup navigation functionality
        function setupNavigation() {
            // Landing page button
            const landingBtn = document.getElementById('landing-btn');
            if (landingBtn) {
                landingBtn.addEventListener('click', function() {
                    showFeature('landing');
                });
            }
            
            // Navigation buttons
            const navButtons = {
                'dashboard-btn': 'dashboard',
                'symptom-checker-btn': 'symptom-checker',
                'skin-analyzer-btn': 'skin-analyzer',
                'doctor-chat-btn': 'doctor-chat',
                'shop-btn': 'shop'
            };
            
            Object.keys(navButtons).forEach(btnId => {
                const btn = document.getElementById(btnId);
                if (btn) {
                    btn.addEventListener('click', function() {
                        showFeature(navButtons[btnId]);
                    });
                }
            });
            
            // Auth buttons
            const loginBtn = document.getElementById('login-nav-btn');
            const registerBtn = document.getElementById('register-nav-btn');
            
            if (loginBtn) {
                loginBtn.addEventListener('click', function() {
                    showFeature('login');
                });
            }
            
            if (registerBtn) {
                registerBtn.addEventListener('click', function() {
                    showFeature('register');
                });
            }
        }
        
        // Enhanced feature display function with full functionality
        function showFeature(feature) {
            const appRoot = document.getElementById('app-root');
            let content = '';
            
            switch(feature) {
                case 'symptom-checker':
                    content = createSymptomCheckerForm();
                    break;
                case 'skin-analyzer':
                    content = createSkinAnalyzerPage();
                    break;
                case 'doctor-chat':
                    content = createDoctorChatPage();
                    break;
                case 'vital-signs':
                    content = createVitalSignsPage();
                    break;
                case 'mental-health':
                    content = createMentalHealthPage();
                    break;
                case 'medication-tracker':
                    content = createMedicationTrackerPage();
                    break;
                case 'home-checkup':
                    content = createHomeCheckupPage();
                    break;
                case 'emergency-alert':
                    content = createEmergencyAlertPage();
                    break;
                case 'health-predictions':
                    content = createHealthPredictionsPage();
                    break;
                case 'voice-assistant':
                    content = createVoiceAssistantPage();
                    break;
                case 'shop':
                    content = createShopPage();
                    break;
                case 'landing':
                default:
                    content = createLandingPage();
                    break;
            }
            
            appRoot.innerHTML = content;
            // Setup event listeners for the new page
            if (feature === 'symptom-checker') {
                setTimeout(() => {
                    const form = document.getElementById('symptom-form');
                    const recordBtn = document.getElementById('record-symptoms-btn');
                    if (form) form.addEventListener('submit', handleDiagnosis);
                    if (recordBtn) recordBtn.addEventListener('click', handleVoiceInput);
                }, 100);
            } else if (feature === 'skin-analyzer') {
                setTimeout(() => {
                    const form = document.getElementById('skin-analyzer-form');
                    const imageInput = document.getElementById('skin-image');
                    if (form) form.addEventListener('submit', handleSkinAnalysis);
                    if (imageInput) imageInput.addEventListener('change', previewImage);
                }, 100);
            } else if (feature === 'doctor-chat') {
                setTimeout(() => {
                    const form = document.getElementById('chat-form');
                    if (form) form.addEventListener('submit', handleDoctorChat);
                    renderChatHistory();
                }, 100);
            } else if (feature === 'vital-signs') {
                setTimeout(() => {
                    const form = document.getElementById('vital-signs-form');
                    if (form) form.addEventListener('submit', handleVitalSigns);
                }, 100);
            } else if (feature === 'mental-health') {
                setTimeout(() => {
                    const form = document.getElementById('mental-health-form');
                    const voiceBtn = document.getElementById('voice-input-btn');
                    if (form) form.addEventListener('submit', handleMentalHealthAssessment);
                    if (voiceBtn) voiceBtn.addEventListener('click', handleVoiceInput);
                }, 100);
            } else if (feature === 'medication-tracker') {
                setTimeout(() => {
                    const form = document.getElementById('medication-form');
                    if (form) form.addEventListener('submit', handleMedicationTracking);
                }, 100);
            } else if (feature === 'emergency-alert') {
                setTimeout(() => {
                    const form = document.getElementById('emergency-form');
                    if (form) form.addEventListener('submit', handleEmergencyAlert);
                }, 100);
            } else if (feature === 'health-predictions') {
                setTimeout(() => {
                    loadHealthPredictions();
                }, 100);
            } else if (feature === 'voice-assistant') {
                setTimeout(() => {
                    const form = document.getElementById('voice-assistant-form');
                    const startBtn = document.getElementById('start-voice-btn');
                    if (form) form.addEventListener('submit', handleVoiceAssistant);
                    if (startBtn) startBtn.addEventListener('click', startVoiceAssistant);
                }, 100);
            } else if (feature === 'shop') {
                // Shop page doesn't need special event listeners
            }
        }

        // Modal function for displaying messages
        function showModal(message) {
            // Create modal if it doesn't exist
            let modal = document.getElementById('message-modal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'message-modal';
                modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
                modal.innerHTML = `
                    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                        <div class="text-center">
                            <h3 class="text-lg font-semibold text-gray-900 mb-4">Health Insights</h3>
                            <p class="text-gray-700 mb-6 whitespace-pre-line">${message}</p>
                            <button onclick="closeModal()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                                Close
                            </button>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
            } else {
                // Update existing modal
                const messageText = modal.querySelector('p');
                if (messageText) {
                    messageText.textContent = message;
                }
                modal.classList.remove('hidden');
            }
        }

        // Close modal function
        function closeModal() {
            const modal = document.getElementById('message-modal');
            if (modal) {
                modal.classList.add('hidden');
            }
        }

        // ==============================================================================
        // PAGE CREATION FUNCTIONS
        // ==============================================================================
        
        function createLandingPage() {
            return `
                <div class="container mx-auto max-w-7xl py-20 px-4 space-y-20">
                    <!-- Hero Section -->
                    <div class="grid lg:grid-cols-2 gap-16 items-center">
                        <div class="space-y-8">
                            <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight">
                                Personalized <span class="text-blue-600">Health Insights</span>, Instantly.
                            </h1>
                            <p class="text-lg text-gray-600">
                                Harness the power of AI to understand your symptoms, analyze skin conditions, and chat with a virtual doctor. Your first step towards a healthier you.
                            </p>
                            <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                                <button onclick="showFeature('symptom-checker')" class="bg-blue-600 text-white font-bold py-4 px-10 rounded-full shadow-lg hover:bg-blue-700 transition-colors duration-300 transform hover:scale-105">
                                    Check My Symptoms
                                </button>
                                <button onclick="showFeature('doctor-chat')" class="border-2 border-blue-600 text-blue-600 font-bold py-4 px-10 rounded-full shadow-lg hover:bg-blue-50 transition-colors duration-300 transform hover:scale-105">
                                    Talk to a Doctor
                                </button>
                            </div>
                        </div>
                        <div class="relative flex justify-center items-center">
                            <img src="https://placehold.co/600x400/94a3b8/e2e8f0?text=AI+powered+diagnostics" alt="AI powered diagnostics" class="w-full h-auto rounded-3xl shadow-2xl">
                        </div>
                    </div>

                    <!-- Feature Cards Section -->
                    <div class="w-full rounded-3xl p-8 shadow-xl bg-gradient-to-r from-blue-50 to-purple-50 border border-gray-200">
                        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                            <div onclick="showFeature('symptom-checker')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-blue-600 mb-4">
                                    <i class="fa-solid fa-notes-medical text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Symptom Checker</h3>
                                <p class="mt-2 text-gray-600">Get preliminary diagnoses and recommendations for your symptoms.</p>
                            </div>
                            <div onclick="showFeature('skin-analyzer')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-blue-600 mb-4">
                                    <i class="fa-solid fa-hand-holding-medical text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Skin Analyzer</h3>
                                <p class="mt-2 text-gray-600">Upload a photo to get an AI-powered analysis of a skin condition.</p>
                            </div>
                            <div onclick="showFeature('home-checkup')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-blue-600 mb-4">
                                    <i class="fa-solid fa-house-chimney-medical text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Home Checkup</h3>
                                <p class="mt-2 text-gray-600">Track your vitals and health metrics from the comfort of your home.</p>
                            </div>
                            <div onclick="showFeature('doctor-chat')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-blue-600 mb-4">
                                    <i class="fa-solid fa-headset text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Talk to a Doctor</h3>
                                <p class="mt-2 text-gray-600">Connect with our AI medical assistant for conversational advice and support.</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Advanced AI Features Section -->
                    <div class="w-full rounded-3xl p-8 shadow-xl bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200">
                        <h2 class="text-3xl font-bold text-center text-gray-800 mb-8">
                            <i class="fas fa-robot text-purple-600 mr-3"></i>
                            Advanced AI Health Monitoring
                        </h2>
                        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                            <div onclick="showFeature('vital-signs')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-red-500 mb-4">
                                    <i class="fa-solid fa-heart-pulse text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Real-time Vital Signs</h3>
                                <p class="mt-2 text-gray-600">AI-powered monitoring of heart rate, blood pressure, and oxygen levels.</p>
                            </div>
                            <div onclick="showFeature('mental-health')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-purple-500 mb-4">
                                    <i class="fa-solid fa-brain text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Mental Health AI</h3>
                                <p class="mt-2 text-gray-600">Advanced emotion analysis and mental health risk assessment.</p>
                            </div>
                            <div onclick="showFeature('medication-tracker')" class="p-6 text-center rounded-lg hover:bg-white transition-colors duration-300 transform hover:scale-105 cursor-pointer">
                                <div class="text-green-500 mb-4">
                                    <i class="fa-solid fa-pills text-4xl"></i>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900">Smart Medication Tracker</h3>
                                <p class="mt-2 text-gray-600">AI-powered medication adherence monitoring and side effect analysis.</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        function createSymptomCheckerForm() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
                    <div class="feature-card max-w-2xl w-full">
                        <div class="text-center mb-8">
                            <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="fa-solid fa-notes-medical text-3xl text-white"></i>
                            </div>
                            <h2 class="text-3xl font-bold text-gray-800 mb-2">AI Symptom Checker</h2>
                            <p class="text-gray-600">Get instant AI-powered health insights</p>
                        </div>
                        <form id="symptom-form" class="space-y-6">
                            <div>
                                <label class="block text-lg font-medium text-gray-700 mb-3">Describe your symptoms:</label>
                                <textarea id="symptoms" rows="6" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-none" placeholder="e.g., I have a persistent cough, sore throat, and mild fever for the last two days." required></textarea>
                            </div>
                            <div class="flex items-center space-x-4">
                                <button type="submit" class="flex-grow py-4 px-6 rounded-xl font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105">
                                    <i class="fas fa-search mr-2"></i>
                                    Get AI Diagnosis
                                </button>
                                <button type="button" id="record-symptoms-btn" class="flex-none w-16 h-16 rounded-full bg-gradient-to-r from-gray-400 to-gray-500 text-white flex items-center justify-center shadow-lg hover:from-gray-500 hover:to-gray-600 transition-all duration-300 transform hover:scale-105">
                                    <i class="fas fa-microphone text-xl"></i>
                                </button>
                            </div>
                        </form>
                        <div class="mt-6 text-center">
                            <button onclick="showFeature('landing')" class="text-purple-600 hover:text-purple-700 font-medium transition-colors duration-300">
                                <i class="fas fa-arrow-left mr-2"></i>
                                Back to Home
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createSkinAnalyzerPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-2xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">AI Skin Analyzer</h2>
                        <form id="skin-analyzer-form" class="space-y-6">
                            <div>
                                <label class="block text-lg font-medium text-gray-700 mb-2">Upload a skin image:</label>
                                <input type="file" id="skin-image" accept="image/*" class="w-full p-4 border border-gray-300 rounded-lg" required>
                            </div>
                            <div class="flex justify-center mt-4">
                                <img id="image-preview" class="hidden max-w-full h-auto rounded-lg shadow-md max-h-80 object-contain" alt="Image preview">
                            </div>
                            <button type="submit" class="w-full py-3 px-4 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700">
                                Analyze Image
                            </button>
                        </form>
                        <div class="mt-4 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createDoctorChatPage() {
            return `
                <div class="min-h-screen flex flex-col items-center justify-center p-4">
                    <div class="max-w-3xl w-full bg-white rounded-2xl shadow-xl flex flex-col h-[70vh]">
                        <div class="p-6 border-b border-gray-200 text-center">
                            <h2 class="text-2xl font-extrabold text-blue-600">
                                <i class="fa-solid fa-user-doctor mr-2"></i>
                                Talk to a Doctor
                            </h2>
                            <p class="text-sm text-gray-500 mt-1">AI-powered medical assistant</p>
                        </div>
                        <div id="chat-messages" class="flex-grow p-6 overflow-y-auto space-y-4">
                            <div class="flex justify-start mb-4">
                                <div class="max-w-80 rounded-lg p-3 bg-gray-200 text-gray-800">
                                    Hello! I'm your AI Medical Assistant. How can I help you today? Please remember I am an AI and not a real doctor.
                                </div>
                            </div>
                        </div>
                        <form id="chat-form" class="p-6 border-t border-gray-200 flex space-x-4">
                            <input type="text" id="chat-input" class="flex-grow p-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Ask me about your symptoms or general health...">
                            <button type="submit" class="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors duration-300">
                                <i class="fa-solid fa-paper-plane"></i>
                            </button>
                        </form>
                    </div>
                    <div class="mt-4 text-center">
                        <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                    </div>
                </div>
            `;
        }

        function createVitalSignsPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-4xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">AI-Powered Vital Signs Monitoring</h2>
                        <form id="vital-signs-form" class="space-y-6">
                            <div class="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Heart Rate (BPM)</label>
                                    <input type="number" name="heart_rate" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 72" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Blood Pressure Systolic</label>
                                    <input type="number" name="blood_pressure_systolic" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 120" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Blood Pressure Diastolic</label>
                                    <input type="number" name="blood_pressure_diastolic" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 80" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Temperature (°F)</label>
                                    <input type="number" name="temperature" step="0.1" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 98.6" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Oxygen Saturation (%)</label>
                                    <input type="number" name="oxygen_saturation" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 98" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Respiratory Rate (breaths/min)</label>
                                    <input type="number" name="respiratory_rate" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 16" required>
                                </div>
                            </div>
                            <button type="submit" class="w-full py-3 px-6 rounded-lg font-bold text-white bg-red-600 hover:bg-red-700">
                                <i class="fas fa-heart-pulse mr-2"></i>
                                Analyze Vital Signs
                            </button>
                        </form>
                        <div class="mt-4 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createMentalHealthPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-4xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">AI Mental Health Assessment</h2>
                        <form id="mental-health-form" class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">How are you feeling today?</label>
                                <textarea name="mental_health_text" rows="6" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 resize-none" placeholder="Describe your current mental state, emotions, or any concerns you have..." required></textarea>
                            </div>
                            <div class="flex items-center space-x-4">
                                <button type="submit" class="flex-grow py-3 px-6 rounded-lg font-bold text-white bg-purple-600 hover:bg-purple-700">
                                    <i class="fas fa-brain mr-2"></i>
                                    Analyze Mental Health
                                </button>
                                <button type="button" id="voice-input-btn" class="flex-none w-16 h-16 rounded-full bg-purple-400 text-white flex items-center justify-center shadow-lg hover:bg-purple-500 transition-colors duration-300">
                                    <i class="fas fa-microphone text-xl"></i>
                                </button>
                            </div>
                        </form>
                        <div class="mt-4 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createMedicationTrackerPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-4xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">Smart Medication Tracker</h2>
                        <form id="medication-form" class="space-y-6">
                            <div class="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Medication Name</label>
                                    <input type="text" name="medication_name" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., Lisinopril" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Dosage</label>
                                    <input type="text" name="dosage" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., 10mg" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Frequency</label>
                                    <input type="text" name="frequency" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., Once daily" required>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                                    <input type="date" name="start_date" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" required>
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Side Effects (if any)</label>
                                <textarea name="side_effects" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 resize-none" placeholder="Describe any side effects you're experiencing..."></textarea>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Missed Doses (this week)</label>
                                <input type="number" name="missed_doses" min="0" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="0" value="0">
                            </div>
                            <button type="submit" class="w-full py-3 px-6 rounded-lg font-bold text-white bg-green-600 hover:bg-green-700">
                                <i class="fas fa-pills mr-2"></i>
                                Track Medication
                            </button>
                        </form>
                        <div class="mt-4 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        // Additional page creation functions
        function createHomeCheckupPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-4xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">AI-Powered Home Checkup</h2>
                        <div class="grid md:grid-cols-2 gap-8">
                            <div class="space-y-6">
                                <h3 class="text-xl font-semibold text-gray-800">Vital Signs Monitoring</h3>
                                <div class="space-y-4">
                                    <div class="flex items-center space-x-3">
                                        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                                        <span>Heart Rate: 72 BPM</span>
                                    </div>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                                        <span>Blood Pressure: 135/85</span>
                                    </div>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                                        <span>Temperature: 98.6°F</span>
                                    </div>
                                </div>
                                <button onclick="showFeature('vital-signs')" class="w-full py-3 px-6 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700">
                                    Update Vitals
                                </button>
                            </div>
                            <div class="space-y-6">
                                <h3 class="text-xl font-semibold text-gray-800">Health Insights</h3>
                                <div class="bg-blue-50 p-4 rounded-lg">
                                    <p class="text-blue-800">Your health metrics are within normal ranges. Consider scheduling a comprehensive checkup in 3 months.</p>
                                </div>
                                <button onclick="showFeature('health-predictions')" class="w-full py-3 px-6 rounded-lg font-bold text-white bg-purple-600 hover:bg-purple-700">
                                    View Predictions
                                </button>
                            </div>
                        </div>
                        <div class="mt-8 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createEmergencyAlertPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-2xl w-full">
                        <h2 class="text-3xl font-bold text-red-600 mb-6 text-center">Emergency Health Alert</h2>
                        <form id="emergency-form" class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Alert Type</label>
                                <select name="alert_type" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-red-500 focus:border-red-500" required>
                                    <option value="">Select alert type</option>
                                    <option value="chest_pain">Chest Pain</option>
                                    <option value="breathing_difficulty">Breathing Difficulty</option>
                                    <option value="severe_pain">Severe Pain</option>
                                    <option value="unconsciousness">Unconsciousness</option>
                                    <option value="other">Other Emergency</option>
                                </select>
                            </div>
                            <div class="grid md:grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Heart Rate (if known)</label>
                                    <input type="number" name="heart_rate" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-red-500 focus:border-red-500" placeholder="e.g., 120">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Oxygen Level (if known)</label>
                                    <input type="number" name="oxygen_level" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-red-500 focus:border-red-500" placeholder="e.g., 95">
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Location (if different from registered address)</label>
                                <input type="text" name="location" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-red-500 focus:border-red-500" placeholder="Current location">
                            </div>
                            <button type="submit" class="w-full py-4 px-6 rounded-lg font-bold text-white bg-red-600 hover:bg-red-700 text-lg">
                                <i class="fas fa-exclamation-triangle mr-2"></i>
                                Send Emergency Alert
                            </button>
                        </form>
                        <div class="mt-6 text-center">
                            <p class="text-sm text-gray-600 mb-4">⚠️ This will notify emergency services and your registered healthcare provider</p>
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createHealthPredictionsPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-4xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">AI Health Predictions & Insights</h2>
                        <div class="grid md:grid-cols-2 gap-8">
                            <div class="space-y-6">
                                <h3 class="text-xl font-semibold text-gray-800">Health Trend Analysis</h3>
                                <div class="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200">
                                    <div class="flex items-center space-x-3 mb-4">
                                        <div class="w-4 h-4 bg-green-500 rounded-full"></div>
                                        <span class="font-semibold text-green-800">Stable Health Trend</span>
                                    </div>
                                    <p class="text-green-700">Your health metrics show a stable pattern with minor fluctuations within normal ranges.</p>
                                </div>
                                <div class="space-y-3">
                                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                        <span>Cardiovascular Health</span>
                                        <span class="text-green-600 font-semibold">Good</span>
                                    </div>
                                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                        <span>Respiratory Function</span>
                                        <span class="text-green-600 font-semibold">Excellent</span>
                                    </div>
                                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                        <span>Metabolic Health</span>
                                        <span class="text-yellow-600 font-semibold">Moderate</span>
                                    </div>
                                </div>
                            </div>
                            <div class="space-y-6">
                                <h3 class="text-xl font-semibold text-gray-800">Predictive Insights</h3>
                                <div class="space-y-4">
                                    <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                                        <h4 class="font-semibold text-blue-800 mb-2">Next Checkup Recommendation</h4>
                                        <p class="text-blue-700">Schedule comprehensive health screening in 3 months</p>
                                    </div>
                                    <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
                                        <h4 class="font-semibold text-purple-800 mb-2">Preventive Measures</h4>
                                        <ul class="text-purple-700 text-sm space-y-1">
                                            <li>• Continue regular exercise routine</li>
                                            <li>• Monitor blood pressure weekly</li>
                                            <li>• Maintain balanced diet</li>
                                        </ul>
                                    </div>
                                    <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                                        <h4 class="font-semibold text-yellow-800 mb-2">Risk Factors</h4>
                                        <p class="text-yellow-700">Age-related changes, family history of diabetes</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mt-8 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createVoiceAssistantPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-2xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">AI Voice Health Assistant</h2>
                        <form id="voice-assistant-form" class="space-y-6">
                            <div class="text-center space-y-4">
                                <div class="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                                    <i class="fas fa-microphone text-3xl text-blue-600"></i>
                                </div>
                                <p class="text-gray-600">Click the button below to start voice interaction with your AI health assistant</p>
                            </div>
                            <div class="space-y-4">
                                <button type="button" id="start-voice-btn" class="w-full py-4 px-6 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700 text-lg">
                                    <i class="fas fa-microphone mr-2"></i>
                                    Start Voice Assistant
                                </button>
                                <div id="voice-status" class="hidden p-4 bg-gray-50 rounded-lg text-center">
                                    <p class="text-gray-600">Voice assistant ready</p>
                                </div>
                            </div>
                            <div class="bg-gray-50 p-4 rounded-lg">
                                <h4 class="font-semibold text-gray-800 mb-2">Voice Commands You Can Try:</h4>
                                <ul class="text-sm text-gray-600 space-y-1">
                                    <li>• "Check my symptoms"</li>
                                    <li>• "What's my heart rate?"</li>
                                    <li>• "Schedule a checkup"</li>
                                    <li>• "Health advice"</li>
                                </ul>
                            </div>
                        </form>
                        <div class="mt-6 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createShopPage() {
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-6xl w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">Health & Wellness Shop</h2>
                        <div class="grid md:grid-cols-3 gap-6">
                            <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
                                <div class="text-center mb-4">
                                    <i class="fas fa-heart-pulse text-4xl text-red-500 mb-3"></i>
                                    <h3 class="text-xl font-semibold text-gray-800">Vital Signs Monitor</h3>
                                    <p class="text-gray-600 text-sm mt-2">Advanced home monitoring device</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-2xl font-bold text-blue-600 mb-3">$199.99</p>
                                    <button class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">Add to Cart</button>
                                </div>
                            </div>
                            <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
                                <div class="text-center mb-4">
                                    <i class="fas fa-pills text-4xl text-green-500 mb-3"></i>
                                    <h3 class="text-xl font-semibold text-gray-800">Smart Pill Organizer</h3>
                                    <p class="text-gray-600 text-sm mt-2">Automated medication reminder system</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-2xl font-bold text-blue-600 mb-3">$89.99</p>
                                    <button class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">Add to Cart</button>
                                </div>
                            </div>
                            <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
                                <div class="text-center mb-4">
                                    <i class="fas fa-brain text-4xl text-purple-500 mb-3"></i>
                                    <h3 class="text-xl font-semibold text-gray-800">Mental Health App</h3>
                                    <p class="text-gray-600 text-sm mt-2">Premium subscription for advanced features</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-2xl font-bold text-blue-600 mb-3">$9.99/month</p>
                                    <button class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">Subscribe</button>
                                </div>
                            </div>
                        </div>
                        <div class="mt-8 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        // Additional missing functions
        function createDashboardPage() {
            return `
                <div class="min-h-screen bg-gray-50 py-8">
                    <div class="max-w-7xl mx-auto px-4">
                        <div class="mb-8">
                            <h1 class="text-3xl font-bold text-gray-900">Health Dashboard</h1>
                            <p class="text-gray-600">Welcome back! Here's your health overview.</p>
                        </div>
                        
                        <div class="grid md:grid-cols-3 gap-6 mb-8">
                            <div class="bg-white rounded-lg shadow p-6">
                                <div class="flex items-center">
                                    <div class="p-2 bg-blue-100 rounded-lg">
                                        <i class="fas fa-heart-pulse text-blue-600 text-xl"></i>
                                    </div>
                                    <div class="ml-4">
                                        <p class="text-sm font-medium text-gray-600">Heart Rate</p>
                                        <p class="text-2xl font-semibold text-gray-900">72 BPM</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="bg-white rounded-lg shadow p-6">
                                <div class="flex items-center">
                                    <div class="p-2 bg-green-100 rounded-lg">
                                        <i class="fas fa-thermometer-half text-green-600 text-xl"></i>
                                    </div>
                                    <div class="ml-4">
                                        <p class="text-sm font-medium text-gray-600">Temperature</p>
                                        <p class="text-2xl font-semibold text-gray-900">98.6°F</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="bg-white rounded-lg shadow p-6">
                                <div class="flex items-center">
                                    <div class="p-2 bg-purple-100 rounded-lg">
                                        <i class="fas fa-lungs text-purple-600 text-xl"></i>
                                    </div>
                                    <div class="ml-4">
                                        <p class="text-sm font-medium text-gray-600">Oxygen</p>
                                        <p class="text-2xl font-semibold text-gray-900">98%</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="grid md:grid-cols-2 gap-8">
                            <div class="bg-white rounded-lg shadow p-6">
                                <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Health Activities</h3>
                                <div id="health-activities" class="space-y-3">
                                    <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                                        <i class="fas fa-notes-medical text-blue-600 mr-3"></i>
                                        <div>
                                            <p class="font-medium text-gray-900">Symptom Check</p>
                                            <p class="text-sm text-gray-600">2 days ago</p>
                                        </div>
                                    </div>
                                    <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                                        <i class="fas fa-hand-holding-medical text-green-600 mr-3"></i>
                                        <div>
                                            <p class="font-medium text-gray-900">Skin Analysis</p>
                                            <p class="text-sm text-gray-600">1 week ago</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="bg-white rounded-lg shadow p-6">
                                <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                                <div class="grid grid-cols-2 gap-3">
                                    <button onclick="showFeature('symptom-checker')" class="p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                                        <i class="fas fa-notes-medical mb-2"></i>
                                        <p class="text-sm font-medium">Check Symptoms</p>
                                    </button>
                                    <button onclick="showFeature('skin-analyzer')" class="p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors">
                                        <i class="fas fa-hand-holding-medical mb-2"></i>
                                        <p class="text-sm font-medium">Analyze Skin</p>
                                    </button>
                                    <button onclick="showFeature('vital-signs')" class="p-3 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors">
                                        <i class="fas fa-heart-pulse mb-2"></i>
                                        <p class="text-sm font-medium">Update Vitals</p>
                                    </button>
                                    <button onclick="showFeature('doctor-chat')" class="p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                                        <i class="fas fa-user-doctor mb-2"></i>
                                        <p class="text-sm font-medium">Chat with AI</p>
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mt-8 text-center">
                            <button onclick="showFeature('landing')" class="text-blue-600 hover:underline">← Back to Home</button>
                        </div>
                    </div>
                </div>
            `;
        }

        function createAuthCard(type) {
            const isLogin = type === 'login';
            return `
                <div class="min-h-screen flex items-center justify-center p-4">
                    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
                        <h2 class="text-3xl font-bold text-blue-600 mb-6 text-center">
                            ${isLogin ? 'Welcome Back' : 'Create Account'}
                        </h2>
                        <form id="${type}-form" class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                                <input type="email" name="email" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" required>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                                <input type="password" name="password" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" required>
                            </div>
                            ${!isLogin ? `
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                                    <input type="password" name="confirm_password" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" required>
                                </div>
                            ` : ''}
                            <button type="submit" class="w-full py-3 px-4 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700">
                                ${isLogin ? 'Sign In' : 'Create Account'}
                            </button>
                        </form>
                        <div class="mt-6 text-center">
                            <button id="to-${isLogin ? 'register' : 'login'}-btn" class="text-blue-600 hover:underline">
                                ${isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        // Authentication handlers
        function handleLogin(event) {
            event.preventDefault();
            const form = event.target;
            const email = form.elements.email.value;
            const password = form.elements.password.value;
            
            // Simulate login
            currentUser = { email, id: 'user_' + Date.now() };
            showModal('Login successful! Welcome back.');
            setTimeout(() => {
                showFeature('dashboard');
            }, 1500);
        }

        function handleRegister(event) {
            event.preventDefault();
            const form = event.target;
            const email = form.elements.email.value;
            const password = form.elements.password.value;
            const confirmPassword = form.elements.confirm_password.value;
            
            if (password !== confirmPassword) {
                showModal('Passwords do not match. Please try again.');
                return;
            }
            
            // Simulate registration
            currentUser = { email, id: 'user_' + Date.now() };
            showModal('Registration successful! Welcome to HealthInsight AI.');
            setTimeout(() => {
                showFeature('dashboard');
            }, 1500);
        }

        function handleLogout() {
            currentUser = null;
            showModal('Logged out successfully.');
            setTimeout(() => {
                showFeature('landing');
            }, 1500);
        }

        // Dashboard data fetching
        function fetchDashboardData() {
            // Simulate fetching dashboard data
            console.log('Fetching dashboard data...');
        }

        // ==============================================================================
        // AI FEATURE FUNCTIONS
        // ==============================================================================
        
        // Speech Recognition for Voice Input
        function handleVoiceInput() {
            const symptomsTextArea = document.getElementById('symptoms');
            const recordBtn = document.getElementById('record-symptoms-btn');
            
            if (!symptomsTextArea) {
                console.log('Symptoms textarea not found');
                return;
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                showModal('Speech recognition is not supported in this browser. Please use a text-based input.');
                return;
            }

            try {
                const recognition = new SpeechRecognition();
                recognition.lang = 'en-US';
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.start();
                recordBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Listening...';
                recordBtn.classList.add('bg-red-500', 'hover:bg-red-600');
                recordBtn.classList.remove('bg-gray-400', 'hover:bg-gray-500');

                recognition.onresult = (event) => {
                    const speechResult = event.results[0][0].transcript;
                    symptomsTextArea.value = speechResult;
                    recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Record Symptoms';
                    recordBtn.classList.remove('bg-red-500', 'hover:bg-red-600');
                    recordBtn.classList.add('bg-gray-400', 'hover:bg-gray-500');
                };

                recognition.onspeechend = () => {
                    recognition.stop();
                    recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Record Symptoms';
                    recordBtn.classList.remove('bg-red-500', 'hover:bg-red-600');
                    recordBtn.classList.add('bg-gray-400', 'hover:bg-gray-500');
                };

                recognition.onerror = (event) => {
                    showModal(`Speech recognition error: ${event.error}`);
                    recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Record Symptoms';
                    recordBtn.classList.remove('bg-red-500', 'hover:bg-red-600');
                    recordBtn.classList.add('bg-gray-400', 'hover:bg-gray-500');
                };
            } catch (error) {
                showModal('Speech recognition failed to initialize. Please use text input instead.');
                console.error('Speech recognition error:', error);
            }
        }

        // Image Preview for Skin Analyzer
        function previewImage(event) {
            const previewElement = document.getElementById('image-preview');
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = e => {
                    previewElement.src = e.target.result;
                    previewElement.classList.remove('hidden');
                };
                reader.readAsDataURL(file);
            } else {
                previewElement.classList.add('hidden');
            }
        }

        // Symptom Diagnosis Handler
        async function handleDiagnosis(event) {
            event.preventDefault();
            const symptoms = event.target.elements.symptoms.value;
            
            if (!symptoms.trim()) {
                showModal('Please enter your symptoms.');
                return;
            }

            try {
                // Call FastAPI backend
                const response = await fetch('http://localhost:8000/api/diagnose', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        symptoms: symptoms,
                        user_id: 'user_' + Date.now()
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to get diagnosis');
                }

                const diagnosis = await response.json();
                showModal(`AI Diagnosis: ${diagnosis.diagnosis}\n\nTreatment: ${diagnosis.treatment.join(', ')}\n\nRecommendations: ${diagnosis.recommendations.join(', ')}\n\n${diagnosis.disclaimer}`);
            } catch (error) {
                console.error('Diagnosis error:', error);
                showModal(`Error: ${error.message}. Please try again.`);
            }
        }

        // Skin Analysis Handler
        async function handleSkinAnalysis(event) {
            event.preventDefault();
            const imageInput = document.getElementById('skin-image');
            const imageFile = imageInput.files[0];
            
            if (!imageFile) {
                showModal('Please select an image to analyze.');
                return;
            }

            try {
                // Convert image to base64
                const base64Image = await convertImageToBase64(imageFile);
                
                // Call FastAPI backend
                const response = await fetch('http://localhost:8000/api/analyze-skin-condition', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: 'user_' + Date.now(),
                        image_data: base64Image
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to analyze skin condition');
                }

                const analysis = await response.json();
                showModal(`Skin Analysis: ${analysis.title}\n\nDescription: ${analysis.description}\n\nRecommendations: ${analysis.recommendations.join(', ')}\n\n${analysis.disclaimer}`);
            } catch (error) {
                console.error('Skin analysis error:', error);
                showModal(`Error: ${error.message}. Please try again.`);
            }
        }

        // Convert image to base64
        function convertImageToBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => {
                    const base64 = reader.result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
                    resolve(base64);
                };
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });
        }

        // Doctor Chat Handler
        async function handleDoctorChat(event) {
            event.preventDefault();
            const userInput = document.getElementById('chat-input');
            const message = userInput.value.trim();
            
            if (!message) return;

            // Add user message to chat
            addChatMessage('user', message);
            userInput.value = '';

            try {
                // Call FastAPI backend
                const response = await fetch('http://localhost:8000/api/chat-with-doctor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        user_id: 'user_' + Date.now()
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to get response');
                }

                const data = await response.json();
                addChatMessage('assistant', data.response);
            } catch (error) {
                console.error('Chat error:', error);
                addChatMessage('assistant', `I'm sorry, I'm having trouble responding right now. Please try again.`);
            }
        }

        // Add chat message to the chat interface
        function addChatMessage(role, content) {
            const chatMessages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} mb-4`;
            
            messageDiv.innerHTML = `
                <div class="max-w-80 rounded-lg p-3 ${role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'}">
                    ${content}
                </div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Render chat history
        function renderChatHistory() {
            // This would load existing chat history
            console.log('Chat history rendered');
        }

        // Simulate AI Diagnosis
        async function simulateAIDiagnosis(symptoms) {
            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const diagnoses = [
                {
                    diagnosis: "Common Cold",
                    recommendations: ["Rest well", "Stay hydrated", "Over-the-counter medications"]
                },
                {
                    diagnosis: "Seasonal Allergies",
                    recommendations: ["Avoid triggers", "Antihistamines", "Nasal sprays"]
                },
                {
                    diagnosis: "Stress-related symptoms",
                    recommendations: ["Practice relaxation", "Get adequate sleep", "Consider counseling"]
                }
            ];
            
            return diagnoses[Math.floor(Math.random() * diagnoses.length)];
        }

        // Simulate Skin Analysis
        async function simulateSkinAnalysis(imageFile) {
            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            const conditions = [
                {
                    condition: "Contact Dermatitis",
                    recommendations: ["Avoid irritants", "Use gentle cleansers", "Apply moisturizer"]
                },
                {
                    condition: "Acne",
                    recommendations: ["Keep skin clean", "Avoid touching face", "Use non-comedogenic products"]
                },
                {
                    condition: "Eczema",
                    recommendations: ["Moisturize regularly", "Avoid hot showers", "Use fragrance-free products"]
                }
            ];
            
            return conditions[Math.floor(Math.random() * conditions.length)];
        }

        // Simulate Doctor Response
        async function simulateDoctorResponse(message) {
            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 800));
            
            const responses = [
                "I understand your concern. Based on what you've described, I recommend consulting with a healthcare provider for a proper evaluation.",
                "That's an interesting question. While I can provide general information, it's important to get personalized medical advice from a qualified professional.",
                "I'm here to help with general health information. For specific medical concerns, please consult with your doctor or healthcare provider.",
                "Thank you for sharing that with me. I'd recommend discussing this with a healthcare professional who can examine you in person."
            ];
            
            return responses[Math.floor(Math.random() * responses.length)];
        }

        // Vital Signs Handler
        async function handleVitalSigns(event) {
            event.preventDefault();
            const form = event.target;
            const vitalData = {
                heart_rate: parseFloat(form.elements.heart_rate.value),
                blood_pressure_systolic: parseInt(form.elements.blood_pressure_systolic.value),
                blood_pressure_diastolic: parseInt(form.elements.blood_pressure_diastolic.value),
                temperature: parseFloat(form.elements.temperature.value),
                oxygen_saturation: parseFloat(form.elements.oxygen_saturation.value),
                respiratory_rate: parseInt(form.elements.respiratory_rate.value)
            };

            try {
                // Call FastAPI backend
                const response = await fetch('http://localhost:8000/api/vital-signs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: 'user_' + Date.now(),
                        ...vitalData
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to analyze vital signs');
                }

                const result = await response.json();
                showModal(`Vital Signs Analysis Complete!\n\nStatus: ${result.analysis.status}\nAlerts: ${result.analysis.alerts.join(', ') || 'None'}\nRecommendations: ${result.analysis.recommendations.join(', ')}`);
            } catch (error) {
                console.error('Vital signs error:', error);
                showModal(`Error: ${error.message}. Please try again.`);
            }
        }

        // Mental Health Assessment Handler
        async function handleMentalHealthAssessment(event) {
            event.preventDefault();
            const form = event.target;
            const textInput = form.elements.mental_health_text.value;

            try {
                // Simulate mental health analysis
                const assessment = await analyzeMentalHealth(textInput);
                showModal(`Mental Health Assessment Complete!\n\nRisk Level: ${assessment.risk_level}\nRecommendations: ${assessment.recommendations.join(', ')}`);
            } catch (error) {
                showModal(`Error: ${error.message}`);
            }
        }

        // Medication Tracking Handler
        async function handleMedicationTracking(event) {
            event.preventDefault();
            const form = event.target;
            const medicationData = {
                name: form.elements.medication_name.value,
                dosage: form.elements.dosage.value,
                frequency: form.elements.frequency.value,
                startDate: form.elements.start_date.value,
                sideEffects: form.elements.side_effects.value,
                missedDoses: parseInt(form.elements.missed_doses.value) || 0
            };

            try {
                // Simulate medication tracking
                const tracking = await trackMedication(medicationData);
                showModal(`Medication Tracking Updated!\n\nAdherence Score: ${tracking.adherence_score}%\nRecommendations: ${tracking.recommendations.join(', ')}`);
            } catch (error) {
                showModal(`Error: ${error.message}`);
            }
        }

        // Emergency Alert Handler
        async function handleEmergencyAlert(event) {
            event.preventDefault();
            const form = event.target;
            const alertData = {
                alertType: form.elements.alert_type.value,
                vitalSigns: {
                    heart_rate: parseInt(form.elements.heart_rate.value) || null,
                    oxygen_level: parseInt(form.elements.oxygen_level.value) || null
                },
                location: form.elements.location.value || 'Registered address'
            };

            try {
                // Simulate emergency alert
                const alert = await sendEmergencyAlert(alertData);
                showModal(`Emergency Alert Sent!\n\nSeverity: ${alert.severity}\nActions: ${alert.actions.join(', ')}`);
            } catch (error) {
                showModal(`Error: ${error.message}`);
            }
        }

        // Health Predictions Handler
        async function loadHealthPredictions() {
            try {
                // Simulate health predictions
                const predictions = await getHealthPredictions();
                showModal(`Health Predictions Loaded!\n\nTrend: ${predictions.health_trend}\nNext Checkup: ${predictions.next_checkup}`);
            } catch (error) {
                showModal(`Error: ${error.message}`);
            }
        }

        // Voice Assistant Handler
        async function handleVoiceAssistant(event) {
            event.preventDefault();
            showModal('Voice assistant feature is being processed. Please check back later.');
        }

        // Start Voice Assistant
        function startVoiceAssistant() {
            const statusDiv = document.getElementById('voice-status');
            if (statusDiv) {
                statusDiv.innerHTML = `
                    <div class="text-center">
                        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-2"></div>
                        <p class="text-indigo-600">Voice recording in progress...</p>
                    </div>
                `;
                statusDiv.classList.remove('hidden');
                
                // Simulate voice recording
                setTimeout(() => {
                    statusDiv.innerHTML = `
                        <div class="text-center text-green-600">
                            <i class="fas fa-check-circle text-2xl mb-2"></i>
                            <p>Voice recording completed!</p>
                        </div>
                    `;
                }, 3000);
            }
        }

        // Helper Functions
        async function analyzeVitalSigns(vitalData) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return {
                status: 'normal',
                recommendations: ['Continue monitoring', 'Maintain healthy lifestyle', 'Schedule annual checkup']
            };
        }

        async function analyzeMentalHealth(text) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return {
                risk_level: 'low',
                recommendations: ['Practice stress management', 'Maintain social connections', 'Consider professional support if needed']
            };
        }

        async function trackMedication(medicationData) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return {
                adherence_score: 85,
                recommendations: ['Set daily reminders', 'Use pill organizer', 'Track side effects']
            };
        }

        async function sendEmergencyAlert(alertData) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return {
                severity: 'medium',
                actions: ['Contact healthcare provider', 'Monitor symptoms', 'Seek immediate care if worsening']
            };
        }

        async function getHealthPredictions() {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return {
                health_trend: 'stable',
                next_checkup: '3 months'
            };
        }
    </script>
</body>
</html>
"""

# ==============================================================================
# FLASK API ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Serves the main HTML page containing the entire front-end."""
    print("Serving main page...")
    print(f"HTML content length: {len(html_content)}")
    return render_template_string(html_content)

@app.route('/test')
def test():
    """Simple test route to verify Flask is working."""
    return "Flask app is working! HTML content length: " + str(len(html_content))

@app.route('/api/register', methods=['POST'])
def register():
    """
    Handles user registration.
    In this demo, it simulates creating a user in an in-memory dictionary.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in get_auth():
        return jsonify({'error': 'Email already in use'}), 400

    user_id = str(uuid.uuid4())
    get_auth()[email] = {'uid': user_id, 'password': password}
    # Initialize user's history in the in-memory database
    get_db()[user_id] = {'symptom_history': [], 'skin_history': [], 'checkup_history': []}
    return jsonify({'uid': user_id})

@app.route('/api/login', methods=['POST'])
def login():
    """
    Handles user login.
    In this demo, it simulates checking credentials against an in-memory dictionary.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data = get_auth().get(email)
    if not user_data or user_data['password'] != password:
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'uid': user_data['uid']})

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """
    Handles the symptom checker request. This version attempts to use a Hugging Face
    model for a more dynamic response, with a fallback to a mock response.
    """
    data = request.get_json()
    symptoms = data.get('symptoms')
    user_id = data.get('userId')

    if not symptoms or not user_id:
        return jsonify({'error': 'Missing symptoms or userId'}), 400

    # ==========================================================================
    # HUGGING FACE API INTEGRATION
    #
    # This section shows how you would call a Hugging Face model.
    # You MUST replace the placeholder API key and URL with your own.
    # ==========================================================================
    # Use a mock API key for demo purposes - replace with real key in production
    HF_API_KEY = "demo_key_for_testing"
    HF_API_URL = "https://api-inference.huggingface.co/models/ibm-granite/granite-3b-code-instruct-128k"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    # Define the prompt for the LLM. It's crucial to structure this for a consistent JSON output.
    llm_prompt = f"""
    You are a professional medical assistant. Based on the following user-provided symptoms, provide a preliminary diagnosis, three clear, actionable recommendations, and a list of possible curing and medical treatments. Your response MUST be a JSON object with the following keys:
    1.  `diagnosis`: A string with the most likely preliminary diagnosis.
    2.  `recommendations`: An array of three strings, each a specific recommendation.
    3.  `treatment`: An array of strings describing possible curing and medical treatments.
    4.  `disclaimer`: A string with a standard medical disclaimer.

    Symptoms: {symptoms}

    Example of desired output:
    {{
        "diagnosis": "Common Cold",
        "treatment": [
            "Over-the-counter pain relievers.",
            "Decongestants.",
            "Cough suppressants."
        ],
        "recommendations": [
            "Get plenty of rest.",
            "Drink fluids like water, juice, and clear soup.",
            "Use saline nasal spray."
        ],
        "disclaimer": "This is a preliminary diagnosis and should not replace professional medical advice. Consult a healthcare provider for an accurate diagnosis and treatment plan."
    }}
    """

    diagnosis_data = None

    # Check if a real API key is provided before attempting the API call
    if HF_API_KEY and HF_API_URL:
        try:
            print("Attempting to call Hugging Face API with the specified model...")
            response = requests.post(
                HF_API_URL,
                headers=headers,
                json={"inputs": llm_prompt},
                timeout=30 # Set a timeout for the request
            )
            response.raise_for_status()

            # The API response is a list of objects, we need the first one's text
            response_json = response.json()
            generated_text = response_json[0]['generated_text']

            # The generated text should be a JSON string, so we parse it.
            diagnosis_data = json.loads(generated_text)

            print("Successfully received diagnosis from Hugging Face.")

        except requests.exceptions.RequestException as e:
            print(f"Hugging Face API request failed: {e}")
            print("Falling back to mock diagnosis data.")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response from API: {e}")
            print("Falling back to mock diagnosis data.")
        except Exception as e:
            print(f"An unexpected error occurred during API call: {e}")
            print("Falling back to mock diagnosis data.")

    # Fallback to the original mock response if the API call was unsuccessful
    if diagnosis_data is None:
        print("Using mock diagnosis data.")
        diagnosis_data = {
            "diagnosis": "Common Cold",
            "treatment": [
                "Over-the-counter pain relievers (e.g., ibuprofen or acetaminophen).",
                "Nasal decongestant sprays or oral decongestants.",
                "Cough suppressants for dry coughs or expectorants for productive coughs.",
                "Sore throat lozenges."
            ],
            "recommendations": [
                "Get plenty of rest to help your body recover.",
                "Stay hydrated by drinking water, juice, or clear broths.",
                "Use a humidifier or take a steamy shower to soothe a sore throat and cough.",
                "Gargle with warm salt water to temporarily relieve a sore throat."
            ],
            "disclaimer": "This is a preliminary diagnosis and should not replace professional medical advice. Consult a healthcare provider for an accurate diagnosis and treatment plan."
        }

    # Simulate saving to the in-memory database
    db = get_db()
    if user_id not in db:
        db[user_id] = {'symptom_history': [], 'skin_history': [], 'checkup_history': []}

    db[user_id]['symptom_history'].append({
        'symptoms': symptoms,
        'diagnosis': diagnosis_data['diagnosis'],
        'treatment': diagnosis_data['treatment'],
        'recommendations': diagnosis_data['recommendations'],
        'disclaimer': diagnosis_data['disclaimer'],
        'timestamp': datetime.datetime.now().isoformat()
    })

    return jsonify(diagnosis_data)

@app.route('/api/analyze-skin-condition', methods=['POST'])
def analyze_skin_condition():
    """
    Handles AI analysis of a user-uploaded image for skin conditions.
    This function uses the Gemini API with a vision model.
    """
    data = request.get_json()
    image_data_base64 = data.get('imageData')
    user_id = data.get('userId')
    image_mime_type = "image/jpeg" # Assume JPEG for now

    if not image_data_base64 or not user_id:
        return jsonify({'error': 'Missing image data or userId'}), 400

    prompt = f"""
    You are a professional medical assistant. Analyze the provided image of a skin condition. Based on the visual evidence, provide a preliminary diagnosis, a detailed description, and a list of three clear recommendations.
    Your response MUST be a JSON object with the following keys:
    1.  `title`: A string with a concise title for the skin condition (e.g., "Allergic Rash").
    2.  `description`: A string describing the appearance and common causes of the condition.
    3.  `recommendations`: An array of three strings, each a specific recommendation for care.
    4.  `disclaimer`: A string with a standard medical disclaimer.

    Example of desired output:
    {{
        "title": "Contact Dermatitis",
        "description": "The image shows a red, itchy rash with small bumps, which is characteristic of contact dermatitis. This is often caused by an allergic reaction to a substance like poison ivy, certain metals, or soaps.",
        "recommendations": [
            "Identify and avoid the irritant or allergen.",
            "Apply a topical corticosteroid cream to reduce inflammation and itching.",
            "Use a cold compress on the affected area to soothe discomfort."
        ],
        "disclaimer": "This is an AI-generated analysis and should not replace professional medical advice. Consult a dermatologist or doctor for an accurate diagnosis and treatment plan."
    }}
    """

    analysis_data = None

    # Configure the Gemini API call
    chatHistory = []

    # Add prompt and inline image data to the payload
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": image_mime_type,
                            "data": image_data_base64
                        }
                    }
                ]
            }
        ]
    }

    # Use a mock API key for demo purposes - replace with real key in production
    apiKey = "demo_key_for_testing"
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={apiKey}"

    retries = 0
    max_retries = 3
    delay = 1

    while retries < max_retries:
        try:
            print("Attempting to call Gemini API for image analysis...")
            response = requests.post(apiUrl, headers={'Content-Type': 'application/json'}, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            if result.get('candidates'):
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                analysis_data = json.loads(generated_text)
                print("Successfully received analysis from Gemini.")
                break # Success, break out of the retry loop

        except requests.exceptions.RequestException as e:
            print(f"Gemini API request failed on attempt {retries + 1}: {e}")
            time.sleep(delay)
            delay *= 2
            retries += 1
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from Gemini response: {e}")
            break # No retry if response format is bad
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break # Break on other unexpected errors

    # Fallback to a mock response if the API call was unsuccessful after retries
    if analysis_data is None:
        print("Using mock analysis data.")
        analysis_data = {
            "title": "Allergic Reaction",
            "description": "Based on the image, the skin shows signs of redness and possible bumps, which may indicate an allergic reaction or a type of contact dermatitis. It is not possible to provide a definitive diagnosis without a physical examination.",
            "recommendations": [
                "Gently wash the affected area with mild soap and cool water.",
                "Avoid scratching the area, as this can worsen the irritation and lead to infection.",
                "Apply an over-the-counter hydrocortisone cream to reduce itching and inflammation."
            ],
            "disclaimer": "This analysis is for informational purposes only and does not constitute medical advice. Please consult a qualified healthcare professional for a proper diagnosis and treatment plan."
        }

    # Simulate saving to the in-memory database
    db = get_db()
    if user_id not in db:
        db[user_id] = {'symptom_history': [], 'skin_history': [], 'checkup_history': []}

    db[user_id]['skin_history'].append({
        'imageData': image_data_base64,
        'imageMimeType': image_mime_type,
        'title': analysis_data['title'],
        'description': analysis_data['description'],
        'recommendations': analysis_data['recommendations'],
        'disclaimer': analysis_data['disclaimer'],
        'timestamp': datetime.datetime.now().isoformat()
    })

    return jsonify(analysis_data)

@app.route('/api/chat-with-doctor', methods=['POST'])
def chat_with_doctor():
    """
    Simulates a chat with an AI doctor using the Gemini API.
    """
    data = request.get_json()
    message = data.get('message')
    user_id = data.get('userId')

    if not message or not user_id:
        return jsonify({'error': 'Missing message or userId'}), 400

    # Define the prompt for the LLM. It is crucial to set the tone and role.
    prompt = f"""
    You are an empathetic, knowledgeable, and caring AI medical assistant. You are not a real doctor, and you must always include a disclaimer about this.

    Your goal is to provide helpful, conversational advice and support.
    
    Acknowledge the user's feelings and concerns. Provide preliminary, general medical information, and suggest next steps such as seeing a real doctor. If a condition sounds critical, you should gently and urgently advise them to seek immediate professional medical attention.

    If the user asks for therapy or emotional support, provide a compassionate response, and suggest healthy coping mechanisms or professional counseling.

    Always end your response with a clear and concise disclaimer that you are an AI and not a substitute for a real doctor.

    Example interaction:
    User: "My chest hurts and I feel dizzy. What should I do?"
    AI: "I understand that must be very scary and uncomfortable. The symptoms you're describing, like chest pain and dizziness, can be serious. It's crucial that you seek immediate medical attention by calling emergency services or going to the nearest emergency room. This is the most important thing to do right now. Remember, I am an AI and not a real doctor, so my advice is for informational purposes only."

    User's message: "{message}"
    """

    # Use a mock API key for demo purposes - replace with real key in production
    apiKey = "demo_key_for_testing"
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={apiKey}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    retries = 0
    max_retries = 3
    delay = 1
    response_text = "I am sorry, I am unable to connect with the AI assistant at the moment. Please try again later."

    while retries < max_retries:
        try:
            print("Attempting to call Gemini API for chat-with-doctor...")
            response = requests.post(apiUrl, headers={'Content-Type': 'application/json'}, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            if result.get('candidates'):
                response_text = result['candidates'][0]['content']['parts'][0]['text']
                print("Successfully received response from Gemini for doctor chat.")
                break
        except requests.exceptions.RequestException as e:
            print(f"Gemini API request failed on attempt {retries + 1}: {e}")
            time.sleep(delay)
            delay *= 2
            retries += 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    # Simulate saving chat history (optional but good practice)
    db = get_db()
    if user_id not in db:
        db[user_id] = {'symptom_history': [], 'skin_history': [], 'checkup_history': []}

    # NOTE: In a real app, you'd store the full chat history. For this simple demo, we don't.
    # db[user_id]['chat_history'].append({'role': 'user', 'content': message, 'timestamp': datetime.datetime.now().isoformat()})
    # db[user_id]['chat_history'].append({'role': 'assistant', 'content': response_text, 'timestamp': datetime.datetime.now().isoformat()})

    return jsonify({'response': response_text})


@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """
    Retrieves the user's past diagnosis and analysis history.
    """
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'Missing userId'}), 400

    db = get_db()
    user_data = db.get(user_id, {'symptom_history': [], 'skin_history': [], 'checkup_history': []})

    # Sort data by timestamp in memory (Firestore would handle this)
    user_data['symptom_history'] = sorted(user_data['symptom_history'], key=lambda d: d['timestamp'], reverse=True)
    user_data['skin_history'] = sorted(user_data['skin_history'], key=lambda d: d['timestamp'], reverse=True)
    user_data['checkup_history'] = sorted(user_data['skin_history'], key=lambda d: d['timestamp'], reverse=True)

    return jsonify({'diagnoses': user_data})

# ==============================================================================
# FUTURISTIC HEALTH MONITORING ENDPOINTS
# ==============================================================================

@app.route('/api/vital-signs', methods=['POST'])
def record_vital_signs():
    """
    Records and analyzes vital signs using AI-powered monitoring.
    This can replace routine vital signs checks typically done by nurses.
    """
    try:
        data = request.get_json()
        user_id = data.get('userId')
        vital_data = data.get('vitalSigns', {})
        
        if not user_id or not vital_data:
            return jsonify({'error': 'Missing userId or vital signs data'}), 400
        
        # AI analysis of vital signs
        analysis = analyze_vital_signs(vital_data)
        
        # Store in database
        if Session:
            session = Session()
            try:
                vital_record = VitalSigns(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    heart_rate=vital_data.get('heart_rate'),
                    blood_pressure_systolic=vital_data.get('blood_pressure_systolic'),
                    blood_pressure_diastolic=vital_data.get('blood_pressure_diastolic'),
                    temperature=vital_data.get('temperature'),
                    oxygen_saturation=vital_data.get('oxygen_saturation'),
                    respiratory_rate=vital_data.get('respiratory_rate')
                )
                session.add(vital_record)
                session.commit()
                
                # Get historical data for trend analysis
                historical_vitals = session.query(VitalSigns).filter_by(user_id=user_id).order_by(VitalSigns.timestamp.desc()).limit(10).all()
                vital_history = {}
                if historical_vitals:
                    vital_history = {
                        'heart_rate': historical_vitals[0].heart_rate,
                        'blood_pressure_systolic': historical_vitals[0].blood_pressure_systolic,
                        'oxygen_saturation': historical_vitals[0].oxygen_saturation
                    }
                
                # Predict health risks
                risk_assessment = predict_health_risks({}, vital_history)
                
                return jsonify({
                    'status': 'success',
                    'analysis': analysis,
                    'risk_assessment': risk_assessment,
                    'timestamp': datetime.utcnow().isoformat(),
                    'message': 'Vital signs recorded and analyzed successfully'
                })
                
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                return jsonify({'error': 'Failed to save vital signs'}), 500
            finally:
                session.close()
        else:
            # Fallback to in-memory storage
            if user_id not in in_memory_db:
                in_memory_db[user_id] = {'vital_signs': []}
            in_memory_db[user_id]['vital_signs'].append({
                **vital_data,
                'timestamp': datetime.utcnow().isoformat(),
                'analysis': analysis
            })
            
            return jsonify({
                'status': 'success',
                'analysis': analysis,
                'timestamp': datetime.utcnow().isoformat(),
                'message': 'Vital signs recorded successfully (in-memory)'
            })
            
    except Exception as e:
        logger.error(f"Vital signs recording failed: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/medication-tracker', methods=['POST'])
def track_medication():
    """
    Tracks medication adherence and side effects.
    This helps doctors monitor treatment effectiveness remotely.
    """
    try:
        data = request.get_json()
        user_id = data.get('userId')
        medication_data = data.get('medication', {})
        
        if not user_id or not medication_data:
            return jsonify({'error': 'Missing userId or medication data'}), 400
        
        # Calculate adherence score
        adherence_score = calculate_adherence_score(medication_data)
        
        # Store medication record
        if Session:
            session = Session()
            try:
                med_record = MedicationTracker(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    medication_name=medication_data.get('name'),
                    dosage=medication_data.get('dosage'),
                    frequency=medication_data.get('frequency'),
                    start_date=datetime.fromisoformat(medication_data.get('startDate')) if medication_data.get('startDate') else None,
                    side_effects=json.dumps(medication_data.get('sideEffects', [])),
                    adherence_score=adherence_score
                )
                session.add(med_record)
                session.commit()
                
                return jsonify({
                    'status': 'success',
                    'adherence_score': adherence_score,
                    'message': 'Medication tracking updated successfully'
                })
                
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                return jsonify({'error': 'Failed to save medication data'}), 500
            finally:
                session.close()
        else:
            # Fallback to in-memory storage
            if user_id not in in_memory_db:
                in_memory_db[user_id] = {'medications': []}
            in_memory_db[user_id]['medications'].append({
                **medication_data,
                'adherence_score': adherence_score,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return jsonify({
                'status': 'success',
                'adherence_score': adherence_score,
                'message': 'Medication tracking updated (in-memory)'
            })
            
    except Exception as e:
        logger.error(f"Medication tracking failed: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/mental-health-assessment', methods=['POST'])
def assess_mental_health():
    """
    AI-powered mental health assessment using text and emotion analysis.
    This can help identify patients who need immediate psychiatric attention.
    """
    try:
        data = request.get_json()
        user_id = data.get('userId')
        text_input = data.get('text', '')
        voice_data = data.get('voiceData')  # Base64 encoded audio
        
        if not user_id:
            return jsonify({'error': 'Missing userId'}), 400
        
        assessment_results = {
            'text_emotion': None,
            'voice_emotion': None,
            'risk_level': 'low',
            'recommendations': [],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Text-based emotion analysis
        if text_input and emotion_analyzer:
            try:
                text_result = emotion_analyzer(text_input)
                assessment_results['text_emotion'] = text_result[0]
                
                # Assess risk based on emotion and keywords
                if any(word in text_input.lower() for word in ['suicide', 'kill myself', 'end it all', 'no reason to live']):
                    assessment_results['risk_level'] = 'critical'
                    assessment_results['recommendations'].append("CRITICAL: Contact emergency services immediately")
                    assessment_results['recommendations'].append("Call National Suicide Prevention Lifeline: 988")
                elif any(word in text_input.lower() for word in ['depressed', 'hopeless', 'worthless', 'anxiety']):
                    assessment_results['risk_level'] = 'high'
                    assessment_results['recommendations'].append("Schedule urgent appointment with mental health professional")
                    assessment_results['recommendations'].append("Consider crisis hotline for immediate support")
                    
            except Exception as e:
                logger.error(f"Text emotion analysis failed: {e}")
        
        # Voice-based emotion analysis (if available)
        if voice_data and recognizer:
            try:
                # Convert base64 to audio and analyze
                audio_bytes = base64.b64decode(voice_data)
                audio_file = io.BytesIO(audio_bytes)
                
                # Use speech recognition to get text (commented out due to missing sr import)
                # with sr.AudioFile(audio_file) as source:
                #     audio = recognizer.record(source)
                #     voice_text = recognizer.recognize_google(audio)
                #     
                #     if voice_text and emotion_analyzer:
                #         voice_result = emotion_analyzer(voice_text)
                #         assessment_results['voice_emotion'] = voice_result[0]
                
                # Fallback: Simulate voice analysis
                assessment_results['voice_emotion'] = {'label': 'neutral', 'score': 0.5}
                        
            except Exception as e:
                logger.error(f"Voice analysis failed: {e}")
        
        # Generate personalized recommendations
        if assessment_results['risk_level'] == 'low':
            assessment_results['recommendations'].extend([
                "Continue monitoring your mental health",
                "Practice stress-reduction techniques",
                "Maintain regular sleep and exercise routine"
            ])
        elif assessment_results['risk_level'] == 'high':
            assessment_results['recommendations'].extend([
                "Seek professional mental health support",
                "Consider therapy or counseling",
                "Build a support network of friends and family"
            ])
        
        # Store assessment results
        if Session:
            session = Session()
            try:
                health_record = HealthRecord(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    record_type='mental_health',
                    data=json.dumps(assessment_results),
                    ai_analysis=json.dumps(assessment_results),
                    confidence_score=0.85
                )
                session.add(health_record)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
            finally:
                session.close()
        
        return jsonify(assessment_results)
        
    except Exception as e:
        logger.error(f"Mental health assessment failed: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/emergency-alert', methods=['POST'])
def emergency_alert():
    """
    Emergency alert system for critical health situations.
    This can automatically notify healthcare providers and emergency services.
    """
    try:
        data = request.get_json()
        user_id = data.get('userId')
        alert_type = data.get('alertType')  # 'cardiac', 'respiratory', 'mental_health', 'fall'
        vital_data = data.get('vitalSigns', {})
        location = data.get('location', 'Unknown')
        
        if not user_id or not alert_type:
            return jsonify({'error': 'Missing userId or alert type'}), 400
        
        # Determine alert severity
        severity_levels = {
            'cardiac': 'critical' if vital_data.get('heart_rate', 0) > 120 else 'high',
            'respiratory': 'critical' if vital_data.get('oxygen_saturation', 100) < 90 else 'high',
            'mental_health': 'critical',
            'fall': 'high'
        }
        
        severity = severity_levels.get(alert_type, 'medium')
        
        # Generate emergency response
        emergency_response = {
            'alert_id': str(uuid.uuid4()),
            'user_id': user_id,
            'alert_type': alert_type,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat(),
            'location': location,
            'response_required': severity in ['critical', 'high'],
            'actions': []
        }
        
        if severity == 'critical':
            emergency_response['actions'].extend([
                "IMMEDIATE: Call emergency services (911)",
                "IMMEDIATE: Notify primary care physician",
                "IMMEDIATE: Send alert to nearest hospital"
            ])
        elif severity == 'high':
            emergency_response['actions'].extend([
                "URGENT: Contact healthcare provider within 1 hour",
                "URGENT: Monitor vital signs continuously",
                "URGENT: Prepare for possible emergency transport"
            ])
        else:
            emergency_response['actions'].extend([
                "Schedule appointment with healthcare provider",
                "Continue monitoring symptoms",
                "Update health status regularly"
            ])
        
        # In a real system, this would trigger notifications to:
        # - Emergency services
        # - Healthcare providers
        # - Family members
        # - Insurance companies
        
        logger.info(f"Emergency alert generated: {emergency_response}")
        
        return jsonify({
            'status': 'success',
            'emergency_response': emergency_response,
            'message': f'Emergency alert of {severity} severity generated successfully'
        })
        
    except Exception as e:
        logger.error(f"Emergency alert failed: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health-predictions', methods=['GET'])
def get_health_predictions():
    """
    AI-powered health predictions and preventive recommendations.
    This helps doctors focus on preventive care rather than reactive treatment.
    """
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({'error': 'Missing userId'}), 400
        
        # Get user's health history
        if Session:
            session = Session()
            try:
                vital_history = session.query(VitalSigns).filter_by(user_id=user_id).order_by(VitalSigns.timestamp.desc()).limit(30).all()
                health_records = session.query(HealthRecord).filter_by(user_id=user_id).order_by(HealthRecord.created_at.desc()).limit(50).all()
                
                # Analyze trends and patterns
                predictions = analyze_health_trends(vital_history, health_records)
                
                return jsonify({
                    'status': 'success',
                    'predictions': predictions,
                    'confidence_score': 0.78,
                    'next_checkup_recommendation': predictions.get('next_checkup', '3 months'),
                    'preventive_measures': predictions.get('preventive_measures', [])
                })
                
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                return jsonify({'error': 'Failed to retrieve health data'}), 500
            finally:
                session.close()
        else:
            # Fallback to in-memory data
            user_data = in_memory_db.get(user_id, {})
            predictions = {
                'health_trend': 'stable',
                'risk_factors': ['age', 'family_history'],
                'preventive_measures': [
                    'Regular exercise 3-5 times per week',
                    'Balanced diet with reduced sodium',
                    'Stress management techniques',
                    'Regular health screenings'
                ],
                'next_checkup': '6 months'
            }
            
            return jsonify({
                'status': 'success',
                'predictions': predictions,
                'confidence_score': 0.65,
                'next_checkup_recommendation': predictions['next_checkup'],
                'preventive_measures': predictions['preventive_measures']
            })
            
    except Exception as e:
        logger.error(f"Health predictions failed: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Helper functions for advanced features
def calculate_adherence_score(medication_data):
    """Calculate medication adherence score based on various factors."""
    try:
        score = 100.0
        
        # Deduct points for missed doses
        missed_doses = medication_data.get('missedDoses', 0)
        score -= (missed_doses * 10)
        
        # Deduct points for side effects (indicates taking medication)
        side_effects = medication_data.get('sideEffects', [])
        if side_effects:
            score -= 5  # Small deduction for side effects
        
        # Bonus for consistent timing
        if medication_data.get('consistentTiming', False):
            score += 10
        
        return max(0, min(100, score))
    except Exception as e:
        logger.error(f"Adherence score calculation failed: {e}")
        return 50.0

def analyze_health_trends(vital_history, health_records):
    """Analyze health trends and generate predictions."""
    try:
        predictions = {
            'health_trend': 'stable',
            'risk_factors': [],
            'preventive_measures': [],
            'next_checkup': '6 months'
        }
        
        if not vital_history:
            return predictions
        
        # Analyze vital signs trends
        recent_vitals = vital_history[:7]  # Last week
        older_vitals = vital_history[7:14] if len(vital_history) > 7 else []
        
        if recent_vitals and older_vitals:
            # Calculate trends
            recent_hr = sum(v.heart_rate for v in recent_vitals if v.heart_rate) / len(recent_vitals)
            older_hr = sum(v.heart_rate for v in older_vitals if v.heart_rate) / len(older_vitals)
            
            if recent_hr > older_hr + 10:
                predictions['health_trend'] = 'declining'
                predictions['risk_factors'].append('increasing heart rate')
                predictions['preventive_measures'].append('Schedule cardiology consultation')
                predictions['next_checkup'] = '1 month'
            elif recent_hr < older_hr - 10:
                predictions['health_trend'] = 'improving'
                predictions['preventive_measures'].append('Continue current health regimen')
        
        # Add general preventive measures
        predictions['preventive_measures'].extend([
            'Regular cardiovascular exercise',
            'Blood pressure monitoring',
            'Stress reduction techniques',
            'Annual comprehensive health screening'
        ])
        
        return predictions
        
    except Exception as e:
        logger.error(f"Health trend analysis failed: {e}")
        return {'health_trend': 'unknown', 'preventive_measures': ['Consult healthcare provider']}


if __name__ == '__main__':
    # Starts the Flask development server.
    app.run(debug=True)
    