from typing import Optional, List
from pydantic import BaseSettings, validator
import os
import secrets


class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "ViralForge.ai"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ViralForge.ai API"

    # Security (MUST be set via environment variables in production)
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32) if os.getenv("ENVIRONMENT") != "production" else "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/viralforge"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI APIs
    OPENAI_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    HEYGEN_API_KEY: Optional[str] = None
    GOOGLE_AI_API_KEY: Optional[str] = None
    KLING_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # External APIs
    SERPAPI_KEY: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    
    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET: str = "viralforge-videos"
    S3_REGION: str = "us-east-1"
    
    # Payments
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_IDS: dict = {
        "starter": "price_starter_monthly",
        "pro": "price_pro_monthly",
        "enterprise": "price_enterprise_monthly"
    }
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://viralforge.ai"]
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # Feature Flags
    ENABLE_AI_AGENTS: bool = True
    ENABLE_BULK_GENERATION: bool = True
    ENABLE_CUSTOM_AVATARS: bool = True
    ENABLE_ANALYTICS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Video Generation
    MAX_VIDEO_DURATION: int = 60  # seconds
    MAX_BULK_VARIANTS: int = 100
    VIDEO_QUALITY: str = "1080p"
    
    # Avatar Library
    DEFAULT_AVATAR_COUNT: int = 1000
    CUSTOM_AVATAR_TRAINING_TIME: int = 3600  # 1 hour in seconds
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v, values):
        """Ensure SECRET_KEY is properly set in production"""
        environment = values.get("ENVIRONMENT", "development")

        if environment == "production":
            if not v or len(v) < 32:
                raise ValueError(
                    "SECRET_KEY must be set and at least 32 characters in production. "
                    "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
                )
            # Check for common insecure defaults
            insecure_defaults = [
                "your-secret-key-change-in-production",
                "secret",
                "changeme",
                "password",
                "12345"
            ]
            if any(insecure in v.lower() for insecure in insecure_defaults):
                raise ValueError("SECRET_KEY appears to be using an insecure default value")

        return v

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        # Warn if using default insecure credentials
        if "user:password" in v:
            import warnings
            warnings.warn(
                "DATABASE_URL appears to use default credentials. "
                "Please update with secure credentials in production.",
                UserWarning
            )
        return v

    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, v, values):
        """Warn if OpenAI key is missing when AI agents are enabled"""
        if values.get("ENABLE_AI_AGENTS") and not v:
            import warnings
            warnings.warn(
                "OPENAI_API_KEY is not set but AI agents are enabled. "
                "AI features will not work properly.",
                UserWarning
            )
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Environment-specific overrides
if os.getenv("ENVIRONMENT") == "production":
    settings.DEBUG = False
elif os.getenv("ENVIRONMENT") == "development":
    settings.DEBUG = True