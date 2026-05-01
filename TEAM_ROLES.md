# 👥 Team Roles — Student Management System
**Helwan International Technological University — HCI & Cybersecurity Project**

---

## 🐢 Meet the Team

| Ninja Name | Member | Role |
|------------|--------|------|
| 🍕 Michelangelo | عمر قابيل (Omar Kapil) | Database |
| 🔧 Donatello | مازن علاء (Mazen Alaa) | UI / Frontend |
| 🗡️ Raphael | يوسف علي (Youssef Ali) | Testing & QA |
| 🔵 Leonardo | محمد شعبان (Mohamed Shaaban) | Security |

---

## 🗄️ عمر قابيل — Database (Michelangelo 🍕)

**Responsibility:** Designing and managing the database schema, models, and all data-layer logic.

| File | Description |
|------|-------------|
| `backend/models/__init__.py` | Core database models — `User` & `Student` tables, all fields, relationships |
| `backend/routes/students.py` | CRUD operations — Add, Edit, Delete, Search student records |
| `backend/routes/dashboard.py` | Dashboard statistics pulled from the database |
| `.env.example` | Environment variable template (secret key, DB config) |
| `requirements.txt` | Project dependencies including Flask-SQLAlchemy |

**Key contributions:**
- Designed the ERD (Entity Relationship Diagram)
- Implemented `User` and `Student` SQLite models via Flask-SQLAlchemy
- Built parameterised queries to prevent SQL Injection
- Set up the database initialization and migration logic

---

## 🎨 مازن علاء — UI / Frontend (Donatello 🔧)

**Responsibility:** Designing and implementing all user interface elements, templates, and styling.

| File | Description |
|------|-------------|
| `backend/templates/` | All Jinja2 HTML templates (login, dashboard, student forms, etc.) |
| `backend/static/css/` | Custom CSS stylesheets |
| `backend/templates/base.html` | Base layout template (Bootstrap 5 integration, Font Awesome icons) |
| `backend/templates/dashboard.html` | Dashboard page UI |
| `backend/templates/students/` | Student list, add, edit, and detail page templates |

**Key contributions:**
- Applied HCI principles (learnability, visibility, robustness, flexibility)
- Integrated Bootstrap 5 and Font Awesome 6.0
- Built the password strength indicator on the registration page
- Designed confirmation dialogs before delete actions and flash alert messages
- Implemented client-side HTML5/JS input validation UI

---

## 🧪 يوسف علي — Testing & QA (Raphael 🗡️)

**Responsibility:** Verifying all features work correctly, writing and running test cases across the full system.

| File | Description |
|------|-------------|
| `backend/routes/auth.py` | Auth flows tested — login, register, logout |
| `backend/routes/students.py` | CRUD operations tested end-to-end |
| `backend/routes/dashboard.py` | Dashboard data accuracy verified |
| `backend/models/__init__.py` | Model integrity and constraint testing |
| `backend/templates/` | UI rendering and form validation testing |

**Key contributions:**
- Tested all student CRUD operations (Create, Read, Update, Delete)
- Verified search functionality across Name, Code, Course, and Year fields
- Validated brute-force lockout behaviour (5 failed logins → 15-min lockout)
- Tested form validation — both client-side and server-side responses
- Cross-browser and usability testing aligned with HCI principles

---

## 🔒 محمد شعبان — Security (Leonardo 🔵)

**Responsibility:** Implementing and auditing all security features across the application.

| File | Description |
|------|-------------|
| `backend/app.py` | Main Flask app — CSRF protection setup (`Flask-WTF CSRFProtect`), debug mode config |
| `backend/routes/auth.py` | Login/Register/Logout — password hashing, brute-force lockout logic |
| `backend/models/__init__.py` | `failed_logins` and `locked_until` fields for account lockout |
| `.env.example` | Secure secret key loaded from environment (never hardcoded) |
| `run.sh` / `run.bat` | Secure run scripts with environment setup |

**Key contributions:**
- Implemented password hashing using the `scrypt` algorithm (Werkzeug)
- Set up CSRF protection on all POST forms via `Flask-WTF`
- Built brute-force protection — account locked after 5 failed login attempts (15-minute lockout)
- Ensured SQL Injection prevention via SQLAlchemy ORM parameterised queries
- Configured secure secret key loading from environment variables
- Disabled debug mode for production to prevent code exposure

---

## 🗂️ Project Structure Overview

```
student_management_system/
├── backend/
│   ├── app.py                  ← 🔒 Security (Mohamed)
│   ├── models/
│   │   └── __init__.py         ← 🗄️ Database (Omar)
│   ├── routes/
│   │   ├── auth.py             ← 🔒 Security (Mohamed) + 🧪 Testing (Youssef)
│   │   ├── students.py         ← 🗄️ Database (Omar) + 🧪 Testing (Youssef)
│   │   └── dashboard.py        ← 🗄️ Database (Omar) + 🧪 Testing (Youssef)
│   ├── templates/              ← 🎨 UI (Mazen)
│   └── static/css/             ← 🎨 UI (Mazen)
├── .env.example                ← 🗄️ Database + 🔒 Security
├── requirements.txt            ← 🗄️ Database (Omar)
├── run.bat / run.sh            ← 🔒 Security (Mohamed)
└── README.md
```

---

*Helwan International Technological University — HCI & Cybersecurity Project*
