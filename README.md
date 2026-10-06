# UniFolio — Academic Project Portfolio System

> **Phase 1 Implementation**: Submission Portal &bull; PDF Upload &bull; Scikit-Learn TF-IDF & Curated Keyword Tagging &bull; Faculty Review &bull; Search &bull; Outcome Analytics

---

## 1. Project Overview

**UniFolio** is a unified academic project portfolio system designed for university engineering departments. It centralizes student capstone project submissions, applies deterministic natural language processing (**TF-IDF + Curated Keyword Rules**) to extract core competencies, maps them to **Course Outcomes (CO)** and **Program Outcomes (PO)** for accreditation (NBA / NAAC), provides a streamlined **Faculty Review & Sign-off Workflow**, and renders dynamic **Accreditation Analytics**.

### Taglines
* **Main Tagline:** *One Platform for Every Academic Project.*
* **Secondary Tagline:** *Submit. Analyze. Review. Discover.*

---

## 2. Phase 1 Technology Stack

* **Backend:** Python 3.10+ / Flask 3.x
* **Database:** SQLite 3 (Foreign keys enabled, normalized relational schema)
* **NLP Engine:** `scikit-learn` (`TfidfVectorizer`), NumPy, Curated Dictionary matching
* **Frontend:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons
* **Visualizations:** Chart.js 4.x (Real-time dynamic SQLite data feeds)

> **Important — Phase 1 Scope Boundary:**  
> This prototype deliberately excludes BERT, LLMs, GPT APIs, neural vector databases, embeddings, blockchain, or deep learning NLP. In accordance with the Phase 1 specification, NLP is strictly powered by **TF-IDF + Curated Keyword Rules**.

---

## 3. Core Features

1. **Role-Based Authentication & Session Security:**
   - Dedicated Student and Faculty portals.
   - Password hashing with Werkzeug security.
   - 1-Click Demo Login helpers on the sign-in page.
2. **Project Submission & Actual PDF Storage:**
   - Submitter details, co-authors, domain selection, and abstract.
   - Secure PDF upload with MIME validation, unique UUID prefixing, and in-browser preview/download.
3. **Automated TF-IDF NLP Extraction:**
   - Fits `TfidfVectorizer` (unigrams + bigrams) over an academic reference corpus.
   - Extracts top important terms with numerical TF-IDF importance scores.
4. **Curated Keyword & CO-PO Rule Mapping:**
   - Maps extracted terms against modular `SKILL_KEYWORDS` dictionaries.
   - Suggests associated Course Outcomes (`CO1`–`CO5`) and Program Outcomes (`PO1`–`PO5`).
   - Clear institutional disclaimer: *“Automated Suggestion &rarr; Faculty Validation Required”*.
5. **Faculty Review & Accreditation Sign-Off:**
   - Review pending queue, view uploaded PDFs, inspect TF-IDF scores, record faculty remarks, and approve or reject submissions.
6. **Search & Multi-Facet Discovery:**
   - Real-time text search across title, abstract, domain, tags, and student authors.
   - Faceted filters for Domain, Skill, CO, PO, and Review Status.
7. **Dynamic Analytics Dashboard:**
   - Projects by Domain (Bar chart).
   - Technical Skill Distribution (Horizontal bar chart).
   - Course Outcome (CO) Attainment Coverage (Bar chart).
   - Program Outcome (PO) Attainment Coverage (Bar chart).
   - Key KPI cards for total submissions, approvals, top skill, and dominant domain.

---

## 4. Demo Credentials

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Student** | `student@unifolio.demo` | `student123` | Submit projects, upload PDF, view TF-IDF analysis, track review status |
| **Faculty** | `faculty@unifolio.demo` | `faculty123` | View submissions queue, inspect PDFs & TF-IDF scores, validate tags, approve/reject |

*(The login page features 1-Click Quick-Fill buttons for effortless evaluation during project reviews.)*

---

## 5. Quickstart & Running Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize and Seed the Database
```bash
python seed.py
```
*This initializes the SQLite tables, creates demo user accounts, generates a sample valid PDF, and pre-populates 11 realistic academic projects across AI, Web Dev, IoT, Cybersecurity, Data Science, and Databases.*

### 3. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 6. How the NLP Engine Works (TF-IDF + Curated Rules)

```
Project Abstract
       ↓
Text Normalization & Tokenization
       ↓
Scikit-Learn TfidfVectorizer (N-grams: 1-2)
       ↓
Term Importance Scoring (TF-IDF Weights)
       ↓
Curated Keyword Dictionary Match
       ↓
Detected Skills (Python, Computer Vision, etc.)
       ↓
Rule-Based Outcome Matrix Mapping
       ↓
Suggested Course Outcomes (CO) & Program Outcomes (PO)
       ↓
Faculty Review Sign-Off & Validation
```

