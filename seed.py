"""
UniFolio Database Seeder (Phase 1)
Seeds demo users, sample valid PDF documents, and 10+ realistic B.Tech academic projects
with real TF-IDF term scoring and CO/PO outcome mappings.
"""

import os
import sqlite3
from werkzeug.security import generate_password_hash
from config import Config
from database import init_db, get_db_direct
from services.nlp_service import analyze_project_text

def create_sample_pdf(file_path, title_text):
    """Generates a minimal, valid binary PDF file for demonstration."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>endobj\n"
        b"4 0 obj<</Length 55>>stream\n"
        b"BT /F1 18 Tf 50 700 Td (UniFolio Academic Project Report) Tj ET\n"
        b"endstream\n"
        b"endobj\n"
        b"xref\n"
        b"0 5\n"
        b"0000000000 65535 f\n"
        b"0000000009 00000 n\n"
        b"0000000058 00000 n\n"
        b"0000000115 00000 n\n"
        b"0000000216 00000 n\n"
        b"trailer<</Size 5/Root 1 0 R>>\n"
        b"startxref\n"
        b"322\n"
        b"%%EOF\n"
    )
    with open(file_path, 'wb') as f:
        f.write(pdf_content)

def seed_database():
    print("[UniFolio] Initializing database schema...")
    init_db(Config.DATABASE)
    db = get_db_direct(Config.DATABASE)
    
    # Clean existing data
    db.execute("DELETE FROM reviews")
    db.execute("DELETE FROM project_tags")
    db.execute("DELETE FROM project_members")
    db.execute("DELETE FROM projects")
    db.execute("DELETE FROM users")
    db.commit()
    
    print("[UniFolio] Creating Demo Users...")
    # Demo Student
    student_pw = generate_password_hash("student123")
    cur = db.execute(
        "INSERT INTO users (name, email, password_hash, role, department) VALUES (?, ?, ?, ?, ?)",
        ("Alex Chen (Demo Student)", "student@unifolio.demo", student_pw, "student", "Computer Science & Engineering")
    )
    demo_student_id = cur.lastrowid
    
    # Demo Faculty
    faculty_pw = generate_password_hash("faculty123")
    cur = db.execute(
        "INSERT INTO users (name, email, password_hash, role, department) VALUES (?, ?, ?, ?, ?)",
        ("Dr. Sarah Williams (Demo Faculty)", "faculty@unifolio.demo", faculty_pw, "faculty", "Computer Science & Engineering")
    )
    demo_faculty_id = cur.lastrowid
    
    # Additional Students
    students_info = [
        ("Rahul Sharma", "rahul.sharma@unifolio.demo", student_pw, "Information Technology"),
        ("Priya Patel", "priya.patel@unifolio.demo", student_pw, "Computer Science & Engineering"),
        ("David Miller", "david.miller@unifolio.demo", student_pw, "Artificial Intelligence & Data Science"),
        ("Sneha Rao", "sneha.rao@unifolio.demo", student_pw, "Electronics & Communication")
    ]
    student_ids = [demo_student_id]
    for s_name, s_email, s_pw, s_dept in students_info:
        c = db.execute(
            "INSERT INTO users (name, email, password_hash, role, department) VALUES (?, ?, ?, ?, ?)",
            (s_name, s_email, s_pw, "student", s_dept)
        )
        student_ids.append(c.lastrowid)
        
    db.commit()
    db.close()
    print("[UniFolio] Clean initialization complete: Demo accounts created, 0 projects (Ready for real submissions).")

def seed_sample_projects():
    db = get_db_direct(Config.DATABASE)
    demo_student_id = db.execute("SELECT id FROM users WHERE email = 'student@unifolio.demo'").fetchone()[0]
    demo_faculty_id = db.execute("SELECT id FROM users WHERE email = 'faculty@unifolio.demo'").fetchone()[0]
    student_ids = [row[0] for row in db.execute("SELECT id FROM users WHERE role = 'student'").fetchall()]
    
    sample_pdf_name = "demo_sample_project_report.pdf"
    sample_pdf_path = os.path.join(Config.UPLOAD_FOLDER, sample_pdf_name)
    create_sample_pdf(sample_pdf_path, "Demo Project Report")
    
    sample_projects = [
        {
            "title": "AI-Based Smart Attendance System",
            "abstract": "This project uses Python, machine learning, computer vision and face recognition to automatically identify students and maintain attendance records using a database. The system captures live video from classroom cameras, performs facial feature extraction using OpenCV, and updates SQLite logs with timestamped student logs.",
            "domain": "Artificial Intelligence",
            "student_id": demo_student_id,
            "members": ["Alex Chen", "Priya Patel"],
            "status": "Approved",
            "review": {
                "faculty_id": demo_faculty_id,
                "decision": "Approved",
                "comment": "Good project. CO/PO mapping reviewed. Solid implementation of computer vision with robust database logging."
            }
        },
        {
            "title": "Decentralized Healthcare Record Management System",
            "abstract": "A secure web development platform developed with Python Flask and SQLite database for hospital patient record management. Includes role-based authentication for doctors and patients, data encryption, audit trails, and automated medical history report generation.",
            "domain": "Database",
            "student_id": student_ids[1] if len(student_ids) > 1 else demo_student_id,
            "members": ["Rahul Sharma", "Alex Chen"],
            "status": "Approved",
            "review": {
                "faculty_id": demo_faculty_id,
                "decision": "Approved",
                "comment": "Comprehensive database schema and strict role-based access controls. Well-aligned with CO3 and PO3."
            }
        }
    ]
    
    print(f"[UniFolio] Seeding {len(sample_projects)} sample projects...")
    for proj in sample_projects:
        cur = db.execute(
            """
            INSERT INTO projects (title, abstract, domain, pdf_filename, pdf_path, student_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (proj['title'], proj['abstract'], proj['domain'], sample_pdf_name, sample_pdf_path, proj['student_id'], proj['status'])
        )
        proj_id = cur.lastrowid
        for m in proj['members']:
            db.execute("INSERT INTO project_members (project_id, student_name) VALUES (?, ?)", (proj_id, m))
        analysis = analyze_project_text(proj['title'], proj['abstract'])
        for sk in analysis['detected_skills']:
            db.execute("INSERT INTO project_tags (project_id, tag, tag_type, score) VALUES (?, ?, 'skill', ?)", (proj_id, sk['skill'], sk['score']))
        for co in analysis['suggested_cos']:
            db.execute("INSERT INTO project_tags (project_id, tag, tag_type, score) VALUES (?, ?, 'CO', ?)", (proj_id, co['code'], co['score']))
        for po in analysis['suggested_pos']:
            db.execute("INSERT INTO project_tags (project_id, tag, tag_type, score) VALUES (?, ?, 'PO', ?)", (proj_id, po['code'], po['score']))
        if proj['review']:
            r = proj['review']
            db.execute("INSERT INTO reviews (project_id, faculty_id, decision, comment) VALUES (?, ?, ?, ?)", (proj_id, r['faculty_id'], r['decision'], r['comment']))
    db.commit()
    db.close()
    print("[UniFolio] Sample projects seeded successfully.")

if __name__ == '__main__':
    import sys
    seed_database()
    if '--with-samples' in sys.argv:
        seed_sample_projects()
