from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Adds a unique request ID to each request"""
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Structured logging middleware"""
    async def dispatch(self, request: Request, call_next):
        # Simple implementation - can be enhanced with proper logging
        response = await call_next(request)
        return response


class MetricsMiddleware(BaseHTTPMiddleware):
    """Metrics middleware for Prometheus"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
