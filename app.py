import os
import psycopg2
from flask import Flask, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ.get("DB_PORT", "5432")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )


@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE visits SET count = count + 1 WHERE id = 1 RETURNING count;")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    user = session.get("username")
    auth_links = (
        f'Logged in as <strong>{user}</strong> | '
        f'<a href="/dashboard">Dashboard</a> | <a href="/logout">Log out</a>'
        if user else
        '<a href="/register">Register</a> | <a href="/login">Log in</a>'
    )

    return f"""
    <html>
    <head><title>Capstone — Live Web App</title></head>
    <body style="font-family: sans-serif; text-align:center; margin-top:80px;">
        <h1>Cloud &amp; DevOps Capstone</h1>
        <p>This page has been visited <strong>{count}</strong> times.</p>
        <p>{auth_links}</p>
    </body>
    </html>
    """


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password_hash = generate_password_hash(request.form["password"])

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash),
            )
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return "Username already taken", 400
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("login"))

    return """
    <form method="post" style="font-family: sans-serif; text-align:center; margin-top:80px;">
        <h2>Register</h2>
        <input name="username" placeholder="username" required><br><br>
        <input name="password" type="password" placeholder="password" required><br><br>
        <button type="submit">Register</button>
    </form>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row and check_password_hash(row[0], request.form["password"]):
            session["username"] = username
            return redirect(url_for("home"))

        return "Invalid credentials", 401

    return """
    <form method="post" style="font-family: sans-serif; text-align:center; margin-top:80px;">
        <h2>Log in</h2>
        <input name="username" placeholder="username" required><br><br>
        <input name="password" type="password" placeholder="password" required><br><br>
        <button type="submit">Log in</button>
    </form>
    """


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return f"""
    <div style="font-family: sans-serif; text-align:center; margin-top:80px;">
        <h1>Welcome, {session['username']}</h1>
        <p>This is a protected route — only reachable when logged in.</p>
        <a href="/">Home</a>
    </div>
    """


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
