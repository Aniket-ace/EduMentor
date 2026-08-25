from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from collections import defaultdict
from . import db
from .models import Mark, Attendance, Student
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user

    # fetch per-student data
    marks = Mark.query.filter_by(student_id=user.id).order_by(Mark.exam_date.desc()).all()
    attendance = Attendance.query.filter_by(student_id=user.id).order_by(Attendance.date.desc()).all()

    # --- subject averages ---
    subject_aggregates = defaultdict(list)
    for m in marks:
        # guard against None values
        obtained = m.marks_obtained or 0
        maximum  = m.max_marks or 0
        subject_aggregates[m.subject].append((obtained, maximum))

    subject_averages = {}
    for subj, vals in subject_aggregates.items():
        total_marks = sum(v[0] for v in vals)
        total_max   = sum(v[1] for v in vals)
        avg_percent = round((total_marks / total_max) * 100, 2) if total_max > 0 else 0
        subject_averages[subj] = avg_percent

    # --- Attendance: counts and safe percentage ---
    total_days = len(attendance)
    present_days = sum(1 for a in attendance if getattr(a, 'present', False))

    present_days = int(present_days or 0)
    total_days   = int(total_days or 0)

    attendance_pct = round((present_days / total_days) * 100, 2) if total_days > 0 else None

    # --- Recommendations ---
    recommendations = []
    for subj, avg in subject_averages.items():
        if avg < 50:
            recommendations.append(f"⚠️ Work on {subj}: average {avg}%")
        elif avg > 75:
            recommendations.append(f"🏆 Great job in {subj}: average {avg}%")
    if attendance_pct is not None and attendance_pct < 75:
        recommendations.append("📌 Your attendance is below 75% — try to attend more classes!")

    # prepare lists for charts (optional)
    subjects_raw    = list(subject_averages.keys())
    avg_percents    = [subject_averages[s] for s in subjects_raw]
    marks_obtained  = [m.marks_obtained for m in marks]
    max_marks_list  = [m.max_marks for m in marks]

    return render_template(
        "student/dashboard.html",
        user=user,
        marks=marks,
        attendance=attendance,
        subject_averages=subject_averages,
        present_days=present_days,
        total_days=total_days,
        attendance_pct=attendance_pct,
        recommendations=recommendations,
        subjects_raw=subjects_raw,
        marks_obtained=marks_obtained,
        max_marks=max_marks_list,
        avg_percents=avg_percents,
    )


# Form to add a mark
@student_bp.route('/marks/add', methods=['GET', 'POST'])
@login_required
def add_mark():
    if request.method == 'POST':
        subject = (request.form.get('subject') or "").strip()
        marks_obtained = request.form.get('marks_obtained')
        max_marks = request.form.get('max_marks')
        exam_date = request.form.get('exam_date') or datetime.utcnow().date().isoformat()

        # validate and coerce
        try:
            marks_obtained = float(marks_obtained)
            max_marks = float(max_marks)
            exam_date = datetime.fromisoformat(exam_date).date() if isinstance(exam_date, str) else exam_date
        except Exception:
            flash('Please enter valid numeric marks and a valid date.', 'danger')
            return redirect(url_for('student.add_mark'))

        m = Mark(
            student_id=current_user.id,
            subject=subject,
            marks_obtained=marks_obtained,
            max_marks=max_marks,
            exam_date=exam_date
        )
        db.session.add(m)
        db.session.commit()
        flash('Mark added.', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('student/add_mark.html')


# Edit mark
@student_bp.route('/marks/<int:mark_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_mark(mark_id):
    mark = Mark.query.get_or_404(mark_id)
    if mark.student_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        try:
            mark.subject = request.form.get('subject', mark.subject)
            mark.marks_obtained = float(request.form.get('marks_obtained', mark.marks_obtained))
            mark.max_marks = float(request.form.get('max_marks', mark.max_marks))
            exam_date_raw = request.form.get('exam_date')
            if exam_date_raw:
                mark.exam_date = datetime.fromisoformat(exam_date_raw).date()
            db.session.commit()
            flash("Mark updated successfully", "success")
        except Exception:
            db.session.rollback()
            flash("Invalid input when updating mark.", "danger")
        return redirect(url_for('student.dashboard'))
    return render_template('student/edit_mark.html', mark=mark)


# Delete mark
@student_bp.route('/marks/<int:mark_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_mark(mark_id):
    m = Mark.query.get_or_404(mark_id)
    if m.student_id != current_user.id and not getattr(current_user, "is_admin", False):
        abort(403)
    db.session.delete(m)
    db.session.commit()
    flash("Mark deleted", "info")
    return redirect(url_for('student.dashboard'))


# Attendance - add single day
@student_bp.route('/attendance/add', methods=['GET', 'POST'])
@login_required
def add_attendance():
    if request.method == 'POST':
        date_raw = request.form.get('date') or datetime.utcnow().date().isoformat()
        present = True if request.form.get('present') in ('1', 'on', 'true', 'True') else False
        try:
            date = datetime.fromisoformat(date_raw).date()
        except Exception:
            flash('Invalid date', 'danger')
            return redirect(url_for('student.add_attendance'))

        a = Attendance(student_id=current_user.id, date=date, present=present)
        db.session.add(a)
        db.session.commit()
        flash('Attendance recorded.', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('student/add_attendance.html')


# Edit attendance
@student_bp.route('/attendance/<int:attendance_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_attendance(attendance_id):
    a = Attendance.query.get_or_404(attendance_id)
    if a.student_id != current_user.id and not getattr(current_user, "is_admin", False):
        abort(403)
    if request.method == 'POST':
        date_raw = request.form.get('date')
        if date_raw:
            try:
                a.date = datetime.fromisoformat(date_raw).date()
            except Exception:
                flash('Invalid date', 'danger')
                return redirect(url_for('student.edit_attendance', attendance_id=attendance_id))
        a.present = True if request.form.get('present') in ('1', 'on', 'true', 'True') else False
        db.session.commit()
        flash('Attendance updated', 'success')
        return redirect(url_for('student.dashboard'))
    return render_template('student/edit_attendance.html', attendance=a)


# Delete attendance
@student_bp.route('/attendance/<int:att_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_attendance(att_id):
    att = Attendance.query.get_or_404(att_id)
    if att.student_id != current_user.id and not getattr(current_user, "is_admin", False):
        flash("Not authorized to delete this attendance", "error")
        return redirect(url_for('student.dashboard'))

    db.session.delete(att)
    db.session.commit()
    flash("Attendance record deleted", "info")
    return redirect(url_for('student.dashboard'))


# Learning style
@student_bp.route('/learning_style', methods=['GET', 'POST'])
@login_required
def learning_style():
    if request.method == 'POST':
        style = request.form.get('learning_style') or None
        student = Student.query.get(current_user.id)
        if student:
            student.learning_style = style
            db.session.commit()
            flash('Learning style updated.', 'success')
        else:
            flash('Student record not found.', 'danger')
        return redirect(url_for('student.dashboard'))

    return render_template('student/learning_style.html', current_style=getattr(current_user, "learning_style", None))
