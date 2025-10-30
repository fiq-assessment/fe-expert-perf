from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
import base64

app = FastAPI(title="Logs Mock API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate 10k mock logs
LEVELS = ["info", "warn", "error"]
SERVICES = ["api", "auth", "db", "cache", "worker", "scheduler"]
MESSAGES = [
    "Request processed successfully",
    "Database connection established",
    "Cache miss, fetching from database",
    "User authentication successful",
    "API rate limit warning",
    "Slow query detected",
    "Memory usage high",
    "Request timeout",
    "Invalid request payload",
    "Service health check passed"
]

LOGS = []
base_time = datetime.now() - timedelta(hours=24)

for i in range(10000):
    LOGS.append({
        "id": str(i + 1),
        "timestamp": (base_time + timedelta(seconds=i * 8.64)).isoformat(),
        "level": random.choice(LEVELS),
        "message": random.choice(MESSAGES),
        "service": random.choice(SERVICES),
        "trace_id": f"trace-{random.randint(1000, 9999)}",
        "duration_ms": random.randint(1, 500)
    })

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/logs")
async def list_logs(
    cursor: str | None = None,
    limit: int = 100,
    level: str | None = None
):
    """
    EXPECTATION:
    - Implement cursor-based pagination.
    - Filter by log level.
    - Return opaque cursor token for next page.
    - Efficient for large datasets (no OFFSET overhead).
    """
    filtered = LOGS.copy()
    
    if level:
        filtered = [log for log in filtered if log["level"] == level]
    
    # Decode cursor to get starting index
    start_idx = 0
    if cursor:
        try:
            start_idx = int(base64.b64decode(cursor).decode('utf-8'))
        except:
            raise HTTPException(400, "Invalid cursor")
    
    # Get page
    items = filtered[start_idx:start_idx + limit]
    
    # Generate next cursor if more items exist
    next_cursor = None
    if start_idx + limit < len(filtered):
        next_cursor = base64.b64encode(str(start_idx + limit).encode('utf-8')).decode('utf-8')
    
    return {
        "items": items,
        "nextCursor": next_cursor,
        "total": len(filtered)
    }

@app.get("/logs/{id}")
async def get_log_details(id: str):
    """
    EXPECTATION:
    - Return detailed log information.
    - Used for prefetch on hover.
    """
    log = next((l for l in LOGS if l["id"] == id), None)
    if not log:
        raise HTTPException(404, "Log not found")
    
    # Add extra details not in list view
    return {
        **log,
        "stack_trace": "  at handleRequest (server.js:42:15)\n  at processTicksAndRejections (internal/process/task_queues.js:93:5)",
        "user_id": f"user-{random.randint(1, 100)}",
        "request_id": f"req-{random.randint(10000, 99999)}",
        "metadata": {
            "ip": f"192.168.1.{random.randint(1, 255)}",
            "user_agent": "Mozilla/5.0..."
        }
    }

