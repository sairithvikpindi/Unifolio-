import sqlite3
import os
from flask import g, current_app
from config import Config

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        db_path = current_app.config['DATABASE'] if current_app else Config.DATABASE
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def get_db_direct(db_path=None):
    """Direct database connection for non-request scripts (seed, CLI)."""
    if db_path is None:
        db_path = Config.DATABASE
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(db_path=None):
    """Initializes the database schema from schema.sql and seeds default demo accounts if empty."""
    if db_path is None:
        db_path = current_app.config['DATABASE'] if current_app else Config.DATABASE
    
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, mode='r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn = get_db_direct(db_path)
    conn.executescript(schema_sql)
    
    # Ensure demo accounts exist on fresh initializations
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count == 0:
        from werkzeug.security import generate_password_hash
        student_pw = generate_password_hash("student123")
        faculty_pw = generate_password_hash("faculty123")
        conn.execute(
            "INSERT INTO users (name, email, password_hash, role, department) VALUES (?, ?, ?, ?, ?)",
            ("Alex Chen (Demo Student)", "student@unifolio.demo", student_pw, "student", "Computer Science & Engineering")
        )
        conn.execute(
            "INSERT INTO users (name, email, password_hash, role, department) VALUES (?, ?, ?, ?, ?)",
            ("Dr. Sarah Jenkins (Demo Faculty)", "faculty@unifolio.demo", faculty_pw, "faculty", "Computer Science & Engineering")
        )
    
    conn.commit()
    conn.close()

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
