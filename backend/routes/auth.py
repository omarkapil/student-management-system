from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models import db, User
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# ============================================================
# Brute-Force Protection constants
# After MAX_FAILED_ATTEMPTS wrong passwords the account is
# locked for LOCKOUT_MINUTES minutes.
# ============================================================
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES     = 15


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Basic input validation
        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user:
            # ---- Lockout check ----
            if user.locked_until and datetime.utcnow() < user.locked_until:
                remaining = int((user.locked_until - datetime.utcnow()).total_seconds() // 60) + 1
                flash(
                    f'Account locked due to too many failed attempts. '
                    f'Please try again in {remaining} minute(s).',
                    'error'
                )
                return render_template('login.html')

            # ---- Password check ----
            if check_password_hash(user.password, password):
                # Reset failed counter on success
                user.failed_logins = 0
                user.locked_until  = None
                db.session.commit()
                login_user(user)
                return redirect(url_for('dashboard.dashboard'))
            else:
                # Wrong password → increment counter
                user.failed_logins = (user.failed_logins or 0) + 1
                if user.failed_logins >= MAX_FAILED_ATTEMPTS:
                    user.locked_until  = datetime.utcnow() + timedelta(minutes=LOCKOUT_MINUTES)
                    user.failed_logins = 0
                    db.session.commit()
                    flash(
                        f'Too many failed attempts. Account locked for {LOCKOUT_MINUTES} minutes.',
                        'error'
                    )
                else:
                    remaining_attempts = MAX_FAILED_ATTEMPTS - user.failed_logins
                    db.session.commit()
                    flash(
                        f'Incorrect password. {remaining_attempts} attempt(s) remaining.',
                        'error'
                    )
        else:
            # Generic message (don't reveal whether email exists)
            flash('Login unsuccessful. Please check your email and password.', 'error')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Server-side validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email address already exists.', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
        else:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='scrypt')
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. Please sign in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
