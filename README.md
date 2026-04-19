# Student Management System
**Helwan International Technological University — HCI & Cybersecurity Project**

---

## Project Description
A web-based Student Management System built with Python (Flask) and SQLite.
The system allows authorised staff to add, edit, delete, and search student records
through a clean, secure web interface.

---

## Technologies Used
| Layer      | Technology          | Version  |
|------------|---------------------|----------|
| Backend    | Python / Flask      | 3.x / 3.x|
| ORM        | Flask-SQLAlchemy    | 3.x      |
| Database   | SQLite              | built-in |
| Auth       | Flask-Login         | 0.6.x    |
| Security   | Flask-WTF (CSRF)    | 1.x      |
| Frontend   | Bootstrap 5         | 5.1.3    |
| Icons      | Font Awesome        | 6.0      |
| IDE        | VS Code             |          |

---

## Security Features Implemented
1. **Password Hashing** — `scrypt` algorithm (Werkzeug)
2. **CSRF Protection** — Flask-WTF CSRFProtect on all POST forms
3. **Brute-Force Protection** — Account locked after 5 failed logins (15 min lockout)
4. **Input Validation** — Both client-side (HTML5/JS) and server-side (Python)
5. **SQL Injection Prevention** — SQLAlchemy ORM with parameterised queries
6. **Secure Secret Key** — Loaded from environment variable (never hardcoded)
7. **Debug Mode OFF** — Prevents code exposure in production

---

## HCI Principles Applied
| Principle     | Implementation                                              |
|---------------|-------------------------------------------------------------|
| Learnability  | Clear labels, icons, and helper text on every form field    |
| Robustness    | Confirmation dialog before delete; flash alerts for errors  |
| Flexibility   | Search by Name, Code, Course, or Year                       |
| Visibility    | Password strength indicator on registration page            |
| Error Prevention | Client-side + server-side validation; live code preview  |

---

## Database Schema (ERD)

```
┌─────────────────────┐       ┌──────────────────────────┐
│       users         │       │         students          │
├─────────────────────┤       ├──────────────────────────┤
│ id          INTEGER │       │ id           INTEGER PK   │
│ username    VARCHAR │       │ name         VARCHAR(150) │
│ email       VARCHAR │       │ student_code VARCHAR(50)  │
│ password    VARCHAR │       │ email        VARCHAR(150) │
│ failed_logins INT   │       │ course       VARCHAR(100) │
│ locked_until DATETIME│       │ year         VARCHAR(50)  │
│ date_created DATETIME│       │ date_created DATETIME     │
└─────────────────────┘       └──────────────────────────┘
        (manages)
```

---

## How to Run
```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
cd backend
python app.py

# 4. Open browser at http://127.0.0.1:5000
# Default admin: email=admin@example.com  password=admin123
```

---

## Project Structure
```
student_management_system/
├── backend/
│   ├── app.py              # Flask app, CSRF setup
│   ├── models/
│   │   └── __init__.py     # User & Student database models
│   ├── routes/
│   │   ├── auth.py         # Login / Register / Logout
│   │   ├── students.py     # CRUD + Search + Export
│   │   └── dashboard.py    # Dashboard statistics
│   ├── templates/          # Jinja2 HTML templates
│   └── static/css/         # Custom CSS
└── README.md
```
