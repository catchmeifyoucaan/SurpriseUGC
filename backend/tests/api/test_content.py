"""
API Tests for Content Generation Endpoints
Comprehensive tests for script and video generation
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

class TestScriptGeneration:
    """Test script generation endpoints"""

    def test_generate_script_success(self, client: TestClient, auth_headers: dict):
        """Test successful script generation"""
        response = client.post(
            "/api/v1/content/generate-script",
            headers=auth_headers,
            json={
                "product_info": "Revolutionary skincare product that removes wrinkles",
                "target_audience": "Women aged 30-50",
                "platform": "tiktok",
                "count": 3
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 3
        if len(data) > 0:
            assert "script" in data[0]

    def test_generate_script_without_auth(self, client: TestClient):
        """Test script generation without authentication"""
        response = client.post(
            "/api/v1/content/generate-script",
            json={
                "product_info": "Test product",
                "target_audience": "Test audience"
            }
        )

        assert response.status_code == 401

    def test_generate_script_invalid_data(self, client: TestClient, auth_headers: dict):
        """Test script generation with invalid data"""
        response = client.post(
            "/api/v1/content/generate-script",
            headers=auth_headers,
            json={}
        )

        assert response.status_code == 422


class TestVideoGeneration:
    """Test video generation endpoints"""

    def test_generate_video_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_avatar,
        test_voice
    ):
        """Test successful video generation"""
        response = client.post(
            "/api/v1/content/generate-video",
            headers=auth_headers,
            json={
                "script": "This is an amazing product that will change your life!",
                "avatar_id": test_avatar.id,
                "voice_id": test_voice.id,
                "title": "Test Video",
                "language": "en",
                "platform": "tiktok"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Video"
        assert data["status"] == "pending"

    def test_generate_video_without_avatar(self, client: TestClient, auth_headers: dict):
        """Test video generation without avatar"""
        response = client.post(
            "/api/v1/content/generate-video",
            headers=auth_headers,
            json={
                "script": "Test script",
                "avatar_id": "nonexistent-avatar"
            }
        )

        assert response.status_code == 404

    def test_get_user_videos(self, client: TestClient, auth_headers: dict, test_video):
        """Test retrieving user videos"""
        response = client.get(
            "/api/v1/content/videos",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_specific_video(
        self,
        client: TestClient,
        auth_headers: dict,
        test_video
    ):
        """Test retrieving specific video"""
        response = client.get(
            f"/api/v1/content/videos/{test_video.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_video.id
        assert data["title"] == test_video.title

    def test_delete_video(self, client: TestClient, auth_headers: dict, test_video):
        """Test deleting video"""
        response = client.delete(
            f"/api/v1/content/videos/{test_video.id}",
            headers=auth_headers
        )

        assert response.status_code == 200

        # Verify video is deleted
        get_response = client.get(
            f"/api/v1/content/videos/{test_video.id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404


class TestVideoLimits:
    """Test video generation limits"""

    def test_free_user_video_limit(
        self,
        client: TestClient,
        test_user,
        test_avatar,
        session
    ):
        """Test free user reaches video limit"""
        # Set user to free tier with 5 videos generated
        test_user.videos_generated_this_month = 5
        session.add(test_user)
        session.commit()

        from app.core.security import create_access_token
        token = create_access_token(subject=test_user.id)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/v1/content/generate-video",
            headers=headers,
            json={
                "script": "Test",
                "avatar_id": test_avatar.id
            }
        )

        assert response.status_code == 403
        assert "limit" in response.json()["detail"].lower()
