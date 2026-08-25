# app/inspect_student.py
from app import create_app

app = create_app()
with app.app_context():
    from app.models import Student
    print("Student class:", Student)
    print("Has attribute 'username'? ->", hasattr(Student, 'username'))
    try:
        cols = [c.key for c in Student.__table__.columns]
        print("SQLAlchemy columns:")
        for c in cols:
            print("  -", c)
    except Exception as e:
        print("No __table__ or error:", e)
