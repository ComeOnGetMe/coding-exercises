"""
main.py according to DESIGN.md structure

This is the application entry point that:
- Initializes FastAPI app
- Sets up configuration
- Registers middleware
- Registers routes
- Handles graceful shutdown
"""

import signal
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.api.routes import router
from src.api.middleware import (
    RequestIDMiddleware,
    StructuredLoggingMiddleware,
    MetricsMiddleware,  # Optional
)
from src.utils import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown logic.
    Handles graceful shutdown and resource cleanup.
    """
    # Startup
    setup_logging()
    logger = setup_logging()
    logger.info("Starting KV Store Service", extra={"port": settings.PORT})
    
    # Initialize storage connection
    # await kv_store.initialize()
    
    yield
    
    # Shutdown
    logger.info("Shutting down KV Store Service")
    # await kv_store.close()


# Create FastAPI app with lifespan
app = FastAPI(
    title="S3-Backed KV Store Service",
    description="Key-value store service backed by S3/MinIO",
    version="1.0.0",
    lifespan=lifespan,
)

# Register middleware (order matters!)
# They execute: RequestID → Logging → Metrics → Handler → Metrics → Logging → RequestID
app.add_middleware(RequestIDMiddleware)
app.add_middleware(StructuredLoggingMiddleware)

# Optional: Add metrics middleware if Prometheus is enabled
if settings.ENABLE_METRICS:
    app.add_middleware(MetricsMiddleware)

# Register API routes
app.include_router(router, prefix="/kv", tags=["key-value"])


# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint for container orchestration"""
    return {"status": "ok"}


# Optional: Metrics endpoint (if Prometheus is enabled)
if settings.ENABLE_METRICS:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )


# Graceful shutdown handler (optional feature)
def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    logger = setup_logging()
    logger.info("Received shutdown signal, shutting down gracefully...")
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
    )

