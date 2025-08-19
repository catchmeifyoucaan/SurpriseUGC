from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

from ..core.database import get_session
from ..core.security import get_current_user, check_video_limit, increment_video_count, require_role
from ..models.database import User, Video, Project, VideoStatus, Avatar, Voice
from ..ai_agents.agents import generate_viral_content, generate_script_variants
from ..services.video_generator import generate_video_async, generate_bulk_videos_async

router = APIRouter(prefix="/content", tags=["Content Generation"])

# Pydantic models
class ScriptGenerationRequest(BaseModel):
    product_info: str
    target_audience: str
    platform: str = "tiktok"
    count: int = 5

class VideoGenerationRequest(BaseModel):
    script: str
    avatar_id: str
    voice_id: Optional[str] = None
    language: str = "en"
    platform: str = "tiktok"
    project_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

class BulkGenerationRequest(BaseModel):
    scripts: List[str]
    avatar_ids: List[str]
    voice_ids: Optional[List[str]] = None
    platform: str = "tiktok"
    project_id: Optional[str] = None

class VideoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    script: str
    avatar_id: str
    voice_id: Optional[str] = None
    language: str
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    status: VideoStatus
    duration: Optional[float] = None
    file_size: Optional[int] = None
    views: int
    clicks: int
    conversions: int
    revenue: float
    roas: float
    ctr: float
    cpa: float
    created_at: str

class ScriptResponse(BaseModel):
    type: str
    script: str
    score: Optional[float] = None

class ContentGenerationResponse(BaseModel):
    research: Dict[str, Any]
    scripts: List[ScriptResponse]
    optimization: Dict[str, Any]
    recommended_script: ScriptResponse


