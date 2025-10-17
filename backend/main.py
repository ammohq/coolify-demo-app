from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
import json

app = FastAPI(title="Coolify Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "demo")
POSTGRES_USER = os.getenv("POSTGRES_USER", "demo")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "demo123")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        cursor_factory=RealDictCursor
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


try:
    init_db()
except Exception as e:
    print(f"DB init warning: {e}")


class Message(BaseModel):
    content: str


@app.get("/")
def root():
    return {
        "app": "Coolify Demo API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health():
    redis_status = "connected"
    postgres_status = "connected"

    try:
        redis_client.ping()
    except Exception as e:
        redis_status = f"error: {str(e)}"

    try:
        conn = get_db_connection()
        conn.close()
    except Exception as e:
        postgres_status = f"error: {str(e)}"

    return {
        "status": "healthy" if redis_status == "connected" and postgres_status == "connected" else "degraded",
        "redis": redis_status,
        "postgres": postgres_status,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/messages")
def create_message(message: Message):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages (content) VALUES (%s) RETURNING id, content, created_at",
        (message.content,)
    )
    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    redis_client.incr("message_count")
    redis_client.lpush("recent_messages", json.dumps({
        "id": result["id"],
        "content": result["content"],
        "created_at": result["created_at"].isoformat()
    }))
    redis_client.ltrim("recent_messages", 0, 9)

    return {
        "id": result["id"],
        "content": result["content"],
        "created_at": result["created_at"].isoformat()
    }


@app.get("/messages")
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, content, created_at FROM messages ORDER BY created_at DESC LIMIT 50")
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "messages": [
            {
                "id": msg["id"],
                "content": msg["content"],
                "created_at": msg["created_at"].isoformat()
            }
            for msg in messages
        ],
        "total": len(messages)
    }


@app.get("/stats")
def get_stats():
    message_count = redis_client.get("message_count") or "0"

    recent_messages = redis_client.lrange("recent_messages", 0, 9)
    recent = [json.loads(msg) for msg in recent_messages]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM messages")
    db_count = cur.fetchone()["count"]
    cur.close()
    conn.close()

    return {
        "redis_count": int(message_count),
        "postgres_count": db_count,
        "recent_messages": recent
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
