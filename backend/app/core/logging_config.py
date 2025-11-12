"""
Structured Logging Configuration
Production-grade logging with JSON formatting, correlation IDs, and log aggregation support
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
import uuid
from contextvars import ContextVar

from .config import settings

# Context variable for request correlation ID
request_id_var: ContextVar[str] = ContextVar('request_id', default='')


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add correlation ID if available
        request_id = request_id_var.get()
        if request_id:
            log_data['request_id'] = request_id

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)

        # Add user info if available
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        # Add request info if available
        if hasattr(record, 'method'):
            log_data['http_method'] = record.method
        if hasattr(record, 'path'):
            log_data['http_path'] = record.path
        if hasattr(record, 'status_code'):
            log_data['http_status'] = record.status_code

        return json.dumps(log_data)


def setup_logging():
    """
    Configure application logging

    - JSON format for production
    - Human-readable format for development
    - Proper log levels
    - Integration with Sentry
    """
    # Determine log level
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Use JSON formatter in production, human-readable in development
    if settings.ENVIRONMENT == 'production':
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Suppress noisy loggers
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(
        'Logging configured',
        extra={
            'extra_fields': {
                'environment': settings.ENVIRONMENT,
                'log_level': logging.getLevelName(log_level),
                'app_version': settings.APP_VERSION
            }
        }
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get logger with given name

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def set_request_id(request_id: str = None):
    """
    Set request ID for current context

    Args:
        request_id: Request correlation ID (auto-generated if not provided)
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    return request_id


def get_request_id() -> str:
    """Get current request ID"""
    return request_id_var.get()


def log_api_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: str = None,
    error: str = None
):
    """
    Log API request with structured data

    Args:
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration_ms: Request duration in milliseconds
        user_id: User ID if authenticated
        error: Error message if request failed
    """
    logger = get_logger('api')

    log_data = {
        'method': method,
        'path': path,
        'status_code': status_code,
        'duration_ms': duration_ms,
    }

    if user_id:
        log_data['user_id'] = user_id
    if error:
        log_data['error'] = error

    level = logging.ERROR if status_code >= 500 else (
        logging.WARNING if status_code >= 400 else logging.INFO
    )

    logger.log(
        level,
        f'{method} {path} {status_code} {duration_ms:.2f}ms',
        extra={'extra_fields': log_data}
    )
