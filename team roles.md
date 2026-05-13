**Student Management System**

*Helwan International Technological University \| HCI & Cybersecurity*

**Presentation & Code Division Plan**

# ①(Presentation Division) {#presentation-division}

Each team member covers a specific set of HCI principles with a defined speaking time. The order below is the recording order.

| **\#** | **Speaker**  | **Topics Covered**                      | **HCI Principles**     | **Time**     |
|--------|--------------|-----------------------------------------|------------------------|--------------|
| **1**  | **omar kapil Person 1** | Introduction + Visibility + Consistency | Principles 1 & 2       | **\~1:30**   |
| **2**  | **yousef ali Person 2** | Familiarity + Affordance                | Principles 3 & 4       | **\~1:30**   |
| **3**  | **mazin alaa Person 3** | Navigation + Control                    | Principles 5 & 6       | **\~1:40**   |
| **4**  | **shaban Person 4** | Feedback + Recovery + Constraints       | Principles 7, 8 & 9    | **\~2:00**   |
| **5**  | **elshaf3y Person 5** | Flexibility + Style + Conviviality      | Principles 10, 11 & 12 | **\~1:50**   |
| **6**  | **yousef abdelhady Person 6** | 8 Security Mechanisms + Conclusion      | Cybersecurity          | **\~2:30**   |
|        |              | **Total Video Length**                  |                        | **≈ 11 min** |

# ② (Code Division --- Screen Recording Guide) {#code-division-screen-recording-guide}

This table tells each person which files to open and screen-record while they are speaking. Show the code live --- do not use slides.

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 19%" />
<col style="width: 38%" />
<col style="width: 36%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>#</strong></th>
<th><strong>Speaker / Topics</strong></th>
<th><strong>Files to Show on Screen</strong></th>
<th><strong>What to Highlight</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>1</strong></td>
<td><p><strong>Person 1</strong></p>
<p>(Intro + Visibility +</p>
<p>Consistency)</p></td>
<td><p>app.py</p>
<p>templates/base.html</p>
<p>templates/dashboard.html</p>
<p>static/css/style.css</p></td>
<td>Show the Flask app startup, the base template with navbar, the dashboard with live stats, and the Bootstrap color scheme applied consistently.</td>
</tr>
<tr class="even">
<td><strong>2</strong></td>
<td><p><strong>Person 2</strong></p>
<p>(Familiarity +</p>
<p>Affordance)</p></td>
<td><p>templates/students/add_student.html</p>
<p>templates/students/edit_student.html</p>
<p>static/css/style.css</p></td>
<td>Show Font Awesome icons (pencil, trash, plus, magnifier), button styles (green Save, red Delete), input field design with placeholders, and the search bar.</td>
</tr>
<tr class="odd">
<td><strong>3</strong></td>
<td><p><strong>Person 3</strong></p>
<p>(Navigation +</p>
<p>Control)</p></td>
<td><p>templates/base.html</p>
<p>templates/students/students.html</p>
<p>templates/students/edit_student.html</p></td>
<td>Show the fixed navbar with active link highlighting, the students list with column headers and search bar, and the Cancel button on the edit form.</td>
</tr>
<tr class="even">
<td><strong>4</strong></td>
<td><p><strong>Person 4</strong></p>
<p>(Feedback +</p>
<p>Recovery +</p>
<p>Constraints)</p></td>
<td><p>routes/students.py</p>
<p>routes/auth.py</p>
<p>templates/students/students.html</p>
<p>templates/auth/register.html</p></td>
<td>Show flash message logic (green/red alerts), confirmation dialog before delete, form validation with highlighted invalid fields, and the dropdown year field constraint.</td>
</tr>
<tr class="odd">
<td><strong>5</strong></td>
<td><p><strong>Person 5</strong></p>
<p>(Flexibility +</p>
<p>Style +</p>
<p>Conviviality)</p></td>
<td><p>routes/students.py (search/export)</p>
<p>templates/dashboard.html</p>
<p>templates/students/students.html</p>
<p>static/css/style.css</p></td>
<td>Show multi-field search logic, the Export CSV/Excel route, responsive Bootstrap layout, personalized greeting on dashboard, and friendly error messages.</td>
</tr>
<tr class="even">
<td><strong>6</strong></td>
<td><p><strong>Person 6</strong></p>
<p>(Security</p>
<p>Mechanisms +</p>
<p>Conclusion)</p></td>
<td><p>app.py (bcrypt + CSRF + secret key)</p>
<p>models/__init__.py (failed_logins, locked_until)</p>
<p>routes/auth.py (brute-force lock logic)</p>
<p>routes/students.py (SQLAlchemy queries)</p>
<p>.env.example</p></td>
<td>Show bcrypt hashing in models, brute-force counter &amp; lockout in auth.py, CSRF setup in app.py, parameterized ORM queries, and the .env.example for secure key management.</td>
</tr>
</tbody>
</table>

