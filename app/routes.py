# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

# Home / Landing page (renders templates/index.html)
@main_bp.route('/')
def index():
    # If you want to redirect logged-in users to dashboard automatically:
    # if current_user.is_authenticated:
    #     return redirect(url_for('student.dashboard'))
    return render_template('index.html')


# Dashboard route (keeps your existing behavior)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    # If you want admin-specific logic later, put it here
    # e.g. if current_user.is_admin: ...
    return redirect(url_for('student.dashboard'))


@main_bp.route('/admin')
@login_required
def admin_dashboard():
    return "Admin dashboard placeholder"


# Simple placeholder signup/login routes (render or return content)
@main_bp.route('/signup')
def student_signup():
    # You can replace with: return render_template('auth/signup.html')
    return render_template('signup.html') if _template_exists('signup.html') else "signup page"


@main_bp.route('/login')
def login():
    # Replace with your login template/logic if you have one
    return render_template('login.html') if _template_exists('login.html') else "login page"


# Create an endpoint that matches url_for('student.dashboard') used earlier.
# We explicitly set the endpoint string to 'student.dashboard' so existing redirects work.
@main_bp.route('/student/dashboard', endpoint='student.dashboard')
@login_required
def student_dashboard():
    # Render the real student dashboard if you have it, else placeholder
    return render_template('student/dashboard.html') if _template_exists('student/dashboard.html') else "student dashboard"


# small helper: safe-check if a template file exists (avoid TemplateNotFound)
def _template_exists(name):
    """
    Small helper to check for template existence without throwing TemplateNotFound
    (Useful during initial development). Returns True if Jinja can load it.
    """
    try:
        # import here to avoid circular import at top-level
        from flask import current_app
        loader = current_app.jinja_loader
        if loader is None:
            return False
        found = loader.list_templates()
        return name in found
    except Exception:
        return False
# temporary debug route - put in routes.py and restart app
from flask import current_app

@main_bp.route('/_list_templates')
def _list_templates():
    loader = current_app.jinja_loader
    if not loader:
        return "No jinja loader"
    return "<pre>" + "\n".join(sorted(loader.list_templates())) + "</pre>"
# DEBUG ONLY - add to app/routes.py
from flask import current_app, jsonify
@main_bp.route('/_debug_templates')
def _debug_templates():
    loader = current_app.jinja_loader
    templates = sorted(loader.list_templates()) if loader else []
    return jsonify({
        "template_folder": current_app.template_folder,
        "templates_count": len(templates),
        "templates_sample": templates[:200]  # long list truncated
    })
@main_bp.route('/_debug_templates')
def _debug_templates():
    loader = current_app.jinja_loader
    templates = sorted(loader.list_templates()) if loader else []
    return jsonify({
        "app_root_path": current_app.root_path,
        "template_folder_setting": current_app.template_folder,
        "template_folder_abs_path": os.path.join(current_app.root_path, current_app.template_folder),
        "templates_count": len(templates),
        "has_auth_signup": 'auth/signup.html' in templates,
        "sample_templates": templates[:200]
    })
