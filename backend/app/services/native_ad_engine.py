"""
Native Ad Engine
Generate ads that don't feel like ads - they feel native to the platform
"""

import asyncio
import json
import requests
import os
import time
import random
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import re
import hashlib

from ..core.config import settings
from ..services.advanced_ai_agents import advanced_ai_agents


class Platform(Enum):
    """Social media platforms for native ad optimization"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"


class AdFormat(Enum):
    """Native ad formats that don't feel like ads"""
    PAIN_POINT_HOOK = "pain_point_hook"
    STORYTELLING = "storytelling"
    PRODUCT_HERO = "product_hero"
    UGC_TESTIMONIAL = "ugc_testimonial"
    BEHIND_SCENES = "behind_scenes"
    EDUCATIONAL = "educational"
    ENTERTAINMENT = "entertainment"
    LIFESTYLE = "lifestyle"


@dataclass
class PainPoint:
    """Pain point for native ad hooks"""
    pain_point: str
    emotion: str
    intensity: int  # 1-10 scale
    target_audience: str
    platform_optimization: Dict[str, Any]
    hook_variations: List[str]


@dataclass
class StoryArc:
    """Story arc for native ad storytelling"""
    story_type: str
    emotional_journey: List[str]
    conflict: str
    resolution: str
    product_integration: str
    authenticity_markers: List[str]


@dataclass
class ProductHero:
    """Product as hero in native ads"""
    product_name: str
    problem_solved: str
    benefit_delivered: str
    transformation: str
    social_proof: str
    call_to_action: str


@dataclass
class NativeAdVariation:
    """Native ad variation for testing"""
    variation_id: str
    platform: Platform
    ad_format: AdFormat
    pain_point_hook: str
    storytelling: str
    product_hero: str
    ai_avatar: Dict[str, Any]
    cultural_adaptation: Dict[str, Any]
    platform_optimization: Dict[str, Any]
    estimated_cpc: float
    viral_potential: float
    authenticity_score: float


