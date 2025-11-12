"""
API Tests for Authentication Endpoints
Tests for signup, login, token refresh, and user management
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.database import User


class TestSignup:
    """Test user registration endpoint"""

    def test_signup_success(self, client: TestClient):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@viralforge.ai",
                "password": "SecurePassword123!",
                "full_name": "New User",
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@viralforge.ai"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert "hashed_password" not in data  # Password should not be returned

    def test_signup_duplicate_email(self, client: TestClient, test_user: User):
        """Test signup with duplicate email"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": test_user.email,
                "password": "SecurePassword123!",
                "full_name": "Duplicate User",
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_signup_invalid_email(self, client: TestClient):
        """Test signup with invalid email format"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "not-an-email",
                "password": "SecurePassword123!",
                "full_name": "Invalid Email User",
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signup_weak_password(self, client: TestClient):
        """Test signup with weak password"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "weakpass@viralforge.ai",
                "password": "123",
                "full_name": "Weak Password User",
            }
        )

        # Should fail validation if password rules are enforced
        assert response.status_code in [400, 422]


class TestLogin:
    """Test user login endpoint"""

    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "testpassword123",
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Test login with wrong password"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "wrongpassword",
            }
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with nonexistent email"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@viralforge.ai",
                "password": "somepassword",
            }
        )

        assert response.status_code == 401

    def test_login_inactive_user(self, client: TestClient, session: Session):
        """Test login with inactive user account"""
        # Create inactive user
        from app.core.security import get_password_hash
        inactive_user = User(
            email="inactive@viralforge.ai",
            hashed_password=get_password_hash("password123"),
            full_name="Inactive User",
            is_active=False,
        )
        session.add(inactive_user)
        session.commit()

        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": inactive_user.email,
                "password": "password123",
            }
        )

        assert response.status_code in [400, 401]


class TestTokenRefresh:
    """Test token refresh endpoint"""

    def test_refresh_token_success(self, client: TestClient, test_user: User):
        """Test successful token refresh"""
        # First login to get refresh token
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user.email,
                "password": "testpassword123",
            }
        )
        refresh_token = login_response.json()["refresh_token"]

        # Use refresh token to get new access token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_with_invalid_token(self, client: TestClient):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )

        assert response.status_code == 401


class TestProtectedEndpoints:
    """Test authentication on protected endpoints"""

    def test_access_protected_endpoint_without_auth(self, client: TestClient):
        """Test accessing protected endpoint without authentication"""
        response = client.get("/api/v1/content/videos")

        assert response.status_code == 401

    def test_access_protected_endpoint_with_auth(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test accessing protected endpoint with valid token"""
        response = client.get("/api/v1/content/videos", headers=auth_headers)

        assert response.status_code == 200

    def test_access_with_invalid_token(self, client: TestClient):
        """Test accessing protected endpoint with invalid token"""
        response = client.get(
            "/api/v1/content/videos",
            headers={"Authorization": "Bearer invalid.token"}
        )

        assert response.status_code == 401

    def test_access_with_malformed_header(self, client: TestClient):
        """Test accessing protected endpoint with malformed auth header"""
        response = client.get(
            "/api/v1/content/videos",
            headers={"Authorization": "InvalidFormat token123"}
        )

        assert response.status_code == 401


class TestUserProfile:
    """Test user profile endpoints"""

    def test_get_current_user(self, client: TestClient, auth_headers: dict, test_user: User):
        """Test getting current user profile"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["full_name"] == test_user.full_name
        assert "hashed_password" not in data

    def test_update_user_profile(self, client: TestClient, auth_headers: dict):
        """Test updating user profile"""
        response = client.patch(
            "/api/v1/auth/me",
            headers=auth_headers,
            json={
                "full_name": "Updated Name",
                "company": "Test Company"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["company"] == "Test Company"
