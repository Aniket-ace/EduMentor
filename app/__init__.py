import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from .routes import main_bp

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    # 🔹 Force Flask to use the root-level "templates" folder
    project_root = os.path.abspath(os.getcwd())
    templates_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates')

    app = Flask(__name__, template_folder="templates", static_folder="static")

    # App configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///edumentor_dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Example config (change SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY = "replace_this_with_a_real_secret",
        DEBUG = True
    )

    # Register blueprints
    app.register_blueprint(main_bp)

    # Initialize other extensions here (db, login, migrate) if you use them
    # e.g. login_manager.init_app(app)
    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from .auth import auth_bp
    from .routes import main_bp
    from .student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)

    return app
def create_app():
    base = os.path.abspath(os.path.dirname(__file__))  # app package folder
    # ensure template_folder points to the top-level templates folder (project_root/templates)
    # adjust '..' if your templates are at project_root/templates
    template_folder = os.path.join(base, '..', 'templates')
    app = Flask(__name__, template_folder=template_folder, static_folder="static")
    app.config.from_mapping(SECRET_KEY="replace_this", DEBUG=True)
    app.register_blueprint(main_bp)
    return app
