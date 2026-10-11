
import os
import time
import uuid
from statistics import mean

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

EMAIL = os.getenv("EMAIL", "22f3001026@ds.study.iitm.ac.in")
ALLOWED_ORIGIN = "https://dash-58k0n2.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_headers(request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    elapsed = time.perf_counter() - start
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{max(0.0, elapsed):.6f}"
    return response



@app.get("/stats")
def stats(values: str = Query(...)):
    try:
        parts = values.split(",")
        if not parts or any(not p.strip() for p in parts):
            raise ValueError
        numbers = [int(p.strip()) for p in parts]
    except ValueError:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=400,
            content={"detail": "values must be comma-separated integers"},
        )

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": round(mean(numbers), 6),
    }


@app.get("/")
def root():
    return {"status": "ok"}
