
import json
import os
import time

import psycopg2
import redis
from flask import Flask, jsonify, render_template, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "taskmanager"),
    "user": os.getenv("DB_USER", "taskuser"),
    "password": os.getenv("DB_PASSWORD", "change_this_password"),
}

CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "30"))

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "cache"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)

def get_db_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

def initialize_database():
    """Retry briefly while PostgreSQL starts, then create the table."""
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "db", "schema.sql"
    )

    with open(schema_path, encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    for attempt in range(15):
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(schema_sql)
            return
        except psycopg2.OperationalError:
            if attempt == 14:
                raise
            time.sleep(2)

def invalidate_task_cache():
    try:
        cache.delete("tasks:all")
    except redis.RedisError:
        app.logger.warning("Redis unavailable; cache was not cleared.")

def get_all_tasks():
    try:
        cached_tasks = cache.get("tasks:all")
        if cached_tasks:
            return json.loads(cached_tasks)
    except redis.RedisError:
        app.logger.warning("Redis unavailable; reading from PostgreSQL.")

    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM tasks
                ORDER BY id DESC
                """
            )
            tasks = [dict(row) for row in cursor.fetchall()]

    for task in tasks:
        task["created_at"] = task["created_at"].isoformat()

    try:
        cache.setex("tasks:all", CACHE_TTL, json.dumps(tasks))
    except redis.RedisError:
        app.logger.warning("Could not cache tasks in Redis.")

    return tasks

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

        cache.ping()

        return jsonify({
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
        }), 200
    except (psycopg2.Error, redis.RedisError) as error:
        app.logger.warning("Health check failed: %s", error)
        return jsonify({"status": "unhealthy"}), 503

@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    try:
        return jsonify(get_all_tasks()), 200
    except psycopg2.Error:
        app.logger.exception("Could not retrieve tasks")
        return jsonify({"error": "Database operation failed"}), 500

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    if len(title) > 200:
        return jsonify({"error": "Title must be 200 characters or fewer"}), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, description)
                    VALUES (%s, %s)
                    RETURNING id, title, description, completed, created_at
                    """,
                    (title, description),
                )
                task = dict(cursor.fetchone())

        task["created_at"] = task["created_at"].isoformat()
        invalidate_task_cache()
        return jsonify(task), 201
    except psycopg2.Error:
        app.logger.exception("Could not create task")
        return jsonify({"error": "Database operation failed"}), 500

@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    if "completed" not in data or not isinstance(data["completed"], bool):
        return jsonify({"error": "completed must be true or false"}), 400

    try:
        with get_db_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET completed = %s
                    WHERE id = %s
                    RETURNING id, title, description, completed, created_at
                    """,
                    (data["completed"], task_id),
                )
                task = cursor.fetchone()

                if task is None:
                    return jsonify({"error": "Task not found"}), 404

                task = dict(task)

        task["created_at"] = task["created_at"].isoformat()
        invalidate_task_cache()
        return jsonify(task), 200
    except psycopg2.Error:
        app.logger.exception("Could not update task")
        return jsonify({"error": "Database operation failed"}), 500

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM tasks WHERE id = %s RETURNING id",
                    (task_id,),
                )
                deleted = cursor.fetchone()

        if deleted is None:
            return jsonify({"error": "Task not found"}), 404

        invalidate_task_cache()
        return jsonify({"message": "Task deleted"}), 200
    except psycopg2.Error:
        app.logger.exception("Could not delete task")
        return jsonify({"error": "Database operation failed"}), 500

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)
