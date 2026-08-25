# app/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student
from . import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def _is_safe_next(next_url: str) -> bool:
    """Very small safety check: only allow relative paths within this site."""
    return bool(next_url) and next_url.startswith('/')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        identifier = (request.form.get('identifier') or request.form.get('email') or '').strip()
        password = request.form.get('password') or ''

        if not identifier or not password:
            flash('Please provide email (or name) and password', 'error')
            return render_template('auth/login.html')

        # Try finding by email first, then by name
        user = Student.query.filter_by(email=identifier).first()
        if not user:
            user = Student.query.filter_by(name=identifier).first()

        pw_ok = False
        if user:
            pw_hash = getattr(user, 'password_hash', None)
            if pw_hash:
                try:
                    pw_ok = check_password_hash(pw_hash, password)
                except Exception:
                    pw_ok = False
            elif hasattr(user, 'check_password'):
                pw_ok = user.check_password(password)
            else:
                # last-resort (not recommended) plaintext check
                pw_ok = getattr(user, 'password', None) == password

        if user and pw_ok:
            login_user(user)
            next_page = request.args.get('next')
            if _is_safe_next(next_page):
                return redirect(next_page)
            return redirect(url_for('student.dashboard'))

        flash('Invalid email/name or password', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        name = (request.form.get('name') or request.form.get('username') or '').strip()
        password = request.form.get('password') or ''

        if not email or not password:
            flash('Please provide email and password', 'error')
            return render_template('auth/signup.html')

        if Student.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('auth/signup.html')

        # create student (use `name` field in model)
        user = Student(email=email, name=name)
        user.password_hash = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        flash('Account created — please log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('main.index'))
