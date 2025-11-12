"""
Input Sanitization and Validation
Prevents XSS, SQL injection, and other injection attacks
"""

import re
import html
from typing import Any, Optional
import bleach
from urllib.parse import urlparse


class InputSanitizer:
    """Sanitize user inputs to prevent injection attacks"""

    # Allowed HTML tags for rich text (very restricted)
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li']
    ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

    @staticmethod
    def sanitize_html(text: str, allow_tags: bool = False) -> str:
        """
        Sanitize HTML input

        Args:
            text: Input text
            allow_tags: Whether to allow limited HTML tags

        Returns:
            Sanitized text
        """
        if not text:
            return ''

        if allow_tags:
            # Allow limited HTML tags
            return bleach.clean(
                text,
                tags=InputSanitizer.ALLOWED_TAGS,
                attributes=InputSanitizer.ALLOWED_ATTRIBUTES,
                strip=True
            )
        else:
            # Strip all HTML
            return bleach.clean(text, tags=[], strip=True)

    @staticmethod
    def sanitize_script(script: str) -> str:
        """
        Sanitize video script input

        Args:
            script: Video script text

        Returns:
            Sanitized script
        """
        if not script:
            return ''

        # Remove any HTML/script tags
        sanitized = InputSanitizer.sanitize_html(script, allow_tags=False)

        # Remove excessive whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)

        # Trim
        sanitized = sanitized.strip()

        return sanitized

    @staticmethod
    def sanitize_email(email: str) -> Optional[str]:
        """
        Validate and sanitize email address

        Args:
            email: Email address

        Returns:
            Sanitized email or None if invalid
        """
        if not email:
            return None

        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        email = email.strip().lower()

        if re.match(email_pattern, email):
            return email

        return None

    @staticmethod
    def sanitize_url(url: str) -> Optional[str]:
        """
        Validate and sanitize URL

        Args:
            url: URL string

        Returns:
            Sanitized URL or None if invalid
        """
        if not url:
            return None

        url = url.strip()

        try:
            parsed = urlparse(url)

            # Must have scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return None

            # Only allow http/https
            if parsed.scheme not in ['http', 'https']:
                return None

            return url

        except Exception:
            return None

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent directory traversal

        Args:
            filename: Original filename

        Returns:
            Safe filename
        """
        if not filename:
            return 'unnamed'

        # Remove path components
        filename = filename.split('/')[-1]
        filename = filename.split('\\')[-1]

        # Remove dangerous characters
        filename = re.sub(r'[^\w\s.-]', '', filename)

        # Remove leading dots
        filename = filename.lstrip('.')

        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:250] + ('.' + ext if ext else '')

        return filename or 'unnamed'

    @staticmethod
    def sanitize_json_field(value: Any) -> Any:
        """
        Recursively sanitize JSON data

        Args:
            value: JSON value (string, dict, list, etc.)

        Returns:
            Sanitized value
        """
        if isinstance(value, str):
            return InputSanitizer.sanitize_html(value, allow_tags=False)
        elif isinstance(value, dict):
            return {
                k: InputSanitizer.sanitize_json_field(v)
                for k, v in value.items()
            }
        elif isinstance(value, list):
            return [InputSanitizer.sanitize_json_field(item) for item in value]
        else:
            return value

    @staticmethod
    def validate_video_title(title: str) -> str:
        """
        Validate and sanitize video title

        Args:
            title: Video title

        Returns:
            Sanitized title

        Raises:
            ValueError: If title is invalid
        """
        if not title:
            raise ValueError('Title cannot be empty')

        title = InputSanitizer.sanitize_html(title, allow_tags=False)
        title = title.strip()

        if len(title) < 3:
            raise ValueError('Title must be at least 3 characters')

        if len(title) > 200:
            raise ValueError('Title must be less than 200 characters')

        return title

    @staticmethod
    def validate_script_length(script: str, max_length: int = 5000) -> bool:
        """
        Validate script length

        Args:
            script: Video script
            max_length: Maximum allowed length

        Returns:
            True if valid

        Raises:
            ValueError: If script is too long
        """
        if not script:
            raise ValueError('Script cannot be empty')

        if len(script) > max_length:
            raise ValueError(f'Script must be less than {max_length} characters')

        return True


# Convenience functions
def sanitize_user_input(text: str) -> str:
    """Sanitize general user input"""
    return InputSanitizer.sanitize_html(text, allow_tags=False)


def sanitize_rich_text(text: str) -> str:
    """Sanitize rich text with limited HTML"""
    return InputSanitizer.sanitize_html(text, allow_tags=True)


def validate_email(email: str) -> str:
    """Validate email and return sanitized version"""
    sanitized = InputSanitizer.sanitize_email(email)
    if not sanitized:
        raise ValueError('Invalid email address')
    return sanitized


def validate_url(url: str) -> str:
    """Validate URL and return sanitized version"""
    sanitized = InputSanitizer.sanitize_url(url)
    if not sanitized:
        raise ValueError('Invalid URL')
    return sanitized
