import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

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

    return f"""
    <html>
    <head><title>Module 3 — Live Web App</title></head>
    <body style="font-family: sans-serif; text-align:center; margin-top:100px;">
        <h1>Module 3 — Live Web App</h1>
        <p>This page has been visited <strong>{count}</strong> times.</p>
        <p>Deployed on AWS EC2, backed by an RDS PostgreSQL database.</p>
    </body>
    </html>
    """


@app.route("/health")
def health():
    """Simple health check endpoint — useful for monitoring."""
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
