# Spec: 03 — Login and Logout

## Goal

Wire up `POST /login` so users can authenticate with email + password, start a Flask session, and be redirected to `/profile`. Wire up `GET /logout` to clear the session and redirect to `/`. Update the nav in `base.html` to show context-aware links depending on whether a session is active.

---

## Login form inputs (login.html — already exists, no changes needed)

| Field name | Notes |
|------------|-------|
| `email`    | Looked up in `users` table |
| `password` | Checked against `password_hash` with `check_password_hash` |

---

## Validation rules for POST /login

| Rule | Error message |
|------|---------------|
| Both fields non-empty | `"Email and password are required."` |
| Email exists in DB | `"Invalid email or password."` |
| Password matches hash | `"Invalid email or password."` |

Use the same error message for "no such user" and "wrong password" — this prevents user-enumeration.

---

## Session fields

After a successful login, store these two keys in `session`:

| Key | Value |
|-----|-------|
| `user_id` | `users.id` (integer) |
| `username` | `users.username` (string) |

---

## Files to change

### `app.py`

1. Extend the imports:
   ```python
   from flask import Flask, render_template, request, redirect, url_for, session
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. Set a secret key immediately after `app = Flask(__name__)`:
   ```python
   app.secret_key = "dev-secret-key"
   ```

3. Replace the existing `login` route (currently GET-only) with a GET+POST handler:
   ```python
   @app.route("/login", methods=["GET", "POST"])
   def login():
       if request.method == "GET":
           return render_template("login.html")

       email    = request.form.get("email", "").strip()
       password = request.form.get("password", "")

       if not email or not password:
           return render_template("login.html", error="Email and password are required.")

       db   = get_db()
       user = db.execute(
           "SELECT id, username, password_hash FROM users WHERE email = ?", (email,)
       ).fetchone()
       db.close()

       if user is None or not check_password_hash(user["password_hash"], password):
           return render_template("login.html", error="Invalid email or password.")

       session["user_id"]  = user["id"]
       session["username"] = user["username"]
       return redirect(url_for("profile"))
   ```

4. Replace the existing `logout` stub:
   ```python
   @app.route("/logout")
   def logout():
       session.clear()
       return redirect(url_for("landing"))
   ```

### `templates/base.html`

Replace the static `<div class="nav-links">` block with a session-aware version:

```html
<div class="nav-links">
    {% if session.user_id %}
        <span class="nav-username">{{ session.username }}</span>
        <a href="{{ url_for('logout') }}">Sign out</a>
    {% else %}
        <a href="{{ url_for('login') }}">Sign in</a>
        <a href="{{ url_for('register') }}" class="nav-cta">Get started</a>
    {% endif %}
</div>
```

No other files need to change.

---

## What is NOT in scope

- `get_db()` returning `Row` objects — already configured in `database/db.py`
- Protecting routes with a login-required decorator (covered in Step 4)
- Password reset or "remember me"
- Changing `secret_key` to an environment variable (acceptable for dev; production hardening is out of scope)

---

## Verification

```bash
# 1. Start the server
python app.py

# 2. Register a test account at http://localhost:5001/register
#    (or use an existing one from a previous seed)

# 3. Visit http://localhost:5001/login
#    Submit correct credentials → redirects to /profile, nav shows username + "Sign out"

# 4. Submit wrong password → inline error "Invalid email or password."

# 5. Submit a non-existent email → same inline error (no user enumeration)

# 6. Click "Sign out" → session cleared, nav reverts to "Sign in" / "Get started"

# 7. Confirm session is gone: visiting /login after logout shows the form, not a redirect
```
