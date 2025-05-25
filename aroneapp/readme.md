# arone Authentication App

This is a simple Flask web application featuring user registration, login, logout, and protected routes.  
It uses Flask-Login for session management, Flask-WTF for form handling and CSRF protection, and SQLAlchemy with environment-configured database connection.

---

## Features

- User registration with password hashing (Werkzeug security)
- User login with session management (Flask-Login)
- CSRF protection on all forms (Flask-WTF)
- Protected dashboard page accessible only to logged-in users
- Logout functionality
- Database connection via environment variables (`.env` file support)

---

## Technologies Used

-blinker
-click
-colorama
-Flask
-Flask-Login
-Flask-SQLAlchemy
-Flask-WTF
-greenlet
-gunicorn
-itsdangerous
-Jinja2
-MarkupSafe
-packaging
-python-dotenv
-SQLAlchemy
-typing_extensions
-Werkzeug
-WTForms


---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Ekenesamuel8/aroneintview.git

cd aroneapp

python -m venv venv

source venv/bin/activate #on mac
venv\Scripts\activate # On Windows

pip install -r requirements.txt

python app.py
