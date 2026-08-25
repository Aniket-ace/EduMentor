# EduMentor

EduMentor is a Flask-based student performance dashboard that helps students track academic progress, attendance, and learning preferences in one place.

## Features

- Student registration, login, and logout
- Subject-wise marks: add, edit, and delete records
- Attendance tracking with percentage calculation
- Interactive charts for marks and attendance
- Personalized recommendations based on marks and attendance
- Learning-style preference: Visual, Auditory, Kinesthetic, or Reading/Writing
- SQLite database with Flask-SQLAlchemy and database migrations

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- SQLite
- Chart.js

## Project Structure

```
EduMentor/
├── app/            # Flask routes, models, authentication, student features
├── templates/      # Jinja HTML templates
├── migrations/     # Database migrations
├── requirements.txt
└── run.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Aniket-ace/EduMentor.git
cd EduMentor
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

```bash
flask db upgrade
```

### 5. Run the application

```bash
python run.py
```

Then open http://127.0.0.1:5000 in your browser.

## Notes

- The local SQLite database and virtual environment are excluded from Git.
- This project is intended as a student dashboard demo and learning project.
