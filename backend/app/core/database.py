from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import StaticPool
from typing import Generator
import os

from .config import settings

# Database URL configuration
DATABASE_URL = settings.DATABASE_URL

# Create async engine for production
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # For development with regular PostgreSQL URL
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create tables
def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

# Dependency to get database session
def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session

# Async session dependency
async def get_async_session() -> AsyncSession:
    """Get async database session"""
    async with AsyncSession(engine) as session:
        yield session

# Database initialization
def init_db():
    """Initialize database with default data"""
    from ..models.database import User, Avatar, Voice, UserRole
    from ..core.security import get_password_hash
    
    create_db_and_tables()
    
    # Create default avatars and voices if they don't exist
    with Session(engine) as session:
        # Check if we have default avatars
        avatar_count = session.query(Avatar).count()
        if avatar_count == 0:
            # Create some default avatars
            default_avatars = [
                Avatar(
                    name="Sarah - Young Professional",
                    description="Confident young professional woman, perfect for business and lifestyle content",
                    gender="female",
                    age_range="25-35",
                    personality="confident, professional, approachable",
                    is_premium=False,
                    languages=["en", "es", "fr"]
                ),
                Avatar(
                    name="Mike - Fitness Enthusiast",
                    description="Athletic male avatar ideal for fitness, health, and lifestyle products",
                    gender="male",
                    age_range="25-40",
                    personality="energetic, motivational, authentic",
                    is_premium=False,
                    languages=["en", "es"]
                ),
                Avatar(
                    name="Emma - Creative Entrepreneur",
                    description="Creative and trendy avatar perfect for fashion, beauty, and lifestyle brands",
                    gender="female",
                    age_range="20-30",
                    personality="creative, trendy, authentic",
                    is_premium=True,
                    languages=["en", "fr", "de"]
                ),
                Avatar(
                    name="David - Tech Expert",
                    description="Professional tech-savvy avatar for software, gadgets, and tech reviews",
                    gender="male",
                    age_range="30-45",
                    personality="knowledgeable, trustworthy, engaging",
                    is_premium=True,
                    languages=["en", "es", "pt"]
                ),
                Avatar(
                    name="Lisa - Wellness Coach",
                    description="Calm and nurturing avatar perfect for wellness, health, and mindfulness content",
                    gender="female",
                    age_range="35-50",
                    personality="calm, nurturing, trustworthy",
                    is_premium=False,
                    languages=["en", "es", "it"]
                )
            ]
            
            for avatar in default_avatars:
                session.add(avatar)
        
        # Check if we have default voices
        voice_count = session.query(Voice).count()
        if voice_count == 0:
            # Create some default voices
            default_voices = [
                Voice(
                    name="Emma - Natural",
                    description="Warm and natural female voice",
                    gender="female",
                    age_range="25-35",
                    language="en",
                    is_premium=False
                ),
                Voice(
                    name="James - Professional",
                    description="Clear and professional male voice",
                    gender="male",
                    age_range="30-45",
                    language="en",
                    is_premium=False
                ),
                Voice(
                    name="Sophia - Energetic",
                    description="High-energy female voice for dynamic content",
                    gender="female",
                    age_range="20-30",
                    language="en",
                    is_premium=True
                ),
                Voice(
                    name="Carlos - Friendly",
                    description="Friendly and approachable male voice",
                    gender="male",
                    age_range="25-40",
                    language="en",
                    is_premium=False
                ),
                Voice(
                    name="Isabella - Sophisticated",
                    description="Sophisticated and elegant female voice",
                    gender="female",
                    age_range="30-45",
                    language="en",
                    is_premium=True
                )
            ]
            
            for voice in default_voices:
                session.add(voice)
        
        session.commit()

# Health check function
def check_db_connection():
    """Check database connection health"""
    try:
        with Session(engine) as session:
            session.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False