@router.post("/generate-script", response_model=List[ScriptResponse])
async def generate_script(
    request: ScriptGenerationRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Generate viral scripts using AI agents"""
    
    try:
        # Check rate limits
        from ..core.security import check_rate_limit
        check_rate_limit(current_user.id, limit=10, window=60)
        
        # Generate scripts using AI agents
        scripts = generate_script_variants(
            product_info=request.product_info,
            target_audience=request.target_audience,
            count=request.count
        )
        
        # Convert to response format
        script_responses = []
        for script_data in scripts:
            if "error" not in script_data:
                script_responses.append(ScriptResponse(
                    type=script_data.get("type", "variant"),
                    script=script_data.get("script", ""),
                    score=script_data.get("score", 0.8)
                ))
        
        return script_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Script generation failed: {str(e)}"
        )


@router.post("/generate-viral-content", response_model=ContentGenerationResponse)
async def generate_viral_content_endpoint(
    product_info: str,
    target_audience: str,
    platform: str = "tiktok",
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Generate complete viral content using AI crew"""
    
    try:
        # Check rate limits
        from ..core.security import check_rate_limit
        check_rate_limit(current_user.id, limit=5, window=300)  # 5 requests per 5 minutes
        
        # Generate viral content using AI crew
        result = generate_viral_content(
            product_info=product_info,
            target_audience=target_audience,
            platform=platform
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Convert to response format
        scripts = []
        for script_data in result.get("final_content", {}).get("script_variants", []):
            scripts.append(ScriptResponse(
                type=script_data.get("type", "variant"),
                script=script_data.get("script", ""),
                score=0.9  # High score for AI-generated content
            ))
        
        return ContentGenerationResponse(
            research=result.get("research", {}),
            scripts=scripts,
            optimization=result.get("final_content", {}).get("optimization_strategy", {}),
            recommended_script=scripts[0] if scripts else ScriptResponse(
                type="default",
                script="Default script",
                score=0.8
            )
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content generation failed: {str(e)}"
        )


@router.post("/generate-video", response_model=VideoResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Generate a single video"""
    
    # Check video generation limits
    if not check_video_limit(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Video generation limit reached for this month"
        )
    
    # Validate avatar exists
    avatar = session.exec(select(Avatar).where(Avatar.id == request.avatar_id)).first()
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    # Validate voice if provided
    if request.voice_id:
        voice = session.exec(select(Voice).where(Voice.id == request.voice_id)).first()
        if not voice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voice not found"
            )
    
    # Create video record
    video = Video(
        user_id=current_user.id,
        project_id=request.project_id,
        title=request.title or f"Video - {avatar.name}",
        description=request.description,
        script=request.script,
        avatar_id=request.avatar_id,
        voice_id=request.voice_id,
        language=request.language,
        status=VideoStatus.PENDING,
        generation_settings={
            "platform": request.platform,
            "language": request.language
        }
    )
    
    session.add(video)
    session.commit()
    session.refresh(video)
    
    # Add background task for video generation
    background_tasks.add_task(
        generate_video_background,
        video_id=video.id,
        script=request.script,
        avatar_id=request.avatar_id,
        voice_id=request.voice_id,
        language=request.language,
        platform=request.platform,
        user_id=current_user.id
    )
    
    # Increment user's video count
    increment_video_count(current_user, session)
    
    return VideoResponse(
        id=video.id,
        title=video.title,
        description=video.description,
        script=video.script,
        avatar_id=video.avatar_id,
        voice_id=video.voice_id,
        language=video.language,
        video_url=video.video_url,
        thumbnail_url=video.thumbnail_url,
        status=video.status,
        duration=video.duration,
        file_size=video.file_size,
        views=video.views,
        clicks=video.clicks,
        conversions=video.conversions,
        revenue=video.revenue,
        roas=video.roas,
        ctr=video.ctr,
        cpa=video.cpa,
        created_at=video.created_at.isoformat()
    )


@router.post("/generate-bulk-videos", response_model=List[VideoResponse])
async def generate_bulk_videos(
    request: BulkGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_role("pro")),
    session: Session = Depends(get_session)
):
    """Generate multiple videos in bulk (Pro+ only)"""
    
    # Check if user can generate bulk videos
    if len(request.scripts) > 100:  # Limit bulk generation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 videos per bulk generation"
        )
    
    # Check video generation limits
    if not check_video_limit(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Video generation limit reached for this month"
        )
    
    # Validate avatars exist
    for avatar_id in request.avatar_ids:
        avatar = session.exec(select(Avatar).where(Avatar.id == avatar_id)).first()
        if not avatar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Avatar {avatar_id} not found"
            )
    
    # Create video records
    videos = []
    for i, script in enumerate(request.scripts):
        avatar_id = request.avatar_ids[i % len(request.avatar_ids)]
        voice_id = request.voice_ids[i % len(request.voice_ids)] if request.voice_ids else None
        
        video = Video(
            user_id=current_user.id,
            project_id=request.project_id,
            title=f"Bulk Video {i+1}",
            script=script,
            avatar_id=avatar_id,
            voice_id=voice_id,
            language="en",
            status=VideoStatus.PENDING,
            generation_settings={
                "platform": request.platform,
                "bulk_generation": True,
                "index": i
            }
        )
        
        session.add(video)
        videos.append(video)
    
    session.commit()
    
    # Add background task for bulk video generation
    background_tasks.add_task(
        generate_bulk_videos_background,
        video_ids=[v.id for v in videos],
        scripts=request.scripts,
        avatar_ids=request.avatar_ids,
        voice_ids=request.voice_ids,
        platform=request.platform,
        user_id=current_user.id
    )
    
    # Increment user's video count
    increment_video_count(current_user, session)
    
    return [
        VideoResponse(
            id=video.id,
            title=video.title,
            description=video.description,
            script=video.script,
            avatar_id=video.avatar_id,
            voice_id=video.voice_id,
            language=video.language,
            video_url=video.video_url,
            thumbnail_url=video.thumbnail_url,
            status=video.status,
            duration=video.duration,
            file_size=video.file_size,
            views=video.views,
            clicks=video.clicks,
            conversions=video.conversions,
            revenue=video.revenue,
            roas=video.roas,
            ctr=video.ctr,
            cpa=video.cpa,
            created_at=video.created_at.isoformat()
        )
        for video in videos
    ]


@router.get("/videos", response_model=List[VideoResponse])
async def get_user_videos(
    skip: int = 0,
    limit: int = 20,
    status: Optional[VideoStatus] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get user's videos"""
    
    query = select(Video).where(Video.user_id == current_user.id)
    
    if status:
        query = query.where(Video.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Video.created_at.desc())
    
    videos = session.exec(query).all()
    
    return [
        VideoResponse(
            id=video.id,
            title=video.title,
            description=video.description,
            script=video.script,
            avatar_id=video.avatar_id,
            voice_id=video.voice_id,
            language=video.language,
            video_url=video.video_url,
            thumbnail_url=video.thumbnail_url,
            status=video.status,
            duration=video.duration,
            file_size=video.file_size,
            views=video.views,
            clicks=video.clicks,
            conversions=video.conversions,
            revenue=video.revenue,
            roas=video.roas,
            ctr=video.ctr,
            cpa=video.cpa,
            created_at=video.created_at.isoformat()
        )
        for video in videos
    ]


@router.get("/videos/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get specific video by ID"""
    
    video = session.exec(
        select(Video).where(Video.id == video_id, Video.user_id == current_user.id)
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    return VideoResponse(
        id=video.id,
        title=video.title,
        description=video.description,
        script=video.script,
        avatar_id=video.avatar_id,
        voice_id=video.voice_id,
        language=video.language,
        video_url=video.video_url,
        thumbnail_url=video.thumbnail_url,
        status=video.status,
        duration=video.duration,
        file_size=video.file_size,
        views=video.views,
        clicks=video.clicks,
        conversions=video.conversions,
        revenue=video.revenue,
        roas=video.roas,
        ctr=video.ctr,
        cpa=video.cpa,
        created_at=video.created_at.isoformat()
    )


@router.delete("/videos/{video_id}")
async def delete_video(
    video_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a video"""
    
    video = session.exec(
        select(Video).where(Video.id == video_id, Video.user_id == current_user.id)
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    session.delete(video)
    session.commit()
    
    return {"message": "Video deleted successfully"}


# Background task functions
async def generate_video_background(
    video_id: str,
    script: str,
    avatar_id: str,
    voice_id: Optional[str],
    language: str,
    platform: str,
    user_id: str
):
    """Background task for video generation"""
    from ..core.database import get_session
    
    session = next(get_session())
    
    try:
        # Update video status to processing
        video = session.exec(select(Video).where(Video.id == video_id)).first()
        if video:
            video.status = VideoStatus.PROCESSING
            session.add(video)
            session.commit()
        
        # Generate video
        result = await generate_video_async(
            script=script,
            avatar_id=avatar_id,
            voice_id=voice_id,
            language=language,
            platform=platform
        )
        
        # Update video with results
        if video and result["success"]:
            video.video_url = result["video_url"]
            video.thumbnail_url = result["thumbnail_url"]
            video.duration = result["duration"]
            video.file_size = result["file_size"]
            video.status = VideoStatus.COMPLETED
        else:
            video.status = VideoStatus.FAILED
            video.error_message = result.get("error", "Unknown error")
        
        session.add(video)
        session.commit()
        
    except Exception as e:
        # Update video status to failed
        video = session.exec(select(Video).where(Video.id == video_id)).first()
        if video:
            video.status = VideoStatus.FAILED
            video.error_message = str(e)
            session.add(video)
            session.commit()


async def generate_bulk_videos_background(
    video_ids: List[str],
    scripts: List[str],
    avatar_ids: List[str],
    voice_ids: Optional[List[str]],
    platform: str,
    user_id: str
):
    """Background task for bulk video generation"""
    from ..core.database import get_session
    
    session = next(get_session())
    
    try:
        # Generate all videos
        results = await generate_bulk_videos_async(
            scripts=scripts,
            avatar_ids=avatar_ids,
            voice_ids=voice_ids,
            platform=platform
        )
        
        # Update videos with results
        for i, result in enumerate(results):
            if i < len(video_ids):
                video = session.exec(select(Video).where(Video.id == video_ids[i])).first()
                if video and result["success"]:
                    video.video_url = result["video_url"]
                    video.thumbnail_url = result["thumbnail_url"]
                    video.duration = result["duration"]
                    video.file_size = result["file_size"]
                    video.status = VideoStatus.COMPLETED
                elif video:
                    video.status = VideoStatus.FAILED
                    video.error_message = result.get("error", "Unknown error")
                
                session.add(video)
        
        session.commit()
        
    except Exception as e:
        # Mark all videos as failed
        for video_id in video_ids:
            video = session.exec(select(Video).where(Video.id == video_id)).first()
            if video:
                video.status = VideoStatus.FAILED
                video.error_message = str(e)
                session.add(video)
        
        session.commit()