class NativeAdEngine:
    """Native Ad Engine - Generate ads that don't feel like ads"""
    
    def __init__(self):
        self.pain_points = self._initialize_pain_points()
        self.story_arcs = self._initialize_story_arcs()
        self.product_heroes = self._initialize_product_heroes()
        self.platform_optimizations = self._initialize_platform_optimizations()
        self.cultural_adaptations = self._initialize_cultural_adaptations()
        self.ai_avatar_templates = self._initialize_ai_avatar_templates()
        
    def _initialize_pain_points(self) -> Dict[str, PainPoint]:
        """Initialize pain points for native ad hooks"""
        
        pain_points = {}
        
        # Mental Health & Wellness
        pain_points["mental_health"] = PainPoint(
            pain_point="Difficulty maintaining daily wellness routines",
            emotion="frustration",
            intensity=8,
            target_audience="25-45, wellness-focused, busy professionals",
            platform_optimization={
                "facebook": "emotional storytelling, community support",
                "instagram": "visual transformation, lifestyle inspiration",
                "tiktok": "quick tips, relatable moments",
                "youtube": "in-depth solutions, expert advice"
            },
            hook_variations=[
                "One of my New Year resolutions was to start journaling, but I find it hard to sit down and write every day.",
                "I've been trying to meditate for months, but my mind just won't shut up.",
                "Everyone says exercise helps with anxiety, but I can't seem to stick to a routine.",
                "I want to be more mindful, but I'm always rushing from one thing to the next.",
                "My therapist suggested I start tracking my mood, but I keep forgetting to do it."
            ]
        )
        
        # Productivity & Time Management
        pain_points["productivity"] = PainPoint(
            pain_point="Struggling to stay organized and productive",
            emotion="overwhelm",
            intensity=9,
            target_audience="22-40, entrepreneurs, remote workers",
            platform_optimization={
                "facebook": "practical solutions, success stories",
                "instagram": "before/after transformations, productivity hacks",
                "tiktok": "quick wins, time-saving tips",
                "youtube": "comprehensive systems, deep dives"
            },
            hook_variations=[
                "I have 47 tabs open right now and I'm still not getting anything done.",
                "My to-do list is longer than my arm, but I keep adding more things.",
                "I spend more time organizing my workspace than actually working.",
                "Every morning I plan my day perfectly, but by 2 PM I'm completely off track.",
                "I'm drowning in notifications and can't focus on what actually matters."
            ]
        )
        
        # Financial Stress
        pain_points["financial_stress"] = PainPoint(
            pain_point="Worrying about money and financial security",
            emotion="anxiety",
            intensity=9,
            target_audience="25-50, middle class, financially conscious",
            platform_optimization={
                "facebook": "financial education, community support",
                "instagram": "wealth building, lifestyle goals",
                "tiktok": "money-saving tips, financial hacks",
                "youtube": "investment strategies, financial planning"
            },
            hook_variations=[
                "I'm 32 and still living paycheck to paycheck, and it's terrifying.",
                "I have no idea where my money goes every month, and I'm too scared to look.",
                "My friends are buying houses while I'm still paying off student loans.",
                "I want to start investing, but I don't know where to begin.",
                "Every time I think I'm getting ahead, something unexpected happens."
            ]
        )
        
        # Relationship & Social
        pain_points["relationships"] = PainPoint(
            pain_point="Difficulty maintaining meaningful relationships",
            emotion="loneliness",
            intensity=7,
            target_audience="20-45, urban, socially active",
            platform_optimization={
                "facebook": "community building, relationship advice",
                "instagram": "social connection, lifestyle sharing",
                "tiktok": "dating tips, friendship advice",
                "youtube": "relationship psychology, communication skills"
            },
            hook_variations=[
                "I have 500 Facebook friends but I feel completely alone.",
                "I'm great at making small talk, but I can't seem to make real connections.",
                "My dating life is a disaster, and I don't know what I'm doing wrong.",
                "I want to be more social, but I'm exhausted just thinking about it.",
                "I feel like everyone else has figured out how to make friends except me."
            ]
        )
        
        # Career & Growth
        pain_points["career_growth"] = PainPoint(
            pain_point="Feeling stuck in career and personal development",
            emotion="frustration",
            intensity=8,
            target_audience="25-45, professionals, career-focused",
            platform_optimization={
                "facebook": "career advice, professional development",
                "instagram": "career milestones, skill building",
                "tiktok": "career tips, job search hacks",
                "youtube": "career coaching, industry insights"
            },
            hook_variations=[
                "I've been in the same job for 5 years and I feel completely stuck.",
                "I want to learn new skills, but I don't know what's worth my time.",
                "Everyone around me is getting promoted while I'm still doing the same work.",
                "I'm passionate about my field, but I'm not sure how to stand out.",
                "I want to start my own business, but I'm paralyzed by fear."
            ]
        )
        
        return pain_points
    
    def _initialize_story_arcs(self) -> Dict[str, StoryArc]:
        """Initialize story arcs for native ad storytelling"""
        
        story_arcs = {}
        
        # Discovery Story
        story_arcs["discovery"] = StoryArc(
            story_type="discovery",
            emotional_journey=["frustration", "hope", "excitement", "gratitude"],
            conflict="Struggling with a persistent problem",
            resolution="Friend recommends a solution that changes everything",
            product_integration="Natural recommendation from trusted source",
            authenticity_markers=[
                "casual conversation",
                "friend's personal experience",
                "immediate improvement",
                "daily ritual formation"
            ]
        )
        
        # Transformation Story
        story_arcs["transformation"] = StoryArc(
            story_type="transformation",
            emotional_journey=["struggle", "determination", "breakthrough", "confidence"],
            conflict="Long-term struggle with no solution in sight",
            resolution="Product provides the missing piece for transformation",
            product_integration="Catalyst for personal growth",
            authenticity_markers=[
                "gradual improvement",
                "measurable results",
                "personal commitment",
                "lasting change"
            ]
        )
        
        # Community Story
        story_arcs["community"] = StoryArc(
            story_type="community",
            emotional_journey=["isolation", "connection", "belonging", "contribution"],
            conflict="Feeling disconnected and alone",
            resolution="Product connects them to like-minded people",
            product_integration="Bridge to community and belonging",
            authenticity_markers=[
                "shared experiences",
                "mutual support",
                "collective growth",
                "meaningful connections"
            ]
        )
        
        # Efficiency Story
        story_arcs["efficiency"] = StoryArc(
            story_type="efficiency",
            emotional_journey=["overwhelm", "clarity", "control", "freedom"],
            conflict="Drowning in complexity and chaos",
            resolution="Product simplifies and streamlines their life",
            product_integration="Tool for regaining control",
            authenticity_markers=[
                "time savings",
                "reduced stress",
                "increased clarity",
                "regained freedom"
            ]
        )
        
        return story_arcs
    
    def _initialize_product_heroes(self) -> Dict[str, ProductHero]:
        """Initialize product heroes for native ads"""
        
        product_heroes = {}
        
        # Wellness App
        product_heroes["wellness_app"] = ProductHero(
            product_name="Recordbook AI",
            problem_solved="Difficulty maintaining daily wellness routines",
            benefit_delivered="Effortless daily reflection and mental health improvement",
            transformation="From struggling to consistent to thriving",
            social_proof="Friend's recommendation and immediate positive results",
            call_to_action="Start your daily wellness ritual today"
        )
        
        # Productivity Tool
        product_heroes["productivity_tool"] = ProductHero(
            product_name="FocusFlow",
            problem_solved="Overwhelm and lack of focus",
            benefit_delivered="Clear priorities and increased productivity",
            transformation="From scattered to focused to accomplished",
            social_proof="Colleague's success story and measurable results",
            call_to_action="Transform your productivity today"
        )
        
        # Financial App
        product_heroes["financial_app"] = ProductHero(
            product_name="MoneyMind",
            problem_solved="Financial stress and lack of control",
            benefit_delivered="Clear financial picture and peace of mind",
            transformation="From anxious to informed to confident",
            social_proof="Friend's financial turnaround and community support",
            call_to_action="Take control of your finances today"
        )
        
        # Learning Platform
        product_heroes["learning_platform"] = ProductHero(
            product_name="SkillSync",
            problem_solved="Career stagnation and skill gaps",
            benefit_delivered="Relevant skills and career advancement",
            transformation="From stuck to growing to advancing",
            social_proof="Peer's career breakthrough and industry recognition",
            call_to_action="Unlock your career potential today"
        )
        
        return product_heroes
    
    def _initialize_platform_optimizations(self) -> Dict[str, Dict[str, Any]]:
        """Initialize platform-specific optimizations"""
        
        return {
            "facebook": {
                "content_length": "150-300 words",
                "tone": "conversational, community-focused",
                "visual_elements": "personal photos, authentic moments",
                "engagement_tactics": "questions, personal stories, community calls",
                "optimal_posting_time": "7-9 AM, 6-8 PM",
                "hashtag_strategy": "community-focused, relatable",
                "call_to_action": "gentle, non-pushy, community-oriented"
            },
            "instagram": {
                "content_length": "100-200 words",
                "tone": "inspirational, lifestyle-focused",
                "visual_elements": "high-quality images, aesthetic appeal",
                "engagement_tactics": "beautiful visuals, aspirational content, story features",
                "optimal_posting_time": "8-10 AM, 6-8 PM",
                "hashtag_strategy": "lifestyle, inspiration, community",
                "call_to_action": "aspirational, lifestyle-enhancing"
            },
            "tiktok": {
                "content_length": "15-60 seconds",
                "tone": "entertaining, relatable, authentic",
                "visual_elements": "casual videos, real moments, trending sounds",
                "engagement_tactics": "trending topics, relatable humor, authentic moments",
                "optimal_posting_time": "7-9 PM, 12-2 PM",
                "hashtag_strategy": "trending, viral, relatable",
                "call_to_action": "casual, non-salesy, community-focused"
            },
            "youtube": {
                "content_length": "2-10 minutes",
                "tone": "educational, helpful, authoritative",
                "visual_elements": "tutorial-style, before/after, demonstrations",
                "engagement_tactics": "value-first content, problem-solving, expertise sharing",
                "optimal_posting_time": "2-4 PM, 7-9 PM",
                "hashtag_strategy": "educational, problem-solving, expertise",
                "call_to_action": "helpful, value-focused, community-building"
            }
        }
    
    def _initialize_cultural_adaptations(self) -> Dict[str, Dict[str, Any]]:
        """Initialize cultural adaptations for global markets"""
        
        return {
            "united_states": {
                "communication_style": "direct, personal, achievement-focused",
                "pain_point_expression": "open, vulnerable, solution-seeking",
                "storytelling_approach": "individual success, personal transformation",
                "product_integration": "practical benefits, measurable results"
            },
            "united_kingdom": {
                "communication_style": "understated, witty, self-deprecating",
                "pain_point_expression": "reserved, humorous, practical",
                "storytelling_approach": "modest success, gradual improvement",
                "product_integration": "subtle benefits, long-term value"
            },
            "germany": {
                "communication_style": "precise, logical, quality-focused",
                "pain_point_expression": "analytical, systematic, solution-oriented",
                "storytelling_approach": "methodical improvement, proven results",
                "product_integration": "technical benefits, reliability"
            },
            "japan": {
                "communication_style": "respectful, community-focused, harmony-seeking",
                "pain_point_expression": "collective challenges, group solutions",
                "storytelling_approach": "community improvement, shared success",
                "product_integration": "social benefits, group harmony"
            },
            "brazil": {
                "communication_style": "warm, emotional, relationship-focused",
                "communication_style": "warm, emotional, relationship-focused",
                "pain_point_expression": "passionate, expressive, community-oriented",
                "storytelling_approach": "emotional transformation, social connection",
                "product_integration": "relationship benefits, social impact"
            }
        }
    
    def _initialize_ai_avatar_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize AI avatar templates for native ads"""
        
        return {
            "authentic_friend": {
                "personality": "warm, relatable, trustworthy",
                "communication_style": "casual, conversational, genuine",
                "appearance": "approachable, diverse, real-looking",
                "background": "everyday person, relatable experiences",
                "credibility_markers": ["personal story", "friend recommendation", "immediate results"]
            },
            "successful_peer": {
                "personality": "confident, inspiring, approachable",
                "communication_style": "encouraging, motivational, authentic",
                "appearance": "professional, polished, relatable",
                "background": "achievement story, transformation journey",
                "credibility_markers": ["measurable results", "transformation story", "expertise sharing"]
            },
            "community_leader": {
                "personality": "inclusive, supportive, knowledgeable",
                "communication_style": "educational, helpful, community-focused",
                "appearance": "approachable, trustworthy, diverse",
                "background": "community building, helping others, shared success",
                "credibility_markers": ["community impact", "helping others", "collective success"]
            },
            "everyday_hero": {
                "personality": "determined, resilient, inspiring",
                "communication_style": "honest, vulnerable, motivational",
                "appearance": "real, relatable, diverse",
                "background": "overcoming challenges, personal growth, transformation",
                "credibility_markers": ["personal struggle", "breakthrough moment", "lasting change"]
            }
        }
    
    async def generate_native_ad_variations(self, 
                                         product_info: Dict[str, Any],
                                         target_audience: str,
                                         platform: Platform,
                                         cultural_market: str = "united_states",
                                         num_variations: int = 100) -> List[NativeAdVariation]:
        """Generate 100+ native ad variations for testing"""
        
        try:
            variations = []
            
            # Get relevant pain points for target audience
            relevant_pain_points = self._get_relevant_pain_points(target_audience)
            
            # Get story arcs and product hero info
            story_arcs = list(self.story_arcs.values())
            product_hero = self._get_product_hero(product_info)
            
            # Generate variations
            for i in range(num_variations):
                variation = await self._create_single_variation(
                    product_info, target_audience, platform, cultural_market,
                    relevant_pain_points, story_arcs, product_hero, i
                )
                variations.append(variation)
            
            return variations
            
        except Exception as e:
            raise Exception(f"Native ad variation generation failed: {str(e)}")
    
    async def _create_single_variation(self, 
                                     product_info: Dict[str, Any],
                                     target_audience: str,
                                     platform: Platform,
                                     cultural_market: str,
                                     pain_points: List[PainPoint],
                                     story_arcs: List[StoryArc],
                                     product_hero: ProductHero,
                                     variation_index: int) -> NativeAdVariation:
        """Create a single native ad variation"""
        
        # Select random pain point, story arc, and AI avatar
        pain_point = random.choice(pain_points)
        story_arc = random.choice(story_arcs)
        ai_avatar = random.choice(list(self.ai_avatar_templates.values()))
        
        # Generate pain point hook
        pain_point_hook = self._generate_pain_point_hook(
            pain_point, platform, cultural_market, variation_index
        )
        
        # Generate storytelling
        storytelling = self._generate_storytelling(
            story_arc, product_hero, platform, cultural_market, variation_index
        )
        
        # Generate product hero section
        product_hero_section = self._generate_product_hero_section(
            product_hero, story_arc, platform, cultural_market, variation_index
        )
        
        # Calculate metrics
        estimated_cpc = self._calculate_estimated_cpc(
            pain_point, story_arc, platform, cultural_market
        )
        viral_potential = self._calculate_viral_potential(
            pain_point, story_arc, platform, cultural_market
        )
        authenticity_score = self._calculate_authenticity_score(
            pain_point, story_arc, ai_avatar, platform, cultural_market
        )
        
        return NativeAdVariation(
            variation_id=f"native_ad_{variation_index:03d}",
            platform=platform,
            ad_format=AdFormat.PAIN_POINT_HOOK,
            pain_point_hook=pain_point_hook,
            storytelling=storytelling,
            product_hero=product_hero_section,
            ai_avatar=ai_avatar,
            cultural_adaptation=self.cultural_adaptations.get(cultural_market, {}),
            platform_optimization=self.platform_optimizations.get(platform.value, {}),
            estimated_cpc=estimated_cpc,
            viral_potential=viral_potential,
            authenticity_score=authenticity_score
        )
    
    def _generate_pain_point_hook(self, 
                                 pain_point: PainPoint,
                                 platform: Platform,
                                 cultural_market: str,
                                 variation_index: int) -> str:
        """Generate pain point hook for native ad"""
        
        # Get base hook
        base_hook = random.choice(pain_point.hook_variations)
        
        # Apply platform optimization
        platform_opt = self.platform_optimizations.get(platform.value, {})
        
        # Apply cultural adaptation
        cultural_opt = self.cultural_adaptations.get(cultural_market, {})
        
        # Apply variation-specific modifications
        modifications = self._get_hook_modifications(variation_index)
        
        # Combine all elements
        final_hook = self._apply_hook_optimizations(
            base_hook, platform_opt, cultural_opt, modifications
        )
        
        return final_hook
    
    def _generate_storytelling(self, 
                              story_arc: StoryArc,
                              product_hero: ProductHero,
                              platform: Platform,
                              cultural_market: str,
                              variation_index: int) -> str:
        """Generate storytelling section for native ad"""
        
        # Create story based on arc
        story = f"And I told my friend this, and she recommended {product_hero.product_name}. "
        
        # Add emotional journey
        story += f"And basically, {self._get_story_details(story_arc, variation_index)}"
        
        # Add product integration
        story += f" {product_hero.benefit_delivered}, and I can feel {product_hero.transformation}."
        
        # Apply platform and cultural optimization
        story = self._apply_storytelling_optimizations(
            story, platform, cultural_market, variation_index
        )
        
        return story
    
    def _generate_product_hero_section(self, 
                                     product_hero: ProductHero,
                                     story_arc: StoryArc,
                                     platform: Platform,
                                     cultural_market: str,
                                     variation_index: int) -> str:
        """Generate product hero section for native ad"""
        
        # Create product hero narrative
        hero_section = f"{product_hero.product_name} has become my daily ritual. "
        hero_section += f"It's not just about {product_hero.problem_solved}, "
        hero_section += f"it's about {product_hero.benefit_delivered}. "
        hero_section += f"I can honestly say it's {product_hero.social_proof}."
        
        # Apply optimizations
        hero_section = self._apply_product_hero_optimizations(
            hero_section, platform, cultural_market, variation_index
        )
        
        return hero_section
    
    def _get_relevant_pain_points(self, target_audience: str) -> List[PainPoint]:
        """Get relevant pain points for target audience"""
        
        # This would use AI to analyze target audience and select relevant pain points
        # For now, returning all pain points
        return list(self.pain_points.values())
    
    def _get_product_hero(self, product_info: Dict[str, Any]) -> ProductHero:
        """Get product hero information"""
        
        # This would use AI to generate product hero based on product info
        # For now, returning a default wellness app hero
        return self.product_heroes["wellness_app"]
    
    def _get_hook_modifications(self, variation_index: int) -> List[str]:
        """Get hook modifications for variation"""
        
        modifications = [
            "adding urgency",
            "increasing specificity",
            "enhancing emotional impact",
            "improving relatability",
            "adding cultural context"
        ]
        
        # Select modifications based on variation index
        selected_modifications = modifications[:variation_index % len(modifications) + 1]
        return selected_modifications
    
    def _get_story_details(self, story_arc: StoryArc, variation_index: int) -> str:
        """Get story details for variation"""
        
        # This would use AI to generate unique story details
        # For now, returning template-based details
        if story_arc.story_type == "discovery":
            return "I can just talk to it, and it will ask me questions about my day, and it helps me be so much more introspective and mindful"
        elif story_arc.story_type == "transformation":
            return "it guides me through a process that actually works, and I'm seeing real changes in my daily life"
        elif story_arc.story_type == "community":
            return "it connects me with people who are on the same journey, and we support each other"
        elif story_arc.story_type == "efficiency":
            return "it streamlines everything so I can focus on what actually matters"
        
        return "it helps me in ways I never expected, and I'm genuinely excited about the results"
    
    def _apply_hook_optimizations(self, 
                                 hook: str,
                                 platform_opt: Dict[str, Any],
                                 cultural_opt: Dict[str, Any],
                                 modifications: List[str]) -> str:
        """Apply optimizations to pain point hook"""
        
        # Apply platform-specific optimizations
        if platform_opt.get("tone") == "conversational":
            hook = hook.replace("I find it hard", "I just can't seem to")
        
        # Apply cultural adaptations
        if cultural_opt.get("communication_style") == "understated":
            hook = hook.replace("terrifying", "concerning")
        
        # Apply modifications
        if "adding urgency" in modifications:
            hook += " And I'm running out of time to figure this out."
        
        return hook
    
    def _apply_storytelling_optimizations(self, 
                                        story: str,
                                        platform: Platform,
                                        cultural_market: str,
                                        variation_index: int) -> str:
        """Apply optimizations to storytelling section"""
        
        # Apply platform-specific optimizations
        platform_opt = self.platform_optimizations.get(platform.value, {})
        
        if platform_opt.get("tone") == "conversational":
            story = story.replace("And basically", "So basically")
        
        # Apply cultural adaptations
        cultural_opt = self.cultural_adaptations.get(cultural_market, {})
        
        if cultural_opt.get("communication_style") == "understated":
            story = story.replace("amazing", "pretty good")
        
        return story
    
    def _apply_product_hero_optimizations(self, 
                                        hero_section: str,
                                        platform: Platform,
                                        cultural_market: str,
                                        variation_index: int) -> str:
        """Apply optimizations to product hero section"""
        
        # Apply platform-specific optimizations
        platform_opt = self.platform_optimizations.get(platform.value, {})
        
        if platform_opt.get("call_to_action") == "gentle":
            hero_section += " Maybe it could help you too."
        
        # Apply cultural adaptations
        cultural_opt = self.cultural_adaptations.get(cultural_market, {})
        
        if cultural_opt.get("communication_style") == "modest":
            hero_section = hero_section.replace("genuinely excited", "pretty pleased")
        
        return hero_section
    
    def _calculate_estimated_cpc(self, 
                                pain_point: PainPoint,
                                story_arc: StoryArc,
                                platform: Platform,
                                cultural_market: str) -> float:
        """Calculate estimated CPC for variation"""
        
        # Base CPC
        base_cpc = 0.50
        
        # Pain point intensity adjustment
        intensity_multiplier = pain_point.intensity / 10.0
        
        # Platform adjustment
        platform_multipliers = {
            "facebook": 1.0,
            "instagram": 1.2,
            "tiktok": 0.8,
            "youtube": 1.5
        }
        platform_multiplier = platform_multipliers.get(platform.value, 1.0)
        
        # Cultural market adjustment
        cultural_multipliers = {
            "united_states": 1.0,
            "united_kingdom": 1.1,
            "germany": 1.3,
            "japan": 1.4,
            "brazil": 0.9
        }
        cultural_multiplier = cultural_multipliers.get(cultural_market, 1.0)
        
        # Calculate final CPC
        estimated_cpc = base_cpc * intensity_multiplier * platform_multiplier * cultural_multiplier
        
        # Add some randomness for variation
        estimated_cpc *= random.uniform(0.8, 1.2)
        
        return round(estimated_cpc, 2)
    
    def _calculate_viral_potential(self, 
                                  pain_point: PainPoint,
                                  story_arc: StoryArc,
                                  platform: Platform,
                                  cultural_market: str) -> float:
        """Calculate viral potential for variation"""
        
        # Base viral potential
        base_potential = 0.5
        
        # Pain point relevance
        pain_relevance = pain_point.intensity / 10.0
        
        # Story arc emotional impact
        emotional_impact = len(story_arc.emotional_journey) / 4.0
        
        # Platform viral potential
        platform_potentials = {
            "facebook": 0.6,
            "instagram": 0.7,
            "tiktok": 0.9,
            "youtube": 0.5
        }
        platform_potential = platform_potentials.get(platform.value, 0.5)
        
        # Calculate final viral potential
        viral_potential = (base_potential + pain_relevance + emotional_impact + platform_potential) / 4
        
        # Add some randomness
        viral_potential *= random.uniform(0.9, 1.1)
        
        return min(1.0, max(0.0, viral_potential))
    
    def _calculate_authenticity_score(self, 
                                    pain_point: PainPoint,
                                    story_arc: StoryArc,
                                    ai_avatar: Dict[str, Any],
                                    platform: Platform,
                                    cultural_market: str) -> float:
        """Calculate authenticity score for variation"""
        
        # Base authenticity
        base_authenticity = 0.7
        
        # Pain point authenticity
        pain_authenticity = pain_point.intensity / 10.0
        
        # Story arc authenticity
        story_authenticity = len(story_arc.authenticity_markers) / 4.0
        
        # AI avatar authenticity
        avatar_authenticity = 0.8 if "personal story" in ai_avatar.get("credibility_markers", []) else 0.6
        
        # Platform authenticity
        platform_authenticities = {
            "facebook": 0.8,
            "instagram": 0.7,
            "tiktok": 0.9,
            "youtube": 0.6
        }
        platform_authenticity = platform_authenticities.get(platform.value, 0.7)
        
        # Calculate final authenticity score
        authenticity_score = (base_authenticity + pain_authenticity + story_authenticity + 
                            avatar_authenticity + platform_authenticity) / 5
        
        # Add some randomness
        authenticity_score *= random.uniform(0.95, 1.05)
        
        return min(1.0, max(0.0, authenticity_score))
    
    async def test_ad_variations(self, 
                               variations: List[NativeAdVariation],
                               test_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Test ad variations to find optimal performance"""
        
        try:
            test_results = []
            
            # Simulate testing each variation
            for variation in variations:
                result = await self._test_single_variation(variation, test_parameters)
                test_results.append(result)
            
            # Sort by performance
            test_results.sort(key=lambda x: x["performance_score"], reverse=True)
            
            # Get top performers
            top_performers = test_results[:10]
            
            return {
                "success": True,
                "total_variations_tested": len(variations),
                "top_performers": top_performers,
                "performance_insights": self._generate_performance_insights(test_results),
                "optimization_recommendations": self._generate_optimization_recommendations(test_results)
            }
            
        except Exception as e:
            raise Exception(f"Ad variation testing failed: {str(e)}")
    
    async def _test_single_variation(self, 
                                   variation: NativeAdVariation,
                                   test_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single ad variation"""
        
        # Simulate performance metrics
        impressions = random.randint(1000, 10000)
        clicks = random.randint(50, 500)
        conversions = random.randint(5, 50)
        
        # Calculate metrics
        ctr = clicks / impressions if impressions > 0 else 0
        cpc = variation.estimated_cpc * random.uniform(0.8, 1.2)
        conversion_rate = conversions / clicks if clicks > 0 else 0
        
        # Calculate performance score
        performance_score = (ctr * 0.4 + (1 - cpc) * 0.3 + conversion_rate * 0.3)
        
        return {
            "variation_id": variation.variation_id,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "ctr": ctr,
            "cpc": cpc,
            "conversion_rate": conversion_rate,
            "performance_score": performance_score,
            "viral_potential": variation.viral_potential,
            "authenticity_score": variation.authenticity_score
        }
    
    def _generate_performance_insights(self, test_results: List[Dict[str, Any]]) -> List[str]:
        """Generate performance insights from test results"""
        
        insights = []
        
        # Top performer insights
        top_performer = test_results[0] if test_results else None
        if top_performer:
            insights.append(f"Top performer achieved {top_performer['performance_score']:.2f} performance score")
        
        # CPC insights
        avg_cpc = sum(r["cpc"] for r in test_results) / len(test_results) if test_results else 0
        insights.append(f"Average CPC across all variations: ${avg_cpc:.2f}")
        
        # CTR insights
        avg_ctr = sum(r["ctr"] for r in test_results) / len(test_results) if test_results else 0
        insights.append(f"Average CTR across all variations: {avg_ctr:.2%}")
        
        return insights
    
    def _generate_optimization_recommendations(self, test_results: List[Dict[str, Any]]) -> List[str]:
        """Generate optimization recommendations from test results"""
        
        recommendations = []
        
        # Performance-based recommendations
        if test_results:
            top_performers = test_results[:5]
            avg_viral_potential = sum(r["viral_potential"] for r in top_performers) / len(top_performers)
            
            if avg_viral_potential > 0.8:
                recommendations.append("Focus on high viral potential variations for organic reach")
            
            avg_authenticity = sum(r["authenticity_score"] for r in top_performers) / len(top_performers)
            if avg_authenticity > 0.8:
                recommendations.append("Emphasize authenticity in future variations")
        
        # General recommendations
        recommendations.extend([
            "Test variations across different times and audiences",
            "Monitor performance trends and adjust strategy accordingly",
            "Scale successful variations while continuing to test new ones"
        ])
        
        return recommendations


# Global instance
native_ad_engine = NativeAdEngine()


async def generate_native_ad_variations(product_info: Dict[str, Any], **kwargs) -> List[NativeAdVariation]:
    """Generate 100+ native ad variations for testing"""
    return await native_ad_engine.generate_native_ad_variations(product_info, **kwargs)


async def test_ad_variations(variations: List[NativeAdVariation], **kwargs) -> Dict[str, Any]:
    """Test ad variations to find optimal performance"""
    return await native_ad_engine.test_ad_variations(variations, **kwargs)