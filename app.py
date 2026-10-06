import os
from flask import Flask, render_template, session, redirect, url_for, flash
from config import Config
import database

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    
    if test_config is not None:
        app.config.from_mapping(test_config)

    # Ensure the upload and instance directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize Database & seed demo accounts if database file does not exist
    if not os.path.exists(app.config['DATABASE']):
        database.init_db(app.config['DATABASE'])

    database.init_app(app)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.faculty_routes import faculty_bp
    from routes.search_routes import search_bp
    from routes.analytics_routes import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(analytics_bp)

    @app.template_filter('date_format')
    def date_format(value):
        if not value:
            return ""
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        return str(value)[:10]

    @app.context_processor
    def inject_user_context():
        """Injects authentication state and dynamic network IP into all Jinja templates."""
        import socket
        def get_ip():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except Exception:
                return "127.0.0.1"

        return {
            'is_authenticated': 'user_id' in session,
            'current_user_id': session.get('user_id'),
            'current_user_name': session.get('user_name'),
            'current_user_email': session.get('user_email'),
            'current_user_role': session.get('user_role'),
            'current_user_dept': session.get('user_department'),
            'local_ip': get_ip()
        }

    @app.route('/')
    def landing():
        """Landing Page showing Hero, Live Stats, Problems, Workflow, and Roadmap."""
        # Query preview data for the hero dashboard preview
        try:
            db = database.get_db()
            total_projects = db.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
            pending_count = db.execute("SELECT COUNT(*) FROM projects WHERE status = 'Pending'").fetchone()[0]
            approved_count = db.execute("SELECT COUNT(*) FROM projects WHERE status = 'Approved'").fetchone()[0]
            top_skills = db.execute("SELECT tag, COUNT(*) as c FROM project_tags WHERE tag_type = 'skill' GROUP BY tag ORDER BY c DESC LIMIT 4").fetchall()
            recent_projects = db.execute("SELECT title, domain, status, created_at FROM projects ORDER BY created_at DESC LIMIT 3").fetchall()
        except Exception:
            total_projects = 0
            pending_count = 0
            approved_count = 0
            top_skills = []
            recent_projects = []

        return render_template(
            'landing.html',
            total_projects=total_projects,
            pending_count=pending_count,
            approved_count=approved_count,
            top_skills=top_skills,
            recent_projects=recent_projects
        )

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', custom_error="404: The requested page could not be found."), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        flash("File upload exceeds the 16MB maximum permitted size.", "danger")
        return redirect(request.referrer or url_for('student.dashboard')), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', custom_error="500: An unexpected internal server error occurred."), 500

    return app

app = create_app()

if __name__ == '__main__':
    from threading import Thread
    from werkzeug.serving import run_simple
    
    port_env = os.environ.get('PORT')
    if port_env:
        # Running in cloud environment (e.g., Render, Railway) with assigned PORT
        cloud_port = int(port_env)
        print(f"[UniFolio] Running on assigned Cloud PORT {cloud_port} ...")
        app.run(host='0.0.0.0', port=cloud_port)
    else:
        # Local development: start multi-port listener (80 and 5000)
        def run_port_80():
            try:
                run_simple('0.0.0.0', 80, app, use_reloader=False, threaded=True)
            except Exception:
                pass

        t = Thread(target=run_port_80, daemon=True)
        t.start()

        print("[UniFolio] Local development server running on http://127.0.0.1:5000 and port 80")
        run_simple('0.0.0.0', 5000, app, use_reloader=False, threaded=True)
