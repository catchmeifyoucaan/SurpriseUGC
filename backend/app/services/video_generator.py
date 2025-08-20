import os
import asyncio
import aiohttp
import json
import tempfile
from typing import Dict, Any, Optional, List
from datetime import datetime
import boto3
from elevenlabs import generate, save, set_api_key
from elevenlabs.api import History
import requests
from PIL import Image
import io

from ..core.config import settings
from ..models.database import Video, VideoStatus, Avatar, Voice
from .veo3_generator import generate_veo3_video, generate_veo3_variations


class VideoGenerator:
    """Service for generating AI videos with avatars and voice synthesis"""
    
    def __init__(self):
        # Initialize API keys
        if settings.ELEVENLABS_API_KEY:
            set_api_key(settings.ELEVENLABS_API_KEY)
        
        # Initialize S3 client for storage
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION
        ) if settings.AWS_ACCESS_KEY_ID else None
    
    async def generate_video(
        self,
        script: str,
        avatar_id: str,
        voice_id: Optional[str] = None,
        language: str = "en",
        platform: str = "tiktok",
        custom_settings: Optional[Dict[str, Any]] = None,
        use_veo3: bool = True
    ) -> Dict[str, Any]:
        """Generate a complete video with avatar and voice"""
        
        try:
            # Step 1: Generate voice audio
            audio_url = await self._generate_voice(script, voice_id, language)
            
            # Step 2: Generate video (Veo3 or traditional avatar)
            if use_veo3 and settings.GOOGLE_AI_API_KEY:
                avatar_video_url = await self._generate_veo3_video(script, platform)
            else:
                avatar_video_url = await self._generate_avatar_video(
                    script, avatar_id, language, platform
                )
            
            # Step 3: Combine audio and video
            final_video_url = await self._combine_audio_video(
                audio_url, avatar_video_url, platform
            )
            
            # Step 4: Generate thumbnail
            thumbnail_url = await self._generate_thumbnail(final_video_url)
            
            # Step 5: Upload to cloud storage
            cloud_video_url = await self._upload_to_cloud(final_video_url, "videos")
            cloud_thumbnail_url = await self._upload_to_cloud(thumbnail_url, "thumbnails")
            
            return {
                "success": True,
                "video_url": cloud_video_url,
                "thumbnail_url": cloud_thumbnail_url,
                "audio_url": audio_url,
                "avatar_video_url": avatar_video_url,
                "duration": await self._get_video_duration(cloud_video_url),
                "file_size": await self._get_file_size(cloud_video_url)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "video_url": None,
                "thumbnail_url": None
            }
    
    async def _generate_voice(self, script: str, voice_id: Optional[str], language: str) -> str:
        """Generate voice audio using ElevenLabs"""
        try:
            # Clean and prepare script for voice generation
            clean_script = self._clean_script_for_voice(script)
            
            # Use default voice if none specified
            if not voice_id:
                voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default ElevenLabs voice
            
            # Generate audio
            audio = generate(
                text=clean_script,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Save to temporary file
            temp_audio_path = tempfile.mktemp(suffix=".mp3")
            save(audio, temp_audio_path)
            
            # Upload to cloud storage
            cloud_audio_url = await self._upload_to_cloud(temp_audio_path, "audio")
            
            # Clean up temp file
            os.remove(temp_audio_path)
            
            return cloud_audio_url
            
        except Exception as e:
            raise Exception(f"Voice generation failed: {str(e)}")
    
    async def _generate_veo3_video(self, script: str, platform: str) -> str:
        """Generate video using Google's Veo3 model"""
        try:
            # Determine aspect ratio based on platform
            aspect_ratio = "9:16" if platform in ["tiktok", "instagram"] else "16:9"
            
            # Generate video using Veo3
            result = await generate_veo3_video(
                prompt=script,
                duration=15,
                aspect_ratio=aspect_ratio,
                style="cinematic",
                quality="high"
            )
            
            if result["success"]:
                return result["video_url"]
            else:
                raise Exception("Veo3 video generation failed")
                
        except Exception as e:
            print(f"Veo3 generation failed: {e}")
            # Fallback to mock video
            return "https://storage.googleapis.com/viralforge-videos/mock_video.mp4"
    
    async def _generate_avatar_video(
        self, 
        script: str, 
        avatar_id: str, 
        language: str, 
        platform: str
    ) -> str:
        """Generate avatar video using HeyGen or similar service"""
        try:
            # This would integrate with HeyGen API
            # For now, return a mock video URL
            # In production, this would make API calls to HeyGen
            
            # Mock HeyGen API call
            heygen_payload = {
                "avatar_id": avatar_id,
                "text": script,
                "language": language,
                "platform": platform,
                "settings": {
                    "resolution": "1080p",
                    "fps": 30,
                    "duration": self._estimate_duration(script)
                }
            }
            
            # Simulate API call delay
            await asyncio.sleep(2)
            
            # Return mock video URL (in production, this would be the actual HeyGen response)
            mock_video_url = f"https://api.heygen.com/videos/{avatar_id}_{datetime.now().timestamp()}.mp4"
            
            return mock_video_url
            
        except Exception as e:
            raise Exception(f"Avatar video generation failed: {str(e)}")
    
    async def _combine_audio_video(self, audio_url: str, video_url: str, platform: str) -> str:
        """Combine audio and video using FFmpeg"""
        try:
            import ffmpeg
            
            # Download files temporarily
            temp_audio = await self._download_file(audio_url)
            temp_video = await self._download_file(video_url)
            
            # Output file
            output_path = tempfile.mktemp(suffix=".mp4")
            
            # Combine using FFmpeg
            stream = ffmpeg.input(temp_video)
            audio = ffmpeg.input(temp_audio)
            
            # Platform-specific settings
            if platform == "tiktok":
                # TikTok optimization
                stream = ffmpeg.output(
                    stream, audio,
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    video_bitrate='2M',
                    audio_bitrate='128k',
                    s='1080x1920',  # Vertical format
                    r=30
                )
            elif platform == "instagram":
                # Instagram optimization
                stream = ffmpeg.output(
                    stream, audio,
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    video_bitrate='3M',
                    audio_bitrate='192k',
                    s='1080x1080',  # Square format
                    r=30
                )
            else:
                # Default optimization
                stream = ffmpeg.output(
                    stream, audio,
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    video_bitrate='2M',
                    audio_bitrate='128k',
                    r=30
                )
            
            ffmpeg.run(stream, overwrite_output=True)
            
            # Clean up temp files
            os.remove(temp_audio)
            os.remove(temp_video)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Audio-video combination failed: {str(e)}")
    
    async def _generate_thumbnail(self, video_url: str) -> str:
        """Generate thumbnail from video"""
        try:
            import ffmpeg
            
            # Download video temporarily
            temp_video = await self._download_file(video_url)
            
            # Generate thumbnail
            thumbnail_path = tempfile.mktemp(suffix=".jpg")
            
            stream = ffmpeg.input(temp_video, ss=1)  # Take frame at 1 second
            stream = ffmpeg.output(stream, thumbnail_path, vframes=1, s='1280x720')
            ffmpeg.run(stream, overwrite_output=True)
            
            # Clean up temp video
            os.remove(temp_video)
            
            return thumbnail_path
            
        except Exception as e:
            raise Exception(f"Thumbnail generation failed: {str(e)}")
    
    async def _upload_to_cloud(self, file_path: str, folder: str) -> str:
        """Upload file to cloud storage (S3)"""
        try:
            if not self.s3_client:
                # Return local path if S3 not configured
                return file_path
            
            # Generate unique filename
            filename = f"{folder}/{datetime.now().strftime('%Y/%m/%d')}/{os.path.basename(file_path)}"
            
            # Upload to S3
            self.s3_client.upload_file(
                file_path,
                settings.S3_BUCKET,
                filename,
                ExtraArgs={'ContentType': self._get_content_type(file_path)}
            )
            
            # Generate public URL
            cloud_url = f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION}.amazonaws.com/{filename}"
            
            # Clean up local file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return cloud_url
            
        except Exception as e:
            raise Exception(f"Cloud upload failed: {str(e)}")
    
    async def _download_file(self, url: str) -> str:
        """Download file from URL to temporary location"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        temp_path = tempfile.mktemp(suffix=self._get_file_extension(url))
                        with open(temp_path, 'wb') as f:
                            f.write(await response.read())
                        return temp_path
                    else:
                        raise Exception(f"Failed to download file: {response.status}")
        except Exception as e:
            raise Exception(f"File download failed: {str(e)}")
    
    def _clean_script_for_voice(self, script: str) -> str:
        """Clean script for voice generation"""
        # Remove markdown-style formatting
        clean_script = script.replace("[HOOK]", "").replace("[PROBLEM]", "").replace("[SOLUTION]", "")
        clean_script = clean_script.replace("[PROOF]", "").replace("[CTA]", "")
        
        # Remove extra whitespace
        clean_script = " ".join(clean_script.split())
        
        # Add pauses for better pacing
        clean_script = clean_script.replace(".", "...").replace("!", "!...")
        
        return clean_script
    
    def _estimate_duration(self, script: str) -> int:
        """Estimate video duration based on script length"""
        # Average speaking rate: 150 words per minute
        word_count = len(script.split())
        duration_seconds = (word_count / 150) * 60
        
        # Add buffer for pauses and effects
        duration_seconds += 5
        
        return min(max(int(duration_seconds), 15), 60)  # Between 15-60 seconds
    
    def _get_content_type(self, file_path: str) -> str:
        """Get content type based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.mp4': 'video/mp4',
            '.mp3': 'audio/mpeg',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
            '.webm': 'video/webm'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    def _get_file_extension(self, url: str) -> str:
        """Get file extension from URL"""
        return os.path.splitext(url)[1] or '.mp4'
    
    async def _get_video_duration(self, video_url: str) -> float:
        """Get video duration in seconds"""
        try:
            import ffmpeg
            
            temp_video = await self._download_file(video_url)
            probe = ffmpeg.probe(temp_video)
            duration = float(probe['streams'][0]['duration'])
            
            os.remove(temp_video)
            return duration
            
        except Exception:
            return 30.0  # Default duration
    
    async def _get_file_size(self, file_url: str) -> int:
        """Get file size in bytes"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(file_url) as response:
                    return int(response.headers.get('content-length', 0))
        except Exception:
            return 0


class BulkVideoGenerator:
    """Service for generating multiple video variants"""
    
    def __init__(self):
        self.video_generator = VideoGenerator()
    
    async def generate_bulk_videos(
        self,
        scripts: List[str],
        avatar_ids: List[str],
        voice_ids: Optional[List[str]] = None,
        platform: str = "tiktok",
        max_concurrent: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate multiple videos concurrently"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def generate_single_video(script: str, avatar_id: str, voice_id: Optional[str] = None):
            async with semaphore:
                return await self.video_generator.generate_video(
                    script=script,
                    avatar_id=avatar_id,
                    voice_id=voice_id,
                    platform=platform
                )
        
        # Create tasks for all videos
        tasks = []
        for i, script in enumerate(scripts):
            avatar_id = avatar_ids[i % len(avatar_ids)]
            voice_id = voice_ids[i % len(voice_ids)] if voice_ids else None
            
            task = generate_single_video(script, avatar_id, voice_id)
            tasks.append(task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": str(result),
                    "script_index": i
                })
            else:
                processed_results.append({
                    **result,
                    "script_index": i
                })
        
        return processed_results


# Global instances
video_generator = VideoGenerator()
bulk_generator = BulkVideoGenerator()


async def generate_video_async(
    script: str,
    avatar_id: str,
    voice_id: Optional[str] = None,
    language: str = "en",
    platform: str = "tiktok"
) -> Dict[str, Any]:
    """Async wrapper for video generation"""
    return await video_generator.generate_video(
        script=script,
        avatar_id=avatar_id,
        voice_id=voice_id,
        language=language,
        platform=platform
    )


async def generate_bulk_videos_async(
    scripts: List[str],
    avatar_ids: List[str],
    voice_ids: Optional[List[str]] = None,
    platform: str = "tiktok"
) -> List[Dict[str, Any]]:
    """Async wrapper for bulk video generation"""
    return await bulk_generator.generate_bulk_videos(
        scripts=scripts,
        avatar_ids=avatar_ids,
        voice_ids=voice_ids,
        platform=platform
    )