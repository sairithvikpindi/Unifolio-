-- UniFolio SQLite Database Schema (Phase 1)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'faculty')),
    department TEXT DEFAULT 'Computer Science & Engineering',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    domain TEXT NOT NULL,
    pdf_filename TEXT,
    pdf_path TEXT,
    student_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    tag_type TEXT NOT NULL CHECK(tag_type IN ('skill', 'CO', 'PO')),
    score REAL DEFAULT 0.0,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    faculty_id INTEGER NOT NULL,
    decision TEXT NOT NULL CHECK(decision IN ('Approved', 'Rejected')),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_projects_student ON projects(student_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_domain ON projects(domain);
CREATE INDEX IF NOT EXISTS idx_tags_project ON project_tags(project_id);
CREATE INDEX IF NOT EXISTS idx_tags_type ON project_tags(tag_type);
CREATE INDEX IF NOT EXISTS idx_reviews_project ON reviews(project_id);
