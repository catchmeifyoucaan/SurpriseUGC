"""
Multi-Model Video Generation Service
Combines Veo3, KWEN3, and other advanced models for maximum quality
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np

from .veo3_generator import generate_veo3_video, generate_veo3_variations
from .kwen3_generator import generate_kwen3_video, generate_kwen3_long_form_video, generate_kwen3_variations
from ..core.config import settings


class MultiModelVideoGenerator:
    """Multi-model video generation combining the world's best AI models"""
    
    def __init__(self):
        self.available_models = {
            "veo3": {
                "name": "Google Veo3",
                "max_duration": 60,
                "quality": "high",
                "strengths": ["cinematic", "realistic", "fast"],
                "api_key_required": "GOOGLE_AI_API_KEY"
            },
            "kwen3": {
                "name": "Kling KWEN3",
                "max_duration": 120,
                "quality": "ultra_hd",
                "strengths": ["photorealistic", "long_form", "advanced_motion"],
                "api_key_required": "KLING_API_KEY"
            },
            "sora": {
                "name": "OpenAI Sora",
                "max_duration": 60,
                "quality": "high",
                "strengths": ["creative", "artistic", "imaginative"],
                "api_key_required": "OPENAI_API_KEY"
            },
            "pika": {
                "name": "Pika Labs",
                "max_duration": 30,
                "quality": "high",
                "strengths": ["fast", "creative", "accessible"],
                "api_key_required": "PIKA_API_KEY"
            }
        }
    
    async def generate_with_best_model(self, 
                                     prompt: str,
                                     duration: int = 15,
                                     aspect_ratio: str = "9:16",
                                     style: str = "cinematic",
                                     quality: str = "high",
                                     use_multiple_models: bool = True) -> Dict[str, Any]:
        """Generate video using the best available model(s)"""
        
        try:
            if use_multiple_models and self._can_use_multiple_models():
                return await self._generate_with_ensemble(prompt, duration, aspect_ratio, style, quality)
            else:
                return await self._generate_with_single_best_model(prompt, duration, aspect_ratio, style, quality)
                
        except Exception as e:
            raise Exception(f"Multi-model generation failed: {str(e)}")
    
    async def _generate_with_ensemble(self, prompt: str, duration: int, aspect_ratio: str, style: str, quality: str) -> Dict[str, Any]:
        """Generate video using multiple models and combine results"""
        
        results = {}
        tasks = []
        
        # Generate with Veo3 if available
        if settings.GOOGLE_AI_API_KEY:
            tasks.append(self._generate_veo3_async(prompt, duration, aspect_ratio, style, quality))
        
        # Generate with KWEN3 if available
        if settings.KLING_API_KEY:
            tasks.append(self._generate_kwen3_async(prompt, duration, aspect_ratio, style, quality))
        
        # Execute all generations concurrently
        if tasks:
            generation_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(generation_results):
                if isinstance(result, dict) and result.get("success"):
                    model_name = list(self.available_models.keys())[i]
                    results[model_name] = result
        
        # Select the best result based on quality scoring
        best_result = self._select_best_result(results, prompt, style, quality)
        
        return {
            "success": True,
            "best_video": best_result,
            "all_results": results,
            "model_used": best_result.get("model", "ensemble"),
            "ensemble_generation": True,
            "generation_time": datetime.utcnow().isoformat()
        }
    
    async def _generate_with_single_best_model(self, prompt: str, duration: int, aspect_ratio: str, style: str, quality: str) -> Dict[str, Any]:
        """Generate video using the single best available model"""
        
        # Priority order: KWEN3 > Veo3 > Sora > Pika
        if settings.KLING_API_KEY:
            return await generate_kwen3_video(prompt, duration, aspect_ratio, style, quality)
        elif settings.GOOGLE_AI_API_KEY:
            return await generate_veo3_video(prompt, duration, aspect_ratio, style, quality)
        else:
            raise Exception("No video generation models available")
    
    async def _generate_veo3_async(self, prompt: str, duration: int, aspect_ratio: str, style: str, quality: str) -> Dict[str, Any]:
        """Generate video with Veo3 asynchronously"""
        try:
            return await generate_veo3_video(prompt, duration, aspect_ratio, style, quality)
        except Exception as e:
            return {"success": False, "error": str(e), "model": "veo3"}
    
    async def _generate_kwen3_async(self, prompt: str, duration: int, aspect_ratio: str, style: str, quality: str) -> Dict[str, Any]:
        """Generate video with KWEN3 asynchronously"""
        try:
            return await generate_kwen3_video(prompt, duration, aspect_ratio, style, quality, motion_scale=1.0)
        except Exception as e:
            return {"success": False, "error": str(e), "model": "kwen3"}
    
    def _select_best_result(self, results: Dict[str, Any], prompt: str, style: str, quality: str) -> Dict[str, Any]:
        """Select the best video result based on quality scoring"""
        
        if not results:
            raise Exception("No successful generations")
        
        # Score each result
        scored_results = []
        
        for model_name, result in results.items():
            if result.get("success"):
                score = self._calculate_quality_score(result, prompt, style, quality)
                scored_results.append((score, result, model_name))
        
        if not scored_results:
            raise Exception("No valid results to select from")
        
        # Return the highest scored result
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return scored_results[0][1]
    
    def _calculate_quality_score(self, result: Dict[str, Any], prompt: str, style: str, quality: str) -> float:
        """Calculate quality score for a video result"""
        
        score = 0.0
        
        # Base quality score
        quality_scores = {
            "standard": 0.7,
            "high": 0.85,
            "ultra_hd": 0.95,
            "4k": 0.98
        }
        
        result_quality = result.get("quality", "high")
        score += quality_scores.get(result_quality, 0.8)
        
        # Model-specific bonuses
        model = result.get("model", "")
        if model == "kwen3":
            score += 0.1  # KWEN3 bonus
        elif model == "veo3":
            score += 0.05  # Veo3 bonus
        
        # Duration bonus (longer videos get higher scores)
        duration = result.get("duration", 15)
        if duration > 30:
            score += 0.05
        
        # Resolution bonus
        resolution = result.get("resolution", "")
        if "4K" in resolution or "3840" in resolution:
            score += 0.1
        
        # File size bonus (larger files often mean higher quality)
        file_size = result.get("file_size", 0)
        if file_size > 10 * 1024 * 1024:  # > 10MB
            score += 0.05
        
        return min(score, 1.0)
    
    def _can_use_multiple_models(self) -> bool:
        """Check if multiple models are available"""
        available_count = 0
        
        if settings.GOOGLE_AI_API_KEY:
            available_count += 1
        if settings.KLING_API_KEY:
            available_count += 1
        
        return available_count >= 2
    
    async def generate_long_form_video(self, 
                                     prompt: str,
                                     duration: int = 60,
                                     aspect_ratio: str = "16:9",
                                     quality: str = "ultra_hd") -> Dict[str, Any]:
        """Generate long-form video using the best available model"""
        
        # KWEN3 is best for long-form videos
        if settings.KLING_API_KEY:
            return await generate_kwen3_long_form_video(prompt, duration, aspect_ratio, quality)
        elif settings.GOOGLE_AI_API_KEY:
            # Veo3 can handle shorter long-form
            max_duration = min(duration, 60)
            return await generate_veo3_video(prompt, max_duration, aspect_ratio, "cinematic", quality)
        else:
            raise Exception("No models available for long-form video generation")
    
    async def generate_video_variations(self, 
                                      base_video_id: str,
                                      variations: int = 3,
                                      models: List[str] = None) -> List[Dict[str, Any]]:
        """Generate video variations using multiple models"""
        
        if models is None:
            models = ["kwen3", "veo3"]  # Default to best models
        
        all_variations = []
        
        for model in models:
            try:
                if model == "kwen3" and settings.KLING_API_KEY:
                    variations_result = await generate_kwen3_variations(base_video_id, variations)
                    all_variations.extend(variations_result)
                elif model == "veo3" and settings.GOOGLE_AI_API_KEY:
                    variations_result = await generate_veo3_variations(base_video_id, variations)
                    all_variations.extend(variations_result)
            except Exception as e:
                print(f"Failed to generate variations with {model}: {e}")
        
        return all_variations
    
    async def generate_style_transfer_video(self, 
                                          base_video_url: str,
                                          target_style: str,
                                          model: str = "best") -> Dict[str, Any]:
        """Generate style transfer video using the best model"""
        
        prompt = f"Apply {target_style} style to this video while maintaining the original content and motion"
        
        if model == "best":
            if settings.KLING_API_KEY:
                return await generate_kwen3_video(prompt, 15, "9:16", target_style, "ultra_hd")
            elif settings.GOOGLE_AI_API_KEY:
                return await generate_veo3_video(prompt, 15, "9:16", target_style, "high")
        elif model == "kwen3" and settings.KLING_API_KEY:
            return await generate_kwen3_video(prompt, 15, "9:16", target_style, "ultra_hd")
        elif model == "veo3" and settings.GOOGLE_AI_API_KEY:
            return await generate_veo3_video(prompt, 15, "9:16", target_style, "high")
        
        raise Exception(f"Style transfer not available with model: {model}")
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get list of available models and their capabilities"""
        
        available = {}
        
        for model_key, model_info in self.available_models.items():
            api_key_attr = model_info["api_key_required"]
            if hasattr(settings, api_key_attr) and getattr(settings, api_key_attr):
                available[model_key] = {
                    **model_info,
                    "available": True
                }
            else:
                available[model_key] = {
                    **model_info,
                    "available": False
                }
        
        return available
    
    async def compare_models(self, prompt: str, duration: int = 15) -> Dict[str, Any]:
        """Compare different models on the same prompt"""
        
        results = {}
        
        # Generate with all available models
        if settings.KLING_API_KEY:
            try:
                results["kwen3"] = await generate_kwen3_video(prompt, duration, "9:16", "cinematic", "ultra_hd")
            except Exception as e:
                results["kwen3"] = {"success": False, "error": str(e)}
        
        if settings.GOOGLE_AI_API_KEY:
            try:
                results["veo3"] = await generate_veo3_video(prompt, duration, "9:16", "cinematic", "high")
            except Exception as e:
                results["veo3"] = {"success": False, "error": str(e)}
        
        # Add comparison metrics
        for model_name, result in results.items():
            if result.get("success"):
                result["quality_score"] = self._calculate_quality_score(result, prompt, "cinematic", "high")
                result["processing_time"] = result.get("generation_time", "")
        
        return {
            "prompt": prompt,
            "duration": duration,
            "results": results,
            "comparison_time": datetime.utcnow().isoformat()
        }


# Global instance
multi_model_generator = MultiModelVideoGenerator()


async def generate_with_best_model(prompt: str,
                                  duration: int = 15,
                                  aspect_ratio: str = "9:16",
                                  style: str = "cinematic",
                                  quality: str = "high",
                                  use_multiple_models: bool = True) -> Dict[str, Any]:
    """Generate video using the best available model(s)"""
    
    return await multi_model_generator.generate_with_best_model(
        prompt=prompt,
        duration=duration,
        aspect_ratio=aspect_ratio,
        style=style,
        quality=quality,
        use_multiple_models=use_multiple_models
    )


async def generate_long_form_video(prompt: str,
                                  duration: int = 60,
                                  aspect_ratio: str = "16:9",
                                  quality: str = "ultra_hd") -> Dict[str, Any]:
    """Generate long-form video using the best available model"""
    
    return await multi_model_generator.generate_long_form_video(
        prompt=prompt,
        duration=duration,
        aspect_ratio=aspect_ratio,
        quality=quality
    )


async def compare_video_models(prompt: str, duration: int = 15) -> Dict[str, Any]:
    """Compare different video generation models"""
    
    return await multi_model_generator.compare_models(prompt, duration)