# ③ (Detailed Speaker Notes) {#detailed-speaker-notes}

## omar kapil Person 1 --- Intro + Visibility + Consistency (\~1:30 \| Principles 1 & 2) {#person-1-intro-visibility-consistency-130-principles-1-2}

- Open: show the GitHub repo URL + project name on screen

- Dashboard: live stats (total students, recent activity)

- Show the real-time password strength indicator on register page

- Flash messages --- point to green/red alerts in the HTML

- Navbar: highlight the active page indicator

- Bootstrap classes: same navbar, same color scheme across all pages

## yousef ali Person 2 --- Familiarity + Affordance (\~1:30 \| Principles 3 & 4) {#person-2-familiarity-affordance-130-principles-3-4}

- Font Awesome icons: magnifier (search), pencil (edit), trash (delete), plus (add)

- Forms: familiar labels --- Email, Password, Student Code

- Green Save button vs. Red Delete button --- explain color semantics

- Input field borders + placeholder text

- Search bar: wide field + icon + button = recognizable pattern

## mazin alaa Person 3 --- Navigation + Control (\~1:40 \| Principles 5 & 6) {#person-3-navigation-control-140-principles-5-6}

- Fixed top navbar: Dashboard, Students, Add Student, Logout

- Active link highlighted in navbar (show base.html code)

- Students list: search bar at top, labeled column headers

- Logo click → back to dashboard (no dead ends)

- Delete: confirmation dialog --- user can cancel

- Edit page: Cancel button beside Save --- show both on screen

- No auto-submit, no forced workflows

## shaban Person 4 --- Feedback + Recovery + Constraints (\~2:00 \| Principles 7, 8 & 9) {#person-4-feedback-recovery-constraints-200-principles-7-8-9}

- Flash message: green \'Student added successfully\' --- show the code in routes/students.py

- Login fail: red \'Invalid email or password\' --- show routes/auth.py

- Field-level validation: red borders on bad input

- Recovery: confirmation before delete --- show JS dialog in template

- Recovery: form keeps data after error, highlights only bad fields

- Password reset link on login page

- Constraints: email format validation, student code max length

- Year dropdown: cannot type invalid values

- Required fields: form won\'t submit until satisfied

## elshaf3y Person 5 --- Flexibility + Style + Conviviality (\~1:50 \| Principles 10, 11 & 12) {#person-5-flexibility-style-conviviality-150-principles-10-11-12}

- Search: filter by Name, Student Code, Course, or Year --- show routes/students.py

- Keyboard navigation: Tab key through forms

- Export CSV/Excel: show the export route in routes/students.py

- Bootstrap 5: soft blues, whites, accent greens --- show static/css/style.css

- Responsive layout: show on desktop and mobile widths

- Dashboard greeting: \'Welcome, \[username\]\' --- show templates/dashboard.html

- Friendly error messages: \'Please enter a valid email\' not \'ERROR 400\'

- Helper text under input fields

## yousef abdelhady Person 6 --- 8 Security Mechanisms + Conclusion (\~2:30 \| Cybersecurity) {#person-6-8-security-mechanisms-conclusion-230-cybersecurity}

- 1\. Password Hashing: show bcrypt/scrypt in models/\_\_init\_\_.py

- 2\. Brute-Force: show failed_logins counter + locked_until in models, lockout logic in routes/auth.py

- 3\. CSRF Protection: show CSRFProtect(app) in app.py and {% csrf_token %} in templates

- 4\. Input Validation: HTML5 + Python validation side-by-side

- 5\. SQL Injection: show SQLAlchemy ORM queries in routes/students.py (parameterized, not raw SQL)

- 6\. Secure Secret Key: show SECRET_KEY from env in app.py + .env.example

- 7\. Debug Mode OFF: show app.run(debug=False) or env-controlled

- 8\. (Bonus) XSS: show Jinja2 auto-escaping in templates

- Closing: all team members on camera, say University name

# ④ Recording Tips {#recording-tips}

- Speak at \~130 words per minute --- slightly slower than conversation.

- Show the live running app on http://127.0.0.1:5000 while speaking.

- Open VS Code side-by-side with the browser for code + UI simultaneously.

- Each speaker ends with the handoff line already in the script.

- Person 6: have the relevant file tabs open in VS Code before you start.

- Closing shot: all 6 team members on camera for the \'Thank you.\'
