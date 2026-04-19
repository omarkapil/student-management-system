from flask import Blueprint, render_template
from flask_login import login_required
from models import db, Student

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    total_students = Student.query.count()
    recent_students = Student.query.order_by(Student.date_created.desc()).limit(5).all()
    return render_template('dashboard.html', total_students=total_students, recent_students=recent_students)