### Curated Skill Dictionary Sample (`services/tagging_service.py`)
```python
SKILL_KEYWORDS = {
    "Python": ["python", "pandas", "numpy", "flask", "django"],
    "Machine Learning": ["machine learning", "classification", "regression", "prediction"],
    "Computer Vision": ["opencv", "image processing", "computer vision", "face recognition"],
    "Web Development": ["html", "css", "javascript", "web development", "bootstrap"],
    "Database": ["sql", "mysql", "sqlite", "database", "crud"],
    "IoT": ["iot", "arduino", "sensor", "embedded", "esp32"]
}
```

### CO & PO Rule Mapping Sample
```python
CO_MAPPING = {
    "Python": ["CO1", "CO5"],
    "Machine Learning": ["CO2", "CO3", "CO5"],
    "Computer Vision": ["CO2", "CO4"],
    "Database": ["CO3", "CO4"]
}

PO_MAPPING = {
    "Python": ["PO1", "PO5"],
    "Machine Learning": ["PO1", "PO2", "PO5"],
    "Computer Vision": ["PO2", "PO3", "PO5"]
}
```

---

## 7. Project Structure

```
unifolio/
│
├── app.py                      # Flask Application Factory & Entry Point
├── config.py                   # App Configuration & Limits
├── database.py                 # SQLite Helper & Foreign Key Enforcer
├── schema.sql                  # SQLite Relational Schema DDL
├── seed.py                     # Database Seeder (Demo Users + 11 Projects + Sample PDF)
├── requirements.txt            # Python Dependencies
├── README.md                   # System Documentation
│
├── services/
│   ├── __init__.py
│   ├── nlp_service.py          # Scikit-Learn TF-IDF Extraction & Term Scoring
│   ├── tagging_service.py      # Curated Dictionaries & CO/PO Rule Engine
│   └── pdf_service.py          # PDF File Validation, Storage & Retrieval
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py          # Authentication, Role Decorators & Profiles
│   ├── student_routes.py       # Student Submission & Analysis Visualization
│   ├── faculty_routes.py       # Faculty Review Queue & Approval Workflow
│   ├── search_routes.py        # Multi-Attribute Repository Search Engine
│   └── analytics_routes.py     # Analytics & Chart.js JSON API Endpoints
│
├── templates/
│   ├── base.html               # Master Layout with Modern Navbar & Footer
│   ├── landing.html            # Landing Page with Hero Preview & Roadmap
│   ├── login.html              # Sign-In with 1-Click Demo Fill
│   ├── register.html           # Student Registration
│   ├── profile.html            # User Profile & Activity Metrics
│   ├── student/
│   │   ├── dashboard.html      # Student Metrics & Recent Projects
│   │   ├── submit.html         # Submission Form with Drag-and-Drop PDF Upload
│   │   ├── analysis_result.html# Multi-Step Pipeline Tracker & TF-IDF Score Table
│   │   ├── my_projects.html    # Student's Projects & Faculty Feedback
│   │   └── project_details.html# Comprehensive Project View with PDF Download
│   ├── faculty/
│   │   ├── dashboard.html      # Pending Queue & Evaluation Stats
│   │   ├── submissions.html    # Filterable Repository Table (Status & Domain)
│   │   └── review.html         # Evaluation Form: TF-IDF Terms, Outcomes, Remarks
│   ├── search/
│   │   └── index.html          # Faceted Discovery Portal
│   └── analytics/
│       └── index.html          # Dynamic Chart.js Analytics (Domain, Skills, CO, PO)
│
├── static/
│   ├── css/
│   │   └── style.css           # Academic SaaS Custom Styling
│   └── js/
│       ├── main.js             # Drag-and-drop Upload & Demo Login Helpers
│       └── charts.js           # Chart.js Integration & SQLite API Fetcher
│
└── uploads/                    # Secure Storage for Uploaded PDF Files
```

---

## 8. Multi-Phase Roadmap

* **Phase 1 (Current Active Deliverable):** Submission portal, PDF upload validation, Scikit-Learn TF-IDF vectorization, curated keyword skill tagging, rule-based CO/PO suggestions, faculty review/approval sign-off, search portal, Chart.js outcome analytics.
* **Phase 2 (Future Scope):** Fine-tuned BERT multi-label classifier, dense embedding cosine similarity, automated idea duplicate detection.
* **Phase 3 (Future Scope):** Cryptographic faculty sign-off hashes, automated NBA/NAAC Self-Assessment Report (SAR) generation, multi-year cohort attainment tracking.
* **Phase 4 (Future Scope):** Multi-department tenant isolation, LMS (Canvas/Moodle) LTI integration, SAML/OAuth Single Sign-On.
