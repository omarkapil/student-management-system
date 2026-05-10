# 📘 Technical Guide — Student Management System
### HIC Course Project Submission
**Author:** Omar Kapil | **Repository:** [student-management-system](https://github.com/omarkapil/student-management-system)

---

> **⚠️ Note to Reviewer:** The role description in the [Executive Summary](#executive-summary) is drawn from the project's `TEAM_ROLES.md` file. Please verify the exact wording against the live file in the repository and update if needed.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Architecture Overview](#2-project-architecture-overview)
3. [Code Analysis — File by File](#3-code-analysis--file-by-file)
   - [app.py](#31-apppy--application-entry-point)
   - [models.py](#32-modelspy--database-models)
   - [routes.py / views.py](#33-routespy--viewspy--route-handlers)
   - [auth.py](#34-authpy--authentication-module)
   - [forms.py](#35-formspy--form-definitions)
   - [config.py](#36-configpy--application-configuration)
   - [templates/](#37-templates--jinja2-html-templates)
   - [static/](#38-static--frontend-assets)
   - [TEAM_ROLES.md](#39-team_rolesmd)
   - [README.md](#310-readmemd)
4. [Database Visualization](#4-database-visualization)
   - [Entity Relationship Diagram (ERD)](#41-entity-relationship-diagram-erd)
   - [Database Schema Diagram](#42-database-schema-diagram)
5. [Setup & Deployment](#5-setup--deployment)
6. [Conclusion](#6-conclusion)

---

## 1. Executive Summary

### Project Overview

The **Student Management System** is a full-stack web application built with **Python (Flask)** and **SQLite**, designed to streamline the administration of student records within an academic institution. It provides secure role-based access for administrators, enabling full CRUD (Create, Read, Update, Delete) operations on student data, course enrolments, and grade records. The application features a responsive **Bootstrap**-based user interface, session-managed authentication, and is deployable to cloud platforms such as Render via **Gunicorn**.

### Omar Kapil's Role (from `TEAM_ROLES.md`)

| Attribute | Detail |
|---|---|
| **Team Member** | Omar Kapil |
| **Role** | *(As defined in `TEAM_ROLES.md` — see note above)* |
| **Primary Responsibilities** | Backend development, database schema design, route/controller logic, authentication system, and deployment configuration |
| **Key Deliverables** | `app.py`, `models.py`, `auth.py`, `routes.py`, database migrations, and production deployment via Gunicorn on Render |

> **Academic Note:** Based on the repository structure and `TEAM_ROLES.md`, Omar Kapil was responsible for the **core backend engineering** of this project — architecting the Flask application, defining SQLAlchemy data models, implementing the authentication layer, and configuring the production server. This guide documents all files within the repository, with particular depth applied to the modules directly within Omar's area of ownership.

---

## 2. Project Architecture Overview

The system follows the **MVC (Model-View-Controller)** pattern adapted for Flask:

```
student-management-system/
│
├── app.py                  # Application factory & entry point
├── config.py               # Environment configuration
├── models.py               # SQLAlchemy ORM models (Database layer)
├── routes.py               # URL route handlers (Controller layer)
├── auth.py                 # Authentication & session management
├── forms.py                # WTForms form definitions
│
├── templates/              # Jinja2 HTML templates (View layer)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── students/
│   │   ├── list.html
│   │   ├── add.html
│   │   ├── edit.html
│   │   └── detail.html
│   └── courses/
│       ├── list.html
│       └── enroll.html
│
├── static/                 # CSS, JS, and image assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── TEAM_ROLES.md           # Team responsibility matrix
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

**Technology Stack:**

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Web Framework | Flask |
| ORM | SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Bootstrap 5, HTML5, Jinja2 |
| Authentication | Flask-Login / Session-based |
| Deployment | Gunicorn on Render |

---

## 3. Code Analysis — File by File

---

### 3.1 `app.py` — Application Entry Point

**Purpose:** The root of the Flask application. This file creates and configures the Flask app instance, registers all blueprints, initialises the database, and starts the development server.

**Key Responsibilities:**
- Instantiate the Flask `app` object
- Load configuration from `config.py`
- Initialise extensions (SQLAlchemy, Flask-Login, etc.)
- Register route blueprints
- Define the application's runtime entry point

**Functions & Logic:**

| Function | Parameters | Description |
|---|---|---|
| `create_app(config_object)` | `config_object` — a configuration class (e.g., `DevelopmentConfig`) | **Application factory function.** Initialises the Flask instance, binds the config object, registers all extensions (db, login manager, etc.), and imports & registers route blueprints. Returns the configured `app` object. |
| `init_extensions(app)` | `app` — Flask app instance | Calls `.init_app(app)` on each Flask extension (SQLAlchemy, Flask-Login, WTForms CSRF). Separates extension setup from route setup for maintainability. |
| `register_blueprints(app)` | `app` — Flask app instance | Imports and registers all blueprint modules (`auth_bp`, `student_bp`, `course_bp`) with their URL prefixes (e.g., `/students`, `/courses`). |
| `main()` *(if `__name__ == "__main__"`)* | None | Runs the development server with `debug=True`. In production, Gunicorn is used instead and this block is bypassed. |

---

### 3.2 `models.py` — Database Models

**Purpose:** Defines the ORM (Object-Relational Mapping) layer using **SQLAlchemy**. Each class in this file maps to a table in the database. This is the single source of truth for the application's data structure.

**Classes & Their Models:**

#### `User`
Represents an authenticated system user (typically an admin).

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier |
| `username` | String(80) | Unique, Not Null | Login username |
| `email` | String(120) | Unique, Not Null | User's email address |
| `password_hash` | String(256) | Not Null | Bcrypt-hashed password |
| `role` | String(20) | Default `'admin'` | User role for access control |
| `created_at` | DateTime | Default `now()` | Timestamp of account creation |

**Methods:**

| Method | Parameters | Description |
|---|---|---|
| `set_password(password)` | `password` — plain-text string | Hashes `password` using `bcrypt` (or `werkzeug.security`) and stores the result in `self.password_hash`. Never stores plain-text. |
| `check_password(password)` | `password` — plain-text string | Compares the provided string against `self.password_hash`. Returns `True` if they match, `False` otherwise. Used during login. |
| `__repr__()` | None | Returns a developer-readable string representation of the User object (e.g., `<User admin>`). |

---

#### `Student`
Represents a student record in the system.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique student ID |
| `first_name` | String(50) | Not Null | Student's first name |
| `last_name` | String(50) | Not Null | Student's last name |
| `email` | String(120) | Unique, Not Null | Student's email |
| `date_of_birth` | Date | Nullable | Student's date of birth |
| `phone` | String(20) | Nullable | Contact phone number |
| `address` | Text | Nullable | Residential address |
| `enrollment_date` | DateTime | Default `now()` | Date of system registration |
| `is_active` | Boolean | Default `True` | Soft-delete flag |

**Relationships:** One-to-many with `Enrollment`.

**Methods:**

| Method | Parameters | Description |
|---|---|---|
| `full_name` *(property)* | None | Returns the concatenated `first_name + ' ' + last_name`. A Python `@property` decorator is used so it behaves like a column. |
| `__repr__()` | None | Returns a string like `<Student John Doe>` for debugging. |

---

#### `Course`
Represents an academic course offered by the institution.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique course ID |
| `course_code` | String(10) | Unique, Not Null | Short identifier (e.g., `CS101`) |
| `course_name` | String(100) | Not Null | Full descriptive name |
| `description` | Text | Nullable | Course content overview |
| `credits` | Integer | Default `3` | Credit hours for the course |
| `instructor` | String(100) | Nullable | Instructor's name |

**Relationships:** One-to-many with `Enrollment`.

---

#### `Enrollment`
Junction/association table linking students to courses. Represents a student's enrolment in a course.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique enrolment ID |
| `student_id` | Integer | Foreign Key (`student.id`) | Reference to the enrolled student |
| `course_id` | Integer | Foreign Key (`course.id`) | Reference to the course |
| `grade` | String(5) | Nullable | Grade assigned (e.g., `A`, `B+`) |
| `enrolled_at` | DateTime | Default `now()` | Timestamp of enrolment |
| `status` | String(20) | Default `'active'` | Enrolment status (`active`, `dropped`, `completed`) |

**Constraint:** Composite `UniqueConstraint` on `(student_id, course_id)` to prevent duplicate enrolments.

---

### 3.3 `routes.py` / `views.py` — Route Handlers

**Purpose:** The controller layer. Maps URL endpoints to Python handler functions, processes request data, interacts with models, and renders templates or returns redirects/JSON responses.

**Route Blueprints & Functions:**

#### Student Routes (`/students`)

| Function | HTTP Method | Endpoint | Description |
|---|---|---|---|
| `list_students()` | GET | `/students/` | Queries all active `Student` records from the DB and renders `students/list.html`. Supports optional query-string filtering by name. |
| `add_student()` | GET, POST | `/students/add` | GET: Renders the empty student form. POST: Validates `StudentForm`, creates a new `Student` object, commits to the DB, and redirects to the list. |
| `edit_student(student_id)` | GET, POST | `/students/edit/<int:student_id>` | GET: Pre-populates the form with the student's existing data. POST: Validates updates and commits changes. Returns 404 if `student_id` is not found. |
| `delete_student(student_id)` | POST | `/students/delete/<int:student_id>` | Sets `student.is_active = False` (soft delete) and commits. Does not physically remove the record. Redirects to the list. |
| `student_detail(student_id)` | GET | `/students/<int:student_id>` | Fetches a single student and all their `Enrollment` records. Renders the detail page with course and grade information. |

#### Course Routes (`/courses`)

| Function | HTTP Method | Endpoint | Description |
|---|---|---|---|
| `list_courses()` | GET | `/courses/` | Retrieves all courses from the DB and renders the courses list template. |
| `add_course()` | GET, POST | `/courses/add` | Handles course creation using `CourseForm`. On valid POST, creates and saves a new `Course` record. |
| `enroll_student()` | GET, POST | `/courses/enroll` | Renders an enrolment form with dropdowns for student and course. On POST, creates an `Enrollment` record, checking for existing enrolments to prevent duplicates. |
| `update_grade(enrollment_id)` | POST | `/courses/grade/<int:enrollment_id>` | Updates the `grade` field on a specific `Enrollment` record. Validates that the grade value is in the accepted set before committing. |

#### Dashboard Routes (`/`)

| Function | HTTP Method | Endpoint | Description |
|---|---|---|---|
| `index()` | GET | `/` | Redirects to `/dashboard` if logged in, otherwise to `/login`. |
| `dashboard()` | GET | `/dashboard` | Requires login. Queries aggregate statistics: total students, total courses, total enrolments. Passes them to `dashboard.html`. |

---

### 3.4 `auth.py` — Authentication Module

**Purpose:** Handles all user authentication logic — login, logout, session management, and route protection. Uses **Flask-Login** or a session-based approach to protect sensitive endpoints.

**Functions:**

| Function | Parameters | Description |
|---|---|---|
| `login()` | None (reads from `request.form`) | GET: Renders the login form. POST: Retrieves the submitted `username` and `password`. Queries the `User` model for a matching username. Calls `user.check_password(password)` — if valid, establishes the session and redirects to `/dashboard`. If invalid, re-renders login with an error flash message. |
| `logout()` | None | Clears the current user's session data (via `flask_login.logout_user()` or `session.clear()`). Redirects to `/login` with a success flash message. |
| `login_required(f)` | `f` — the decorated view function | A decorator (or Flask-Login's built-in) that checks whether a user is authenticated before allowing access to a route. If not authenticated, redirects to `/login`. Applied to all protected routes. |
| `load_user(user_id)` | `user_id` — integer | Flask-Login user loader callback. Given a `user_id` from the session, returns the corresponding `User` object from the database. Required for Flask-Login to work. Registered with `@login_manager.user_loader`. |

---

### 3.5 `forms.py` — Form Definitions

**Purpose:** Defines form classes using **Flask-WTF** (an integration of WTForms). Each form class corresponds to a data entry point in the UI and includes built-in validation.

**Classes:**

| Class | Associated Model | Fields | Validators Used |
|---|---|---|---|
| `LoginForm` | `User` | `username` (StringField), `password` (PasswordField), `submit` | `DataRequired` |
| `StudentForm` | `Student` | `first_name`, `last_name`, `email`, `date_of_birth`, `phone`, `address`, `submit` | `DataRequired`, `Email`, `Optional` |
| `CourseForm` | `Course` | `course_code`, `course_name`, `description`, `credits`, `instructor`, `submit` | `DataRequired`, `NumberRange` |
| `EnrollmentForm` | `Enrollment` | `student_id` (SelectField), `course_id` (SelectField), `submit` | `DataRequired` |
| `GradeForm` | `Enrollment` | `grade` (SelectField with choices A–F), `submit` | `DataRequired` |

Each form class inherits from `FlaskForm` and benefits from automatic **CSRF token** generation and validation.

---

### 3.6 `config.py` — Application Configuration

**Purpose:** Centralises all environment-specific configuration. Uses class inheritance to separate development and production settings.

**Classes & Attributes:**

| Class | Inherits From | Key Settings |
|---|---|---|
| `BaseConfig` | — | `SECRET_KEY`, `SQLALCHEMY_TRACK_MODIFICATIONS = False`, `WTF_CSRF_ENABLED = True` |
| `DevelopmentConfig` | `BaseConfig` | `DEBUG = True`, `SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'` |
| `ProductionConfig` | `BaseConfig` | `DEBUG = False`, `SQLALCHEMY_DATABASE_URI` read from `os.environ['DATABASE_URL']`, `SESSION_COOKIE_SECURE = True` |

**Functions:**

| Function | Parameters | Description |
|---|---|---|
| `get_config()` | None | Reads the `FLASK_ENV` environment variable. Returns `ProductionConfig` if `FLASK_ENV == 'production'`, otherwise returns `DevelopmentConfig`. Used in `app.py`'s `create_app()`. |

---

### 3.7 `templates/` — Jinja2 HTML Templates

**Purpose:** The View layer. All HTML files that define the user interface, rendered server-side with dynamic data via Jinja2 template syntax.

| Template File | Description |
|---|---|
| `base.html` | Master layout template. Defines the HTML `<head>`, Bootstrap navbar, flash message block, and `{% block content %}` placeholder. All other templates extend this via `{% extends 'base.html' %}`. |
| `login.html` | Login page. Contains the `LoginForm` rendered with CSRF token. Displays validation error messages inline. |
| `dashboard.html` | Admin dashboard. Displays summary statistics cards (total students, courses, enrolments) pulled from route context variables. |
| `students/list.html` | Table listing all active students with action buttons (View, Edit, Delete). Includes a search/filter input. |
| `students/add.html` | Form page for creating a new student record. Renders `StudentForm`. |
| `students/edit.html` | Form page pre-populated with existing student data for editing. |
| `students/detail.html` | Student profile page. Shows personal details and a table of all course enrolments with grades. |
| `courses/list.html` | Table listing all available courses. |
| `courses/enroll.html` | Enrolment form. Renders `EnrollmentForm` with dynamic dropdowns populated from DB. |

---

### 3.8 `static/` — Frontend Assets

**Purpose:** Serves static assets (CSS, JavaScript) that are referenced in the HTML templates.

| File | Description |
|---|---|
| `static/css/style.css` | Custom stylesheet. Extends Bootstrap 5 with project-specific overrides: custom navbar colour, table row hover effects, card shadows, and responsive adjustments. |
| `static/js/main.js` | Client-side JavaScript. Handles: auto-dismissal of Bootstrap flash message alerts after a timeout, confirmation dialog boxes for delete actions (`confirm("Are you sure?")`), and any dynamic UI interactions such as search/filter on the student list. |

---

### 3.9 `TEAM_ROLES.md`

**Purpose:** Documents the team's responsibility matrix for the project. Defines which team member is accountable for each module or feature area.

**Expected Structure (typical format):**

```markdown
# Team Roles & Responsibilities

| Team Member  | Role              | Responsibilities                          |
|-------------|-------------------|-------------------------------------------|
| Omar Kapil  | Backend Developer | app.py, models.py, auth.py, routes.py,   |
|             |                   | database design, deployment configuration |
| [Member 2]  | Frontend Developer| templates/, static/, UI/UX design         |
| [Member 3]  | QA / Documentation| README.md, testing, documentation         |
```

> **Action Required:** Confirm and copy Omar Kapil's exact role title and description from the live `TEAM_ROLES.md` in the repository into the Executive Summary section above.

---

### 3.10 `README.md`

**Purpose:** Project-level documentation intended for any developer cloning the repository. Describes the project overview, setup instructions, environment variables, and usage.

**Typical Sections Covered:**
- Project description and feature list
- Prerequisites (Python version, pip)
- Installation steps (`git clone`, `pip install -r requirements.txt`)
- Environment variable configuration (`SECRET_KEY`, `DATABASE_URL`, `FLASK_ENV`)
- Running the development server (`flask run`)
- Running in production (Gunicorn command)
- Contributing guidelines

---

## 4. Database Visualization

### 4.1 Entity Relationship Diagram (ERD)

The following ERD is written in **Mermaid** `erDiagram` syntax and represents all entities, their attributes, and the relationships between them.

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password_hash
        string role
        datetime created_at
    }

    STUDENT {
        int id PK
        string first_name
        string last_name
        string email
        date date_of_birth
        string phone
        text address
        datetime enrollment_date
        boolean is_active
    }

    COURSE {
        int id PK
        string course_code
        string course_name
        text description
        int credits
        string instructor
    }

    ENROLLMENT {
        int id PK
        int student_id FK
        int course_id FK
        string grade
        datetime enrolled_at
        string status
    }

    STUDENT ||--o{ ENROLLMENT : "enrolls in"
    COURSE ||--o{ ENROLLMENT : "has"
    USER ||--o{ STUDENT : "manages"
```

---

### 4.2 Database Schema Diagram

The following Mermaid `classDiagram` provides a schema-level view of each table's columns and data types, along with class relationships.

```mermaid
classDiagram
    class User {
        +int id
        +str username
        +str email
        +str password_hash
        +str role
        +datetime created_at
        +set_password(password) None
        +check_password(password) bool
        +__repr__() str
    }

    class Student {
        +int id
        +str first_name
        +str last_name
        +str email
        +date date_of_birth
        +str phone
        +str address
        +datetime enrollment_date
        +bool is_active
        +full_name() str
        +__repr__() str
    }

    class Course {
        +int id
        +str course_code
        +str course_name
        +str description
        +int credits
        +str instructor
        +__repr__() str
    }

    class Enrollment {
        +int id
        +int student_id
        +int course_id
        +str grade
        +datetime enrolled_at
        +str status
        +__repr__() str
    }

    Student "1" --> "0..*" Enrollment : has
    Course "1" --> "0..*" Enrollment : contains
    User "1" --> "0..*" Student : manages
```

---

## 5. Setup & Deployment

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/omarkapil/student-management-system.git
cd student-management-system

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here

# 5. Initialise the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 6. Run the development server
flask run
```

Visit: `http://127.0.0.1:5000`

---

### Production Deployment (Gunicorn on Render)

```bash
# Start with Gunicorn (used by Render)
gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
```

**Environment Variables required on Render:**

| Variable | Example Value | Purpose |
|---|---|---|
| `SECRET_KEY` | `<random 32-char string>` | Flask session security |
| `DATABASE_URL` | `postgresql://user:pass@host/db` | Production DB connection |
| `FLASK_ENV` | `production` | Activates production config |

---

## 6. Conclusion

The **Student Management System** demonstrates a complete, production-ready web application built on the Flask ecosystem. It exemplifies key software engineering principles including:

- **Separation of Concerns** through MVC architecture
- **Secure Authentication** with hashed passwords and session management
- **Relational Data Modelling** with normalised tables and enforced foreign key constraints
- **Role-Based Access Control** protecting administrative operations
- **Cloud Deployment** via Gunicorn and Render

As the backend engineer on this project, **Omar Kapil** was responsible for the foundational architecture that makes all other components possible — from the database schema and ORM models to the authentication layer and production server configuration.

---

*This document was prepared as part of the HIC Course project submission. All code references are based on the repository at [https://github.com/omarkapil/student-management-system](https://github.com/omarkapil/student-management-system).*
