# Test all imports from frontend_app.py
print("Testing all imports from frontend_app.py...")

# Basic imports
try:
    import json
    print("✓ json OK")
except Exception as e:
    print(f"✗ json failed: {e}")

try:
    import uuid
    print("✓ uuid OK")
except Exception as e:
    print(f"✗ uuid failed: {e}")

try:
    import datetime
    print("✓ datetime OK")
except Exception as e:
    print(f"✗ datetime failed: {e}")

try:
    import base64
    print("✓ base64 OK")
except Exception as e:
    print(f"✗ base64 failed: {e}")

try:
    import time
    print("✓ time OK")
except Exception as e:
    print(f"✗ time failed: {e}")

try:
    import requests
    print("✓ requests OK")
except Exception as e:
    print(f"✗ requests failed: {e}")

try:
    import os
    print("✓ os OK")
except Exception as e:
    print(f"✗ os failed: {e}")

try:
    import cv2
    print("✓ cv2 OK")
except Exception as e:
    print(f"✗ cv2 failed: {e}")

try:
    import numpy as np
    print("✓ numpy OK")
except Exception as e:
    print(f"✗ numpy failed: {e}")

try:
    from PIL import Image
    print("✓ PIL.Image OK")
except Exception as e:
    print(f"✗ PIL.Image failed: {e}")

try:
    import io
    print("✓ io OK")
except Exception as e:
    print(f"✗ io failed: {e}")

try:
    import hashlib
    print("✓ hashlib OK")
except Exception as e:
    print(f"✗ hashlib failed: {e}")

try:
    import hmac
    print("✓ hmac OK")
except Exception as e:
    print(f"✗ hmac failed: {e}")

try:
    import secrets
    print("✓ secrets OK")
except Exception as e:
    print(f"✗ secrets failed: {e}")

try:
    import threading
    print("✓ threading OK")
except Exception as e:
    print(f"✗ threading failed: {e}")

try:
    import queue
    print("✓ queue OK")
except Exception as e:
    print(f"✗ queue failed: {e}")

try:
    import logging
    print("✓ logging OK")
except Exception as e:
    print(f"✗ logging failed: {e}")

try:
    from datetime import datetime, timedelta
    print("✓ datetime.datetime, timedelta OK")
except Exception as e:
    print(f"✗ datetime.datetime, timedelta failed: {e}")

try:
    import sqlite3
    print("✓ sqlite3 OK")
except Exception as e:
    print(f"✗ sqlite3 failed: {e}")

try:
    import sqlalchemy
    print("✓ sqlalchemy OK")
except Exception as e:
    print(f"✗ sqlalchemy failed: {e}")

try:
    from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Integer
    print("✓ sqlalchemy components OK")
except Exception as e:
    print(f"✗ sqlalchemy components failed: {e}")

try:
    from sqlalchemy.ext.declarative import declarative_base
    print("✓ sqlalchemy.declarative_base OK")
except Exception as e:
    print(f"✗ sqlalchemy.declarative_base failed: {e}")

try:
    from sqlalchemy.orm import sessionmaker
    print("✓ sqlalchemy.sessionmaker OK")
except Exception as e:
    print(f"✗ sqlalchemy.sessionmaker failed: {e}")

try:
    import joblib
    print("✓ joblib OK")
except Exception as e:
    print(f"✗ joblib failed: {e}")

try:
    import pickle
    print("✓ pickle OK")
except Exception as e:
    print(f"✗ pickle failed: {e}")

try:
    import tensorflow as tf
    print("✓ tensorflow OK")
except Exception as e:
    print(f"✗ tensorflow failed: {e}")

try:
    import torch
    print("✓ torch OK")
except Exception as e:
    print(f"✗ torch failed: {e}")

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    print("✓ transformers OK")
except Exception as e:
    print(f"✗ transformers failed: {e}")

try:
    import mediapipe as mp
    print("✓ mediapipe OK")
except Exception as e:
    print(f"✗ mediapipe failed: {e}")

try:
    import face_recognition
    print("✓ face_recognition OK")
except Exception as e:
    print(f"✗ face_recognition failed: {e}")

try:
    import speech_recognition as sr
    print("✓ speech_recognition OK")
except Exception as e:
    print(f"✗ speech_recognition failed: {e}")

try:
    from gtts import gTTS
    print("✓ gtts OK")
except Exception as e:
    print(f"✗ gtts failed: {e}")

try:
    import librosa
    print("✓ librosa OK")
except Exception as e:
    print(f"✗ librosa failed: {e}")

try:
    import soundfile as sf
    print("✓ soundfile OK")
except Exception as e:
    print(f"✗ soundfile failed: {e}")

try:
    import pandas as pd
    print("✓ pandas OK")
except Exception as e:
    print(f"✗ pandas failed: {e}")

try:
    import plotly.graph_objects as go
    print("✓ plotly.graph_objects OK")
except Exception as e:
    print(f"✗ plotly.graph_objects failed: {e}")

try:
    import plotly.express as px
    print("✓ plotly.express OK")
except Exception as e:
    print(f"✗ plotly.express failed: {e}")

try:
    from sklearn.preprocessing import StandardScaler
    print("✓ sklearn.preprocessing OK")
except Exception as e:
    print(f"✗ sklearn.preprocessing failed: {e}")

try:
    from sklearn.ensemble import RandomForestClassifier
    print("✓ sklearn.ensemble OK")
except Exception as e:
    print(f"✗ sklearn.ensemble failed: {e}")

try:
    import warnings
    print("✓ warnings OK")
except Exception as e:
    print(f"✗ warnings failed: {e}")

print("\nImport test completed.")
