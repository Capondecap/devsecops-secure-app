import base64
import logging
import os
import pickle
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request
from prometheus_client import Counter, start_http_server


APP_HOST = "0.0.0.0"
APP_PORT = 5000
METRICS_PORT = 8000
DATABASE_PATH = Path(__file__).resolve().parent / "app.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

REQUEST_COUNTER = Counter(
    "app_http_requests_total",
    "Total HTTP requests handled by the Flask app.",
    ["method", "path"],
)


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                role TEXT NOT NULL
            )
            """
        )

        existing = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if existing == 0:
            connection.executemany(
                "INSERT INTO users (username, role) VALUES (?, ?)",
                [
                    ("alice", "admin"),
                    ("bob", "developer"),
                    ("carol", "analyst"),
                ],
            )
        connection.commit()
    finally:
        connection.close()


@app.before_request
def log_and_count_request():
    REQUEST_COUNTER.labels(method=request.method, path=request.path).inc()
    logger.info(
        "request method=%s path=%s remote_addr=%s",
        request.method,
        request.path,
        request.remote_addr,
    )


@app.get("/")
def index():
    return jsonify(
        {
            "app": "devsecops-secure-app",
            "status": "running",
            "message": "Flask application is running.",
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/ping")
def ping():
    target = request.args.get("target", "127.0.0.1")
    count_flag = "-n" if os.name == "nt" else "-c"
    output = os.popen(f"ping {count_flag} 1 {target}").read()
    return jsonify({"target": target, "output": output})


@app.post("/load")
def load():
    payload = request.get_json(silent=True) or {}
    data = payload.get("data", "")

    try:
        decoded = base64.b64decode(data)
        loaded = pickle.loads(decoded)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"loaded": str(loaded)})


@app.get("/users")
def users():
    username = request.args.get("username", "")
    query = (
        "SELECT id, username, role FROM users "
        + "WHERE username = '"
        + username
        + "'"
    )

    connection = get_db_connection()
    try:
        rows = connection.execute(query).fetchall()
    except sqlite3.Error as exc:
        connection.close()
        return jsonify({"error": str(exc), "query": query}), 400

    connection.close()

    return jsonify(
        {
            "query": query,
            "results": [dict(row) for row in rows],
        }
    )


def main():
    init_db()
    start_http_server(METRICS_PORT)
    logger.info("prometheus metrics listening on 0.0.0.0:%s", METRICS_PORT)
    logger.info("flask app listening on %s:%s", APP_HOST, APP_PORT)
    app.run(host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()
