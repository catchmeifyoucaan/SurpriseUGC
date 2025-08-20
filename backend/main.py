from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.core.config import settings
from app.core.database import init_db, check_db_connection
from app.api import auth, content, quantum_ai


# Sentry configuration
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment="production" if not settings.DEBUG else "development"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting ViralForge.ai API...")
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    
    # Check database connection
    if not check_db_connection():
        print("❌ Database connection check failed")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down ViralForge.ai API...")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="""
    # ViralForge.ai API
    
    The ultimate AI-powered UGC platform for generating viral content at scale.
    
    ## Features
    
    * **AI-Powered Content Generation**: Generate scripts, hooks, and videos using advanced LLMs
    * **Realistic AI Avatars**: 1,000+ lifelike avatars with micro-expressions
    * **Bulk Variant Generation**: Create 100+ video variants for A/B testing
    * **Predictive Analytics**: ROAS/CPA tracking with AI-powered optimization
    * **Global Multi-Language Support**: 65+ languages with cultural adaptation
    
    ## Authentication
    
    Most endpoints require authentication. Use the `/auth/login` endpoint to get access tokens.
    
    ## Rate Limits
    
    * Script generation: 10 requests per minute
    * Content generation: 5 requests per 5 minutes
    * Video generation: Based on subscription plan
    
    ## Subscription Plans
    
    * **Free**: 5 videos/month, basic avatars
    * **Starter**: 20 videos/month, premium avatars
    * **Pro**: 100 videos/month, custom avatars, bulk generation
    * **Enterprise**: Unlimited, API access, dedicated support
    """,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["viralforge.ai", "api.viralforge.ai", "localhost", "127.0.0.1"]
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "Something went wrong"
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_healthy = check_db_connection()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "version": settings.APP_VERSION,
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": "2024-01-01T00:00:00Z"  # In production, use actual timestamp
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ViralForge.ai API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else None,
        "health": "/health"
    }


# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(content.router, prefix=settings.API_V1_STR)
app.include_router(quantum_ai.router, prefix=settings.API_V1_STR)


# Additional API routes for avatars, voices, analytics, etc.
@app.get(f"{settings.API_V1_STR}/avatars")
async def get_avatars():
    """Get available avatars"""
    # This would fetch from database
    # For now, return mock data
    return [
        {
            "id": "avatar_1",
            "name": "Sarah - Young Professional",
            "description": "Confident young professional woman",
            "gender": "female",
            "age_range": "25-35",
            "is_premium": False,
            "languages": ["en", "es", "fr"]
        },
        {
            "id": "avatar_2",
            "name": "Mike - Fitness Enthusiast",
            "description": "Athletic male avatar",
            "gender": "male",
            "age_range": "25-40",
            "is_premium": False,
            "languages": ["en", "es"]
        }
    ]


@app.get(f"{settings.API_V1_STR}/voices")
async def get_voices():
    """Get available voices"""
    # This would fetch from database
    # For now, return mock data
    return [
        {
            "id": "voice_1",
            "name": "Emma - Natural",
            "description": "Warm and natural female voice",
            "gender": "female",
            "language": "en",
            "is_premium": False
        },
        {
            "id": "voice_2",
            "name": "James - Professional",
            "description": "Clear and professional male voice",
            "gender": "male",
            "language": "en",
            "is_premium": False
        }
    ]


@app.get(f"{settings.API_V1_STR}/analytics/overview")
async def get_analytics_overview():
    """Get analytics overview"""
    # This would fetch from database
    # For now, return mock data
    return {
        "total_videos": 163847,
        "total_users": 12456,
        "total_revenue": 284756.32,
        "average_roas": 4.2,
        "top_performing_videos": [
            {
                "id": "video_1",
                "title": "Product Demo Video",
                "views": 125000,
                "conversions": 1250,
                "roas": 8.5
            }
        ]
    }


# Error handlers for specific status codes
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "error": "The requested resource does not exist"
        }
    )


@app.exception_handler(422)
async def validation_error_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "error": "Invalid request data",
            "fields": exc.errors() if hasattr(exc, 'errors') else []
        }
    )


# Development-only endpoints
if settings.DEBUG:
    @app.get("/debug/config")
    async def debug_config():
        """Debug endpoint to show configuration (development only)"""
        return {
            "app_name": settings.APP_NAME,
            "debug": settings.DEBUG,
            "database_url": settings.DATABASE_URL[:20] + "..." if settings.DATABASE_URL else None,
            "cors_origins": settings.BACKEND_CORS_ORIGINS,
            "feature_flags": {
                "enable_ai_agents": settings.ENABLE_AI_AGENTS,
                "enable_bulk_generation": settings.ENABLE_BULK_GENERATION,
                "enable_custom_avatars": settings.ENABLE_CUSTOM_AVATARS,
                "enable_analytics": settings.ENABLE_ANALYTICS
            }
        }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )