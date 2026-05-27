# Spec: 02 — User Registration

## Goal

Wire up the `POST /register` handler so users can create accounts. On success redirect to `/login`; on failure re-render `register.html` with an inline error message.

---

## Form inputs (register.html)

| Field name | DB column      | Notes                         |
|------------|----------------|-------------------------------|
| `name`     | `username`     | Stored as-is (no normalisation) |
| `email`    | `email`        |                               |
| `password` | `password_hash`| Must be hashed before storage |

---

## Validation rules

| Rule | Error message |
|------|---------------|
| All three fields non-empty | `"All fields are required."` |
| `password` ≥ 8 characters | `"Password must be at least 8 characters."` |
| Email / username not already taken | `"An account with that email or username already exists."` |

Client-side `required` attributes are already on the inputs; server-side validation is still mandatory.

---

## Files to change

### `app.py`

1. Extend the imports at the top:
   ```python
   from flask import Flask, render_template, request, redirect, url_for
   import sqlite3
   from werkzeug.security import generate_password_hash
   from database.db import init_db, get_db
   ```

2. Replace the existing `register` route with a GET+POST handler:
   ```python
   @app.route("/register", methods=["GET", "POST"])
   def register():
       if request.method == "GET":
           return render_template("register.html")

       name     = request.form.get("name", "").strip()
       email    = request.form.get("email", "").strip()
       password = request.form.get("password", "")

       if not name or not email or not password:
           return render_template("register.html", error="All fields are required.")

       if len(password) < 8:
           return render_template("register.html",
                                  error="Password must be at least 8 characters.")

       password_hash = generate_password_hash(password)

       try:
           db = get_db()
           db.execute(
               "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
               (name, email, password_hash),
           )
           db.commit()
           db.close()
       except sqlite3.IntegrityError:
           return render_template("register.html",
                                  error="An account with that email or username already exists.")

       return redirect(url_for("login"))
   ```

No other files need to change. `register.html` already contains the `{% if error %}` block; no template edits required.

---

## What is NOT in scope

- Session / login after registration (covered in Step 3)
- Email verification
- Username format constraints beyond non-empty

---

## Verification

```bash
# 1. Start server — should print no errors
python app.py

# 2. Open http://localhost:5001/register in a browser
#    Fill in the form with valid data → should redirect to /login

# 3. Submit the same email again → inline error appears

# 4. Submit with a 5-character password → inline error appears

# 5. Confirm the user row was created
python -c "
import sqlite3
c = sqlite3.connect('expense_tracker.db')
print(list(c.execute('SELECT id, username, email FROM users')))
c.close()
"
```
