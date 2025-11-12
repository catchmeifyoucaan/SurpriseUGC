"""
Test Configuration and Fixtures
Shared test fixtures for ViralForge.ai backend tests
"""

import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.models.database import User, Video, Project, Avatar, Voice, UserRole


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(name="engine")
def engine_fixture():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create a new database session for each test"""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database session override"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ============================================================================
# USER FIXTURES
# ============================================================================

@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user"""
    user = User(
        email="test@viralforge.ai",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        role=UserRole.FREE,
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="pro_user")
def pro_user_fixture(session: Session) -> User:
    """Create a pro user for testing premium features"""
    user = User(
        email="pro@viralforge.ai",
        hashed_password=get_password_hash("propassword123"),
        full_name="Pro User",
        role=UserRole.PRO,
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_token")
def test_token_fixture(test_user: User) -> str:
    """Create a valid JWT token for test user"""
    return create_access_token(subject=test_user.id)


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_token: str) -> dict:
    """Create authorization headers for authenticated requests"""
    return {"Authorization": f"Bearer {test_token}"}


# ============================================================================
# CONTENT FIXTURES
# ============================================================================

@pytest.fixture(name="test_project")
def test_project_fixture(session: Session, test_user: User) -> Project:
    """Create a test project"""
    project = Project(
        user_id=test_user.id,
        name="Test Project",
        description="A test project for e-commerce",
        target_audience="Young professionals aged 25-35",
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@pytest.fixture(name="test_avatar")
def test_avatar_fixture(session: Session) -> Avatar:
    """Create a test avatar"""
    avatar = Avatar(
        name="Sarah - Professional",
        description="Confident young professional woman",
        gender="female",
        age_range="25-35",
        is_premium=False,
        languages=["en", "es"],
    )
    session.add(avatar)
    session.commit()
    session.refresh(avatar)
    return avatar


@pytest.fixture(name="test_voice")
def test_voice_fixture(session: Session) -> Voice:
    """Create a test voice"""
    voice = Voice(
        name="Emma - Natural",
        description="Warm and natural female voice",
        gender="female",
        language="en",
        is_premium=False,
    )
    session.add(voice)
    session.commit()
    session.refresh(voice)
    return voice


@pytest.fixture(name="test_video")
def test_video_fixture(session: Session, test_user: User, test_avatar: Avatar) -> Video:
    """Create a test video"""
    video = Video(
        user_id=test_user.id,
        title="Test Video",
        script="This is a test video script about our amazing product!",
        avatar_id=test_avatar.id,
        language="en",
    )
    session.add(video)
    session.commit()
    session.refresh(video)
    return video


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture(name="mock_openai_response")
def mock_openai_response_fixture():
    """Mock OpenAI API response"""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a viral script hook: Transform your skincare routine in 30 seconds!"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150
        }
    }


@pytest.fixture(name="mock_video_generation_result")
def mock_video_generation_result_fixture():
    """Mock video generation result"""
    return {
        "success": True,
        "video_url": "https://cdn.viralforge.ai/videos/test-123.mp4",
        "thumbnail_url": "https://cdn.viralforge.ai/thumbnails/test-123.jpg",
        "duration": 15.0,
        "file_size": 5242880,  # 5MB
    }


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def reset_settings():
    """Reset settings after each test"""
    yield
    # Reset any modified settings here if needed
    pass
