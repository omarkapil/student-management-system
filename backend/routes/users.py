from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User

users_bp = Blueprint('users', __name__)


@users_bp.route('/users')
@login_required
def list_users():
    users = User.query.order_by(User.date_created.desc()).all()
    return render_template('users.html', users=users)


@users_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()[:150]
        email    = request.form.get('email', '').strip()[:150]
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not username or len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return redirect(url_for('users.add_user'))

        if not email or '@' not in email:
            flash('A valid email address is required.', 'error')
            return redirect(url_for('users.add_user'))

        if not password or len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return redirect(url_for('users.add_user'))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('users.add_user'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('users.add_user'))

        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'error')
            return redirect(url_for('users.add_user'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='scrypt')
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f'User "{username}" added successfully.', 'success')
        return redirect(url_for('users.list_users'))

    return render_template('add_user.html')


@users_bp.route('/users/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_user(id):
    if current_user.id == id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(url_for('users.list_users'))

    user = db.session.get(User, id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('users.list_users'))

    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User "{user.username}" has been {status}.', 'success')
    return redirect(url_for('users.list_users'))


@users_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if current_user.id == id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('users.list_users'))

    user = db.session.get(User, id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('users.list_users'))

    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{username}" deleted successfully.', 'success')
    return redirect(url_for('users.list_users'))
