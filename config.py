import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Persistent Secret Key for Session Signing
    SECRET_KEY = os.environ.get('SECRET_KEY', 'unifolio-persistent-session-secret-key-2026-phase1')
    
    # 30-Day Permanent Session Configuration (Prevents Logins from Vanishing)
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Set to False for HTTP/localhost, True if HTTPS
    
    DATABASE = os.path.join(BASE_DIR, 'unifolio.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    
    # Demo credentials for easy reference
    DEMO_STUDENT_EMAIL = 'student@unifolio.demo'
    DEMO_STUDENT_PASSWORD = 'student123'
    DEMO_FACULTY_EMAIL = 'faculty@unifolio.demo'
    DEMO_FACULTY_PASSWORD = 'faculty123'

