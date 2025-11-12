"""
Unit Tests for Security Module
Tests for authentication, authorization, and security utilities
"""

import pytest
from datetime import timedelta
from jose import jwt

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    check_user_permissions,
    check_video_limit,
)
from app.core.config import settings
from app.models.database import User, UserRole


class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password(self):
        """Test that password hashing works"""
        password = "securepassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > 20
        assert hashed.startswith("$2b$")  # bcrypt prefix

    def test_verify_correct_password(self):
        """Test verifying correct password"""
        password = "securepassword123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Test verifying incorrect password"""
        password = "securepassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)"""
        password = "securepassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test JWT token creation and verification"""

    def test_create_access_token(self):
        """Test creating access token"""
        user_id = "user-123"
        token = create_access_token(subject=user_id)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20

    def test_create_refresh_token(self):
        """Test creating refresh token"""
        user_id = "user-123"
        token = create_refresh_token(subject=user_id)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20

    def test_verify_valid_token(self):
        """Test verifying valid token"""
        user_id = "user-123"
        token = create_access_token(subject=user_id)
        decoded_id = verify_token(token)

        assert decoded_id == user_id

    def test_verify_invalid_token(self):
        """Test verifying invalid token"""
        invalid_token = "invalid.token.here"
        decoded_id = verify_token(invalid_token)

        assert decoded_id is None

    def test_token_expiration(self):
        """Test that expired tokens are rejected"""
        user_id = "user-123"
        # Create token that expires immediately
        token = create_access_token(
            subject=user_id,
            expires_delta=timedelta(seconds=-1)
        )

        decoded_id = verify_token(token)
        assert decoded_id is None

    def test_token_payload(self):
        """Test token contains correct payload"""
        user_id = "user-123"
        token = create_access_token(subject=user_id)

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        assert payload["sub"] == user_id
        assert payload["type"] == "access"
        assert "exp" in payload

    def test_refresh_token_type(self):
        """Test refresh token has correct type"""
        user_id = "user-123"
        token = create_refresh_token(subject=user_id)

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        assert payload["type"] == "refresh"


class TestUserPermissions:
    """Test user permission checking"""

    def test_free_user_permissions(self):
        """Test free user has lowest permissions"""
        user = User(
            email="free@test.com",
            hashed_password="hash",
            role=UserRole.FREE
        )

        assert check_user_permissions(user, "free") is True
        assert check_user_permissions(user, "starter") is False
        assert check_user_permissions(user, "pro") is False
        assert check_user_permissions(user, "enterprise") is False

    def test_starter_user_permissions(self):
        """Test starter user permissions"""
        user = User(
            email="starter@test.com",
            hashed_password="hash",
            role=UserRole.STARTER
        )

        assert check_user_permissions(user, "free") is True
        assert check_user_permissions(user, "starter") is True
        assert check_user_permissions(user, "pro") is False
        assert check_user_permissions(user, "enterprise") is False

    def test_pro_user_permissions(self):
        """Test pro user permissions"""
        user = User(
            email="pro@test.com",
            hashed_password="hash",
            role=UserRole.PRO
        )

        assert check_user_permissions(user, "free") is True
        assert check_user_permissions(user, "starter") is True
        assert check_user_permissions(user, "pro") is True
        assert check_user_permissions(user, "enterprise") is False

    def test_enterprise_user_permissions(self):
        """Test enterprise user has all permissions"""
        user = User(
            email="enterprise@test.com",
            hashed_password="hash",
            role=UserRole.ENTERPRISE
        )

        assert check_user_permissions(user, "free") is True
        assert check_user_permissions(user, "starter") is True
        assert check_user_permissions(user, "pro") is True
        assert check_user_permissions(user, "enterprise") is True


class TestVideoLimits:
    """Test video generation limits"""

    def test_free_user_limit(self):
        """Test free user has 5 video limit"""
        user = User(
            email="free@test.com",
            hashed_password="hash",
            role=UserRole.FREE,
            videos_generated_this_month=0
        )

        # Can generate when under limit
        assert check_video_limit(user) is True

        # Can't generate when at limit
        user.videos_generated_this_month = 5
        assert check_video_limit(user) is False

    def test_starter_user_limit(self):
        """Test starter user has 20 video limit"""
        user = User(
            email="starter@test.com",
            hashed_password="hash",
            role=UserRole.STARTER,
            videos_generated_this_month=19
        )

        assert check_video_limit(user) is True

        user.videos_generated_this_month = 20
        assert check_video_limit(user) is False

    def test_pro_user_limit(self):
        """Test pro user has 100 video limit"""
        user = User(
            email="pro@test.com",
            hashed_password="hash",
            role=UserRole.PRO,
            videos_generated_this_month=99
        )

        assert check_video_limit(user) is True

        user.videos_generated_this_month = 100
        assert check_video_limit(user) is False

    def test_enterprise_user_unlimited(self):
        """Test enterprise user has unlimited videos"""
        user = User(
            email="enterprise@test.com",
            hashed_password="hash",
            role=UserRole.ENTERPRISE,
            videos_generated_this_month=999999
        )

        assert check_video_limit(user) is True
