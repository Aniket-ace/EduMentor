# test_dashboard_template.py
import os
from app import create_app
from flask import render_template

app = create_app()

with app.app_context():
    template_folder = app.template_folder
    path = os.path.join(template_folder, 'student', 'dashboard.html')
    print("Template folder:", template_folder)
    print("Dashboard path:", path)
    print("Exists on disk:", os.path.exists(path))

    # Try rendering (this will raise an exception if template can't be loaded)
    try:
        s = render_template('student/dashboard.html', 
                            user=type('U',(),{'name':'TestUser'})(),
                            marks=[], attendance=[], subject_averages={}, attendance_pct=None)
        print("Rendered ok — length:", len(s))
    except Exception as e:
        print("Render error:", type(e).__name__, e)
