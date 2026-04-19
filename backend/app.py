from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import Markup
import os
from datetime import datetime

app = Flask(__name__)

# ============================================================
# SECURITY: Secret key loaded from environment variable.
# Set SECRET_KEY env var in production to a strong random value.
# Fallback uses os.urandom so the key is never predictable.
# ============================================================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True   # CSRF protection ON

# CSRF Protection (prevents Cross-Site Request Forgery attacks)
csrf = CSRFProtect(app)

from models import db
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Custom Jinja2 filter for highlighting search results
@app.template_filter('highlight')
def highlight_filter(text, query):
    if not query or not text:
        return text
    import re
    highlighted = re.sub(f'({re.escape(query)})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return Markup(highlighted)

# Import models and routes after app initialization
from models import User, Student
from routes.auth import auth_bp as auth
from routes.students import students_bp as students
from routes.dashboard import dashboard_bp as dashboard

app.register_blueprint(auth)
app.register_blueprint(students)
app.register_blueprint(dashboard)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard.dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Ensure year column exists for existing student tables
        try:
            result = db.session.execute(db.text("PRAGMA table_info(students)")).all()
            columns = [row[1] for row in result]
            if 'year' not in columns:
                db.session.execute(db.text('ALTER TABLE students ADD COLUMN year VARCHAR(50)'))
                db.session.commit()
        except Exception:
            db.session.rollback()

        # Create default admin user if no users exist
        if not User.query.first():
            default_user = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123', method='scrypt')
            )
            db.session.add(default_user)
            db.session.commit()
            print("Default admin created: email='admin@example.com', password='admin123'")

    # SECURITY: debug=False prevents code/traceback exposure to users
    app.run(debug=False)
