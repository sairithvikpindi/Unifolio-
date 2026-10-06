"""
UniFolio End-to-End Verification Test Script
Tests the exact 20-step verification workflow specified in the project requirements.
"""

import io
import os
import unittest
from app import create_app
from database import get_db_direct
from seed import seed_database, create_sample_pdf
from config import Config

class UniFolioEndToEndWorkflowTest(unittest.TestCase):
    test_db = os.path.join(os.path.dirname(__file__), 'test_unifolio.db')

    @classmethod
    def setUpClass(cls):
        print("\n=======================================================")
        print("Starting UniFolio 20-Step End-to-End Verification Suite")
        print("=======================================================\n")
        # Ensure clean isolated test database (does not touch production unifolio.db)
        if os.path.exists(cls.test_db):
            try:
                os.remove(cls.test_db)
            except Exception:
                pass
        
        from database import init_db
        init_db(cls.test_db)
        cls.app = create_app({'TESTING': True, 'DATABASE': cls.test_db})
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db):
            try:
                os.remove(cls.test_db)
            except Exception:
                pass

    def test_20_step_workflow(self):
        # -------------------------------------------------------------
        # TEST 1: Open the website
        # -------------------------------------------------------------
        print("[TEST 1] Opening the website (GET /)...")
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"UniFolio", res.data)
        self.assertIn(b"One Platform for Every Academic Project", res.data)
        print("  --> PASS: Landing page loaded successfully with branding.\n")

        # -------------------------------------------------------------
        # TEST 2: Login using student@unifolio.demo / student123
        # -------------------------------------------------------------
        print("[TEST 2] Logging in as student (student@unifolio.demo)...")
        res = self.client.post('/login', data={
            'email': 'student@unifolio.demo',
            'password': 'student123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Student Portal", res.data)
        print("  --> PASS: Student authentication and session established.\n")

        # -------------------------------------------------------------
        # TEST 3: Submit Project with PDF Upload
        # -------------------------------------------------------------
        print("[TEST 3] Submitting new project with PDF report...")
        title = "AI-Based Smart Attendance System (New Test Submission)"
        abstract = "This project uses Python, machine learning, computer vision and face recognition to automatically identify students and maintain attendance records using a database."
        domain = "Artificial Intelligence"
        
        # Create in-memory valid test PDF
        pdf_bytes = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>endobj\n4 0 obj<</Length 44>>stream\nBT /F1 18 Tf 50 700 Td (Test PDF Content) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000216 00000 n\ntrailer<</Size 5/Root 1 0 R>>\nstartxref\n311\n%%EOF\n"
        data = {
            'title': title,
            'abstract': abstract,
            'domain': domain,
            'team_members': 'Alex Chen, Priya Patel',
            'pdf_file': (io.BytesIO(pdf_bytes), 'smart_attendance_report.pdf')
        }
        res = self.client.post('/student/submit', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Project Submitted Successfully", res.data)
        print("  --> PASS: Project submitted and analysis page rendered.\n")

        # -------------------------------------------------------------
        # TEST 4: Confirm project is stored in SQLite
        # -------------------------------------------------------------
        print("[TEST 4] Confirming project is stored in SQLite database...")
        db = get_db_direct(self.test_db)
        row = db.execute("SELECT * FROM projects WHERE title = ?", (title,)).fetchone()
        self.assertIsNotNone(row)
        project_id = row['id']
        self.assertEqual(row['domain'], 'Artificial Intelligence')
        self.assertEqual(row['status'], 'Pending')
        print(f"  --> PASS: Project #{project_id} stored in SQLite with status 'Pending'.\n")

        # -------------------------------------------------------------
        # TEST 5: Confirm TF-IDF runs
        # -------------------------------------------------------------
        print("[TEST 5] Confirming TF-IDF processing occurred...")
        tags = db.execute("SELECT * FROM project_tags WHERE project_id = ?", (project_id,)).fetchall()
        self.assertTrue(len(tags) > 0)
        print(f"  --> PASS: {len(tags)} tags generated and stored in SQLite.\n")

        # -------------------------------------------------------------
        # TEST 6: Confirm important terms appear
        # -------------------------------------------------------------
        print("[TEST 6] Confirming important terms appear...")
        res = self.client.get(f'/student/analysis/{project_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Important Terms (TF-IDF)", res.data)
        print("  --> PASS: TF-IDF terms table rendered.\n")

        # -------------------------------------------------------------
        # TEST 7: Confirm skill tags appear
        # -------------------------------------------------------------
        print("[TEST 7] Confirming skill tags appear...")
        skill_tags = [t['tag'] for t in tags if t['tag_type'] == 'skill']
        print(f"      Extracted Skills: {skill_tags}")
        self.assertIn("Python", skill_tags)
        self.assertIn("Machine Learning", skill_tags)
        self.assertIn("Computer Vision", skill_tags)
        self.assertIn("Database", skill_tags)
        print("  --> PASS: Skills (Python, Machine Learning, Computer Vision, Database) correctly tagged.\n")

        # -------------------------------------------------------------
        # TEST 8: Confirm CO/PO suggestions appear
        # -------------------------------------------------------------
        print("[TEST 8] Confirming CO/PO suggestions appear...")
        co_tags = [t['tag'] for t in tags if t['tag_type'] == 'CO']
        po_tags = [t['tag'] for t in tags if t['tag_type'] == 'PO']
        print(f"      Suggested COs: {co_tags}")
        print(f"      Suggested POs: {po_tags}")
        self.assertTrue(len(co_tags) >= 3)
        self.assertTrue(len(po_tags) >= 2)
        print("  --> PASS: CO/PO suggestions mapped successfully.\n")

        # -------------------------------------------------------------
        # TEST 9: Logout student
        # -------------------------------------------------------------
        print("[TEST 9] Logging out student session...")
        res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        print("  --> PASS: Student logged out successfully.\n")

        # -------------------------------------------------------------
        # TEST 10: Login as faculty@unifolio.demo / faculty123
        # -------------------------------------------------------------
        print("[TEST 10] Logging in as faculty (faculty@unifolio.demo)...")
        res = self.client.post('/login', data={
            'email': 'faculty@unifolio.demo',
            'password': 'faculty123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Faculty Review Dashboard", res.data)
        print("  --> PASS: Faculty authentication established.\n")

        # -------------------------------------------------------------
        # TEST 11: Open the submitted project review page
        # -------------------------------------------------------------
        print(f"[TEST 11] Opening project #{project_id} review page...")
        res = self.client.get(f'/faculty/review/{project_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Faculty Evaluation", res.data)
        print("  --> PASS: Faculty review interface loaded.\n")

        # -------------------------------------------------------------
        # TEST 12: Review the generated tags in review interface
        # -------------------------------------------------------------
        print("[TEST 12] Inspecting generated tags and TF-IDF terms in faculty review...")
        self.assertIn(b"Automated Suggestion", res.data)
        self.assertIn(b"Faculty Validation", res.data)
        self.assertIn(b"Python", res.data)
        print("  --> PASS: Tag breakdown and disclaimer verified in faculty UI.\n")

        # -------------------------------------------------------------
        # TEST 13 & 14: Add comment and Approve project
        # -------------------------------------------------------------
        print("[TEST 13 & 14] Adding remark and submitting Approval decision...")
        faculty_comment = "Good project. CO/PO mapping reviewed."
        res = self.client.post(f'/faculty/review/{project_id}', data={
            'decision': 'Approved',
            'comment': faculty_comment
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        print("  --> PASS: Review submitted successfully.\n")

        # -------------------------------------------------------------
        # TEST 15: Confirm status changed to Approved
        # -------------------------------------------------------------
        print("[TEST 15] Confirming status updated to 'Approved' in SQLite...")
        updated_row = db.execute("SELECT status FROM projects WHERE id = ?", (project_id,)).fetchone()
        self.assertEqual(updated_row['status'], 'Approved')
        review_record = db.execute("SELECT * FROM reviews WHERE project_id = ?", (project_id,)).fetchone()
        self.assertEqual(review_record['decision'], 'Approved')
        self.assertEqual(review_record['comment'], faculty_comment)
        print("  --> PASS: Project status is now 'Approved' and review record verified.\n")

        # -------------------------------------------------------------
        # TEST 16 & 17: Search for "attendance" and confirm approved project appears
        # -------------------------------------------------------------
        print("[TEST 16 & 17] Searching repository for 'attendance'...")
        res = self.client.get('/search/?q=attendance')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"AI-Based Smart Attendance System", res.data)
        self.assertIn(b"Approved", res.data)
        print("  --> PASS: Approved project discovered in repository search.\n")

        # -------------------------------------------------------------
        # TEST 18 & 19: Open Analytics and verify Chart.js data
        # -------------------------------------------------------------
        print("[TEST 18 & 19] Testing Analytics page and dynamic Chart.js JSON API...")
        res = self.client.get('/analytics/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Academic Outcome", res.data)
        self.assertIn(b"Skill Analytics", res.data)
        
        api_res = self.client.get('/analytics/api/data')
        self.assertEqual(api_res.status_code, 200)
        chart_data = api_res.get_json()
        self.assertIn('domains', chart_data)
        self.assertIn('skills', chart_data)
        self.assertIn('cos', chart_data)
        self.assertIn('pos', chart_data)
        self.assertTrue(len(chart_data['domains']['labels']) > 0)
        self.assertTrue(len(chart_data['skills']['labels']) > 0)
        print("  --> PASS: Real dynamic chart data returned from SQLite.\n")

        # -------------------------------------------------------------
        # TEST 20: Verify data persistence across fresh connection
        # -------------------------------------------------------------
        print("[TEST 20] Verifying database persistence across separate connections...")
        db_new = get_db_direct(self.test_db)
        persisted = db_new.execute("SELECT title, status FROM projects WHERE id = ?", (project_id,)).fetchone()
        self.assertEqual(persisted['status'], 'Approved')
        db_new.close()
        print("  --> PASS: Data persistence confirmed.\n")

        print("=======================================================")
        print("All 20 verification tests PASSED successfully!")
        print("=======================================================\n")

if __name__ == '__main__':
    unittest.main()
