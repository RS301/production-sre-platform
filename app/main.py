import os
import time

from fastapi import FastAPI, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

APP_NAME = os.getenv("APP_NAME", "psre-api")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

REQUEST_ERRORS = Counter(
    "http_request_errors_total",
    "Total number of HTTP errors",
    ["method", "path", "status"],
)
app = FastAPI(
    title="Production SRE Platform API",
    version=APP_VERSION,
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path,
        status=str(response.status_code),
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        path=request.url.path,
    ).observe(duration)

    if response.status_code >= 500:
        REQUEST_ERRORS.labels(
            method=request.method,
            path=request.url.path,
            status=str(response.status_code),
        ).inc()
    return response


@app.get("/api/v1/error")
async def error():
    return Response(
        content='{"status":"error"}',
        media_type="application/json",
        status_code=500,
    )

@app.get("/")
async def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "application": APP_NAME,
        "version": APP_VERSION,
    }


@app.get("/ready")
async def ready():
    return {
        "status": "ready",
        "application": APP_NAME,
    }


@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/api/v1/info")
async def info():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
    }


@app.get("/api/v1/work")
async def work():
    start = time.perf_counter()

    time.sleep(0.01)

    duration = time.perf_counter() - start

    return {
        "status": "completed",
        "duration_ms": round(duration * 1000, 2),
    }
