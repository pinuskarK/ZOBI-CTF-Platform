import os
import sqlite3
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
# Secrets must be supplied by the local environment; never commit real values.
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY must be set in the environment")

DB_PATH = os.environ.get("C3_DB_PATH", "/app/data/research.db")
FLAG = os.environ.get("C3_FLAG")
if not FLAG:
    raise RuntimeError("C3_FLAG must be set in the environment")

LOGIN_PAGE = """
<!doctype html>
<html>
<head>
    <title>The Abandoned Lab</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #101820; color: #eee;
               max-width: 700px; margin: 60px auto; padding: 20px; }
        .panel { background: #1d2b36; padding: 24px; border-radius: 8px; }
        input, button { display: block; width: 100%; box-sizing: border-box;
                        margin: 12px 0; padding: 12px; }
        button { background: #4caf50; border: 0; cursor: pointer; }
        .error { color: #ff8585; }
    </style>
</head>
<body>
    <div class="panel">
        <h1>The Abandoned Lab</h1>
        <p>Research Portal — Restricted Access</p>
        <p>Several research records remain archived after the lab was abandoned.</p>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="post">
            <label>Researcher username</label>
            <input name="username" required>
            <label>Password</label>
            <input name="password" type="password" required>
            <button type="submit">Sign in</button>
        </form>
        <p><small>Hint: Investigate how the portal checks login credentials.</small></p>
    </div>
</body>
</html>
"""

ARCHIVE_PAGE = """
<!doctype html>
<html>
<head><title>Research Archive</title></head>
<body style="font-family:Arial;background:#101820;color:#eee;max-width:750px;margin:50px auto;padding:20px">
    <h1>Research Archive</h1>
    <p>Access granted. Archived records recovered.</p>
    <h2>Recovered note</h2>
    <p>The remaining evidence was transferred to Dr. Alex's computer in the observation room.</p>
    <h2>Stage 3 Flag</h2>
    <p id="flag">{{ flag }}</p>
    <p>Record this flag in the CTF platform to complete this stage.</p>
    <a href="{{ url_for('logout') }}" style="color:#8fdaff">Log out</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # INTENTIONAL SQL INJECTION VULNERABILITY:
        # This unsafe query is part of the isolated CTF exercise only.
        query = (
            "SELECT username FROM users "
            f"WHERE username = '{username}' AND password = '{password}'"
        )
        try:
            with sqlite3.connect(DB_PATH) as connection:
                user = connection.execute(query).fetchone()
            if user:
                session["researcher"] = user[0]
                return redirect(url_for("archive"))
        except sqlite3.Error:
            # Avoid exposing database internals in participant-facing responses.
            pass
        error = "Access denied. Check your credentials and try again."
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/archive")
def archive():
    if "researcher" not in session:
        return redirect(url_for("login"))
    return render_template_string(ARCHIVE_PAGE, flag=FLAG)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/health")
def health():
    return {"service": "The Abandoned Lab", "status": "running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
