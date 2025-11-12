"""
Middleware for Production-Ready FastAPI Application
Includes: error handling, logging, security headers, CORS, request ID
"""

import time
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
import logging

from .logging_config import set_request_id, get_request_id, log_api_request
from .config import settings

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or extract request ID
        request_id = request.headers.get('X-Request-ID') or set_request_id()

        # Add to request state
        request.state.request_id = request_id

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers['X-Request-ID'] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all API requests with timing"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Get user ID if authenticated
        user_id = None
        if hasattr(request.state, 'user'):
            user_id = request.state.user.id

        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000

            # Log request
            log_api_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                user_id=user_id
            )

            # Add timing header
            response.headers['X-Response-Time'] = f'{duration_ms:.2f}ms'

            return response

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            # Log error
            log_api_request(
                method=request.method,
                path=request.url.path,
                status_code=500,
                duration_ms=duration_ms,
                user_id=user_id,
                error=str(e)
            )

            logger.exception(f'Request failed: {request.method} {request.url.path}')
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Security headers
        security_headers = {
            # Prevent clickjacking
            'X-Frame-Options': 'DENY',

            # Prevent MIME type sniffing
            'X-Content-Type-Options': 'nosniff',

            # Enable XSS filter
            'X-XSS-Protection': '1; mode=block',

            # Referrer policy
            'Referrer-Policy': 'strict-origin-when-cross-origin',

            # Permissions policy
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }

        # HSTS (only in production with HTTPS)
        if settings.ENVIRONMENT == 'production':
            security_headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Content Security Policy (CSP)
        if settings.ENVIRONMENT == 'production':
            csp = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net",
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
                "font-src 'self' https://fonts.gstatic.com",
                "img-src 'self' data: https: blob:",
                "connect-src 'self' https://api.openai.com https://*.elevenlabs.io",
                "media-src 'self' blob:",
                "frame-ancestors 'none'",
            ]
            security_headers['Content-Security-Policy'] = '; '.join(csp)

        # Add headers to response
        for header, value in security_headers.items():
            response.headers[header] = value

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)

        except Exception as e:
            # Log the error
            logger.exception(f'Unhandled exception: {str(e)}')

            # Return appropriate error response
            if settings.DEBUG:
                error_detail = {
                    'error': str(e),
                    'type': type(e).__name__,
                    'request_id': get_request_id()
                }
            else:
                error_detail = {
                    'error': 'Internal server error',
                    'request_id': get_request_id()
                }

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=error_detail
            )


def setup_middleware(app):
    """
    Configure all middleware for the application

    Args:
        app: FastAPI application instance
    """
    # 1. Request ID (first, so all other middleware can use it)
    app.add_middleware(RequestIDMiddleware)

    # 2. Error handling (early, to catch all errors)
    app.add_middleware(ErrorHandlingMiddleware)

    # 3. Logging (to log all requests)
    app.add_middleware(LoggingMiddleware)

    # 4. Security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # 5. CORS (already configured in main.py, but ensure it's here)
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=['X-Request-ID', 'X-Response-Time']
        )

    logger.info('Middleware configured successfully')
