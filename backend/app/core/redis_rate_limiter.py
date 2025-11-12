"""
Redis-based Distributed Rate Limiter
Production-ready rate limiting that scales across multiple instances
"""

import redis
from typing import Optional
from datetime import datetime, timedelta
import logging

from .config import settings

logger = logging.getLogger(__name__)


class RedisRateLimiter:
    """
    Distributed rate limiter using Redis

    Supports:
    - Fixed window rate limiting
    - Sliding window rate limiting
    - Multiple rate limit rules per user
    - Scales across multiple instances
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize Redis connection

        Args:
            redis_url: Redis connection URL (defaults to settings.REDIS_URL)
        """
        self.redis_url = redis_url or settings.REDIS_URL
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Redis rate limiter connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None

    def is_allowed(
        self,
        key: str,
        limit: int,
        window: int,
        method: str = "fixed"
    ) -> bool:
        """
        Check if request is allowed under rate limit

        Args:
            key: Unique identifier (e.g., user_id, ip_address)
            limit: Maximum requests allowed
            window: Time window in seconds
            method: "fixed" or "sliding" window

        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        if not self.redis_client:
            # Fallback: allow request if Redis unavailable
            logger.warning("Redis unavailable, allowing request")
            return True

        try:
            if method == "sliding":
                return self._sliding_window(key, limit, window)
            else:
                return self._fixed_window(key, limit, window)
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # Fail open: allow request on error
            return True

    def _fixed_window(self, key: str, limit: int, window: int) -> bool:
        """
        Fixed window rate limiting

        Uses a simple counter that resets at fixed intervals
        """
        rate_key = f"rate_limit:fixed:{key}:{window}"

        try:
            # Increment counter
            current = self.redis_client.incr(rate_key)

            # Set expiration on first request
            if current == 1:
                self.redis_client.expire(rate_key, window)

            # Check if under limit
            return current <= limit

        except Exception as e:
            logger.error(f"Fixed window rate limit failed: {e}")
            return True

    def _sliding_window(self, key: str, limit: int, window: int) -> bool:
        """
        Sliding window rate limiting

        More accurate than fixed window, prevents burst at window boundaries
        Uses sorted sets to track request timestamps
        """
        rate_key = f"rate_limit:sliding:{key}"
        now = datetime.utcnow().timestamp()
        window_start = now - window

        try:
            pipe = self.redis_client.pipeline()

            # Remove old entries outside the window
            pipe.zremrangebyscore(rate_key, 0, window_start)

            # Count requests in current window
            pipe.zcard(rate_key)

            # Add current request with timestamp as score
            pipe.zadd(rate_key, {str(now): now})

            # Set expiration
            pipe.expire(rate_key, window)

            # Execute pipeline
            results = pipe.execute()

            # Check count (result from zcard)
            current_count = results[1]

            return current_count < limit

        except Exception as e:
            logger.error(f"Sliding window rate limit failed: {e}")
            return True

    def get_remaining(self, key: str, limit: int, window: int) -> int:
        """
        Get remaining requests in current window

        Args:
            key: Unique identifier
            limit: Maximum requests allowed
            window: Time window in seconds

        Returns:
            Number of remaining requests
        """
        if not self.redis_client:
            return limit

        try:
            rate_key = f"rate_limit:fixed:{key}:{window}"
            current = self.redis_client.get(rate_key)

            if current is None:
                return limit

            remaining = limit - int(current)
            return max(0, remaining)

        except Exception as e:
            logger.error(f"Get remaining failed: {e}")
            return limit

    def reset(self, key: str, window: int):
        """
        Reset rate limit for a specific key

        Args:
            key: Unique identifier
            window: Time window in seconds
        """
        if not self.redis_client:
            return

        try:
            rate_key_fixed = f"rate_limit:fixed:{key}:{window}"
            rate_key_sliding = f"rate_limit:sliding:{key}"

            self.redis_client.delete(rate_key_fixed, rate_key_sliding)
            logger.info(f"Rate limit reset for key: {key}")

        except Exception as e:
            logger.error(f"Rate limit reset failed: {e}")

    def get_status(self, key: str, limit: int, window: int) -> dict:
        """
        Get current rate limit status

        Args:
            key: Unique identifier
            limit: Maximum requests allowed
            window: Time window in seconds

        Returns:
            Dict with status information
        """
        if not self.redis_client:
            return {
                "limit": limit,
                "remaining": limit,
                "reset_at": None,
                "window": window
            }

        try:
            rate_key = f"rate_limit:fixed:{key}:{window}"
            current = self.redis_client.get(rate_key)
            ttl = self.redis_client.ttl(rate_key)

            if current is None:
                current = 0
            else:
                current = int(current)

            remaining = max(0, limit - current)
            reset_at = (
                datetime.utcnow() + timedelta(seconds=ttl)
                if ttl > 0
                else None
            )

            return {
                "limit": limit,
                "remaining": remaining,
                "reset_at": reset_at.isoformat() if reset_at else None,
                "window": window,
                "current": current
            }

        except Exception as e:
            logger.error(f"Get status failed: {e}")
            return {
                "limit": limit,
                "remaining": limit,
                "reset_at": None,
                "window": window,
                "error": str(e)
            }

    def check_multiple_limits(
        self,
        key: str,
        limits: list[tuple[int, int]]
    ) -> bool:
        """
        Check multiple rate limit rules

        Useful for tiered rate limiting (e.g., 10/min, 100/hour, 1000/day)

        Args:
            key: Unique identifier
            limits: List of (limit, window) tuples

        Returns:
            True if all limits allow the request
        """
        for limit, window in limits:
            if not self.is_allowed(key, limit, window):
                return False

        return True


# Global rate limiter instance
rate_limiter = RedisRateLimiter()


def check_rate_limit(
    key: str,
    limit: int = 60,
    window: int = 60,
    method: str = "fixed"
) -> bool:
    """
    Convenience function for checking rate limits

    Args:
        key: Unique identifier (user_id, ip_address, etc.)
        limit: Maximum requests allowed
        window: Time window in seconds
        method: "fixed" or "sliding" window

    Returns:
        True if request allowed, False if rate limit exceeded
    """
    return rate_limiter.is_allowed(key, limit, window, method)
