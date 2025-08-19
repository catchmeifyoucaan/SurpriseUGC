from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
import uuid


class UserRole(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class VideoStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AvatarType(str, Enum):
    DEFAULT = "default"
    CUSTOM = "custom"
    HYBRID = "hybrid"


class ContentType(str, Enum):
    UGC = "ugc"
    AD = "ad"
    TESTIMONIAL = "testimonial"
    PRODUCT_DEMO = "product_demo"


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    company: Optional[str] = None
    role: UserRole = Field(default=UserRole.FREE)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Subscription fields
    stripe_customer_id: Optional[str] = None
    subscription_id: Optional[str] = None
    subscription_status: Optional[str] = None
    subscription_end_date: Optional[datetime] = None
    
    # Usage tracking
    videos_generated_this_month: int = Field(default=0)
    videos_generated_total: int = Field(default=0)
    last_reset_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    projects: List["Project"] = Relationship(back_populates="user")
    videos: List["Video"] = Relationship(back_populates="user")
    analytics: List["Analytics"] = Relationship(back_populates="user")


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    name: str
    description: Optional[str] = None
    product_url: Optional[str] = None
    target_audience: Optional[str] = None
    content_type: ContentType = Field(default=ContentType.UGC)
    brand_guidelines: Optional[Dict[str, Any]] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="projects")
    videos: List["Video"] = Relationship(back_populates="project")


class Video(SQLModel, table=True):
    __tablename__ = "videos"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    project_id: Optional[str] = Field(foreign_key="projects.id")
    
    # Content details
    title: str
    description: Optional[str] = None
    script: str
    hook: Optional[str] = None
    cta: Optional[str] = None
    
    # Avatar and voice
    avatar_id: str
    avatar_type: AvatarType = Field(default=AvatarType.DEFAULT)
    voice_id: Optional[str] = None
    language: str = Field(default="en")
    
    # Video files
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None
    
    # Generation settings
    status: VideoStatus = Field(default=VideoStatus.PENDING)
    generation_settings: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    
    # Performance metrics
    views: int = Field(default=0)
    clicks: int = Field(default=0)
    conversions: int = Field(default=0)
    revenue: float = Field(default=0.0)
    roas: float = Field(default=0.0)
    ctr: float = Field(default=0.0)
    cpa: float = Field(default=0.0)
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    is_public: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="videos")
    project: Optional[Project] = Relationship(back_populates="videos")
    analytics: List["Analytics"] = Relationship(back_populates="video")


class Analytics(SQLModel, table=True):
    __tablename__ = "analytics"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    video_id: Optional[str] = Field(foreign_key="videos.id")
    
    # Metrics
    date: datetime = Field(default_factory=datetime.utcnow)
    platform: str  # facebook, tiktok, youtube, etc.
    campaign_id: Optional[str] = None
    
    # Performance data
    impressions: int = Field(default=0)
    views: int = Field(default=0)
    clicks: int = Field(default=0)
    conversions: int = Field(default=0)
    spend: float = Field(default=0.0)
    revenue: float = Field(default=0.0)
    
    # Calculated metrics
    ctr: float = Field(default=0.0)
    cpc: float = Field(default=0.0)
    cpa: float = Field(default=0.0)
    roas: float = Field(default=0.0)
    
    # Engagement metrics
    likes: int = Field(default=0)
    shares: int = Field(default=0)
    comments: int = Field(default=0)
    watch_time: float = Field(default=0.0)
    
    # Relationships
    user: User = Relationship(back_populates="analytics")
    video: Optional[Video] = Relationship(back_populates="analytics")


class Avatar(SQLModel, table=True):
    __tablename__ = "avatars"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    avatar_type: AvatarType = Field(default=AvatarType.DEFAULT)
    
    # Avatar details
    gender: Optional[str] = None
    age_range: Optional[str] = None
    ethnicity: Optional[str] = None
    personality: Optional[str] = None
    
    # Media files
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    
    # Availability
    is_available: bool = Field(default=True)
    is_premium: bool = Field(default=False)
    languages: List[str] = Field(default_factory=list)
    
    # Usage stats
    usage_count: int = Field(default=0)
    average_rating: float = Field(default=0.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Voice(SQLModel, table=True):
    __tablename__ = "voices"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    
    # Voice characteristics
    gender: Optional[str] = None
    age_range: Optional[str] = None
    accent: Optional[str] = None
    language: str = Field(default="en")
    
    # ElevenLabs integration
    elevenlabs_voice_id: Optional[str] = None
    
    # Availability
    is_available: bool = Field(default=True)
    is_premium: bool = Field(default=False)
    
    # Usage stats
    usage_count: int = Field(default=0)
    average_rating: float = Field(default=0.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GenerationJob(SQLModel, table=True):
    __tablename__ = "generation_jobs"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    video_id: Optional[str] = Field(foreign_key="videos.id")
    
    # Job details
    job_type: str  # script_generation, video_generation, bulk_generation
    status: str = Field(default="pending")  # pending, processing, completed, failed
    priority: int = Field(default=1)
    
    # Job data
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    # Processing info
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time: Optional[float] = None
    
    # Celery integration
    celery_task_id: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    
    # Stripe integration
    stripe_subscription_id: str
    stripe_customer_id: str
    stripe_price_id: str
    
    # Subscription details
    plan_type: UserRole
    status: str  # active, canceled, past_due, etc.
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = Field(default=False)
    
    # Usage limits
    monthly_video_limit: int
    videos_generated_this_month: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)