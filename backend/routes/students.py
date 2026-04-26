import re
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from models import db, Student
import csv
from io import StringIO

students_bp = Blueprint('students', __name__)


def normalize_student_code(code):
    """Normalise a user-supplied code to STU-XXXXXXX format."""
    if not code:
        return ''
    cleaned = re.sub(r'\s+', '', code.strip()).upper()
    if cleaned.startswith('STU-'):
        return cleaned
    if cleaned.startswith('STU'):
        return 'STU-' + cleaned[3:].lstrip('-')
    return 'STU-' + cleaned


def is_valid_student_code(code):
    """Validate that the code matches STU-XXXXXXX (exactly 7 digits)."""
    return bool(re.match(r'^STU-\d{7}$', code))


def sanitize_text(value, max_len=150):
    """Strip leading/trailing whitespace and enforce max length."""
    if not value:
        return ''
    return str(value).strip()[:max_len]


@students_bp.route('/students')
@login_required
def list_students():
    page          = request.args.get('page', 1, type=int)
    per_page      = 10
    students_list = Student.query.order_by(Student.date_created.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template('students.html', students=students_list)


@students_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name         = sanitize_text(request.form.get('name'))
        student_code = normalize_student_code(request.form.get('student_code'))
        email        = sanitize_text(request.form.get('email'))
        course       = sanitize_text(request.form.get('course'))
        year         = sanitize_text(request.form.get('year'))

        # Server-side validation (Input Validation → prevents bad data & SQL injection)
        if not name:
            flash('Student name is required.', 'error')
            return redirect(url_for('students.add_student'))

        if not is_valid_student_code(student_code):
            flash('Student code must start with STU- followed by exactly 7 digits (e.g. STU-0001234).', 'error')
            return redirect(url_for('students.add_student'))

        if not email or '@' not in email:
            flash('A valid email address is required.', 'error')
            return redirect(url_for('students.add_student'))

        if not course:
            flash('Please select a course.', 'error')
            return redirect(url_for('students.add_student'))

        # Duplicate check
        if Student.query.filter_by(student_code=student_code).first():
            flash('Student code already exists.', 'error')
            return redirect(url_for('students.add_student'))

        new_student = Student(
            name=name, student_code=student_code,
            email=email, course=course, year=year
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully.', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('add_student.html')


@students_bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = db.session.get(Student, id)
    if not student:
        abort(404)

    if request.method == 'POST':
        name         = sanitize_text(request.form.get('name'))
        student_code = normalize_student_code(request.form.get('student_code'))
        email        = sanitize_text(request.form.get('email'))
        course       = sanitize_text(request.form.get('course'))
        year         = sanitize_text(request.form.get('year'))

        # Server-side validation
        if not name:
            flash('Student name is required.', 'error')
            return redirect(url_for('students.edit_student', id=id))

        if not is_valid_student_code(student_code):
            flash('Student code must start with STU- followed by exactly 7 digits.', 'error')
            return redirect(url_for('students.edit_student', id=id))

        if not email or '@' not in email:
            flash('A valid email address is required.', 'error')
            return redirect(url_for('students.edit_student', id=id))

        # Duplicate check (exclude current student)
        existing = Student.query.filter_by(student_code=student_code).first()
        if existing and existing.id != id:
            flash('Student code already exists for another student.', 'error')
            return redirect(url_for('students.edit_student', id=id))

        student.name         = name
        student.student_code = student_code
        student.email        = email
        student.course       = course
        student.year         = year
        db.session.commit()
        flash('Student updated successfully.', 'success')
        return redirect(url_for('students.list_students'))

    return render_template('edit_student.html', student=student)


@students_bp.route('/students/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    student = db.session.get(Student, id)
    if not student:
        abort(404)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('students.list_students'))


@students_bp.route('/students/search')
@login_required
def search_students():
    query     = sanitize_text(request.args.get('q', ''))
    search_by = request.args.get('search_by', 'name')
    date_from = request.args.get('date_from', '').strip()
    date_to   = request.args.get('date_to', '').strip()

    allowed_fields = {'name', 'student_code', 'course', 'year'}
    if search_by not in allowed_fields:
        search_by = 'name'

    field_map = {
        'name':         Student.name,
        'student_code': Student.student_code,
        'course':       Student.course,
        'year':         Student.year,
    }

    base_query = Student.query

    if query:
        base_query = base_query.filter(field_map[search_by].ilike(f'%{query}%'))

    if date_from:
        try:
            df = datetime.strptime(date_from, '%Y-%m-%d')
            base_query = base_query.filter(Student.date_created >= df)
        except ValueError:
            date_from = ''

    if date_to:
        try:
            dt = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            base_query = base_query.filter(Student.date_created < dt)
        except ValueError:
            date_to = ''

    students_list = base_query.all() if (query or date_from or date_to) else []

    return render_template(
        'search_results.html',
        students=students_list, query=query, search_by=search_by,
        date_from=date_from, date_to=date_to
    )


@students_bp.route('/courses')
@login_required
def list_courses():
    COURSE_ICONS = {
        'AI':                   'fas fa-robot',
        'Cyber Security':       'fas fa-shield-alt',
        'Data Science':         'fas fa-chart-bar',
        'Software Engineering': 'fas fa-laptop-code',
    }
    COURSE_COLORS = {
        'AI':                   'primary',
        'Cyber Security':       'danger',
        'Data Science':         'success',
        'Software Engineering': 'info',
    }
    all_courses = ['AI', 'Cyber Security', 'Data Science', 'Software Engineering']
    students_all = Student.query.order_by(Student.name).all()

    grouped = {c: [] for c in all_courses}
    for s in students_all:
        if s.course in grouped:
            grouped[s.course].append(s)
        else:
            grouped[s.course] = [s]

    # Include any courses not in the predefined list
    for c in list(grouped.keys()):
        if c not in all_courses:
            all_courses.append(c)
            COURSE_ICONS[c]  = 'fas fa-book'
            COURSE_COLORS[c] = 'secondary'

    return render_template(
        'courses.html',
        grouped=grouped,
        all_courses=all_courses,
        course_icons=COURSE_ICONS,
        course_colors=COURSE_COLORS,
    )


@students_bp.route('/students/export')
@login_required
def export_students():
    students_list = Student.query.all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Student Code', 'Email', 'Course', 'Year', 'Date Created'])
    for s in students_list:
        cw.writerow([s.id, s.name, s.student_code, s.email,
                     s.course, s.year or '', s.date_created])
    output = si.getvalue()
    si.close()
    return output, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=students.csv'
    }
