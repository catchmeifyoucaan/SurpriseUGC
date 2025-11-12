"""
OpenAI Service - Real GPT-4 Integration
Handles script generation, content optimization, and AI-powered features
"""

import openai
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging

from ..core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class OpenAIService:
    """Service for OpenAI GPT-4 integration"""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4-turbo-preview"  # Use GPT-4 Turbo for better performance
        self.fallback_model = "gpt-3.5-turbo"  # Fallback if GPT-4 unavailable

    async def generate_viral_script(
        self,
        product_info: str,
        target_audience: str,
        platform: str = "tiktok",
        tone: str = "engaging",
        count: int = 5
    ) -> Dict[str, Any]:
        """
        Generate viral UGC scripts using GPT-4

        Args:
            product_info: Description of the product/service
            target_audience: Target audience description
            platform: Social media platform (tiktok, instagram, youtube)
            tone: Desired tone (engaging, professional, casual, energetic)
            count: Number of script variations to generate

        Returns:
            Dictionary with generated scripts and metadata
        """
        if not self.api_key:
            logger.warning("OpenAI API key not configured, returning mock data")
            return self._generate_mock_scripts(count)

        try:
            prompt = self._build_script_generation_prompt(
                product_info,
                target_audience,
                platform,
                tone
            )

            response = await self._call_openai(
                prompt=prompt,
                temperature=0.8,  # Higher for creativity
                max_tokens=2000
            )

            scripts = self._parse_script_response(response)

            return {
                "success": True,
                "scripts": scripts[:count],
                "model_used": self.model,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"OpenAI script generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "scripts": self._generate_mock_scripts(count),
                "fallback": True
            }

    async def generate_viral_hooks(
        self,
        product_info: str,
        target_audience: str,
        count: int = 10
    ) -> List[str]:
        """
        Generate viral hooks/opening lines

        Args:
            product_info: Description of the product
            target_audience: Target audience description
            count: Number of hooks to generate

        Returns:
            List of viral hook ideas
        """
        if not self.api_key:
            return self._generate_mock_hooks(count)

        try:
            prompt = f"""Generate {count} viral TikTok/Instagram Reels hooks for this product.

Product: {product_info}
Target Audience: {target_audience}

Requirements:
- Each hook should be 5-10 words
- Attention-grabbing and scroll-stopping
- Pattern interrupt techniques
- Question, statement, or bold claim format
- Optimized for short-form video

Return as a numbered list."""

            response = await self._call_openai(prompt, temperature=0.9)
            hooks = self._parse_list_response(response)

            return hooks[:count]

        except Exception as e:
            logger.error(f"Hook generation failed: {str(e)}")
            return self._generate_mock_hooks(count)

    async def generate_cta(
        self,
        product_info: str,
        goal: str = "purchase",
        count: int = 5
    ) -> List[str]:
        """
        Generate call-to-action (CTA) variations

        Args:
            product_info: Description of the product
            goal: Goal of CTA (purchase, signup, learn_more, download)
            count: Number of CTAs to generate

        Returns:
            List of CTA variations
        """
        if not self.api_key:
            return self._generate_mock_ctas(count)

        try:
            prompt = f"""Generate {count} powerful call-to-action (CTA) phrases for this product.

Product: {product_info}
Goal: {goal}

Requirements:
- Action-oriented and urgent
- Benefit-focused
- Short and punchy (under 10 words)
- Different approaches (urgency, FOMO, benefit, social proof)

Return as a numbered list."""

            response = await self._call_openai(prompt, temperature=0.8)
            ctas = self._parse_list_response(response)

            return ctas[:count]

        except Exception as e:
            logger.error(f"CTA generation failed: {str(e)}")
            return self._generate_mock_ctas(count)

    async def optimize_script(
        self,
        script: str,
        optimization_goals: List[str]
    ) -> Dict[str, Any]:
        """
        Optimize an existing script for better performance

        Args:
            script: Original script text
            optimization_goals: List of goals (engagement, conversion, clarity, virality)

        Returns:
            Optimized script with suggestions
        """
        if not self.api_key:
            return {"optimized_script": script, "suggestions": []}

        try:
            prompt = f"""Optimize this UGC video script.

Original Script:
{script}

Optimization Goals: {', '.join(optimization_goals)}

Provide:
1. Optimized version
2. Key improvements made
3. Performance predictions

Format as JSON."""

            response = await self._call_openai(prompt, temperature=0.7)

            # Try to parse as JSON
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                result = {
                    "optimized_script": response,
                    "suggestions": []
                }

            return result

        except Exception as e:
            logger.error(f"Script optimization failed: {str(e)}")
            return {
                "optimized_script": script,
                "suggestions": [],
                "error": str(e)
            }

    async def analyze_virality_potential(
        self,
        script: str,
        platform: str = "tiktok"
    ) -> Dict[str, Any]:
        """
        Analyze the virality potential of a script

        Args:
            script: Script to analyze
            platform: Target platform

        Returns:
            Analysis with virality score and recommendations
        """
        if not self.api_key:
            return {"score": 0.75, "analysis": "Mock analysis"}

        try:
            prompt = f"""Analyze the virality potential of this {platform} script.

Script:
{script}

Provide:
1. Virality score (0-1)
2. Strengths
3. Weaknesses
4. Improvement suggestions
5. Predicted performance metrics

Format as JSON with keys: score, strengths, weaknesses, suggestions, predictions"""

            response = await self._call_openai(prompt, temperature=0.5)

            try:
                analysis = json.loads(response)
            except json.JSONDecodeError:
                analysis = {
                    "score": 0.7,
                    "analysis": response
                }

            return analysis

        except Exception as e:
            logger.error(f"Virality analysis failed: {str(e)}")
            return {
                "score": 0.0,
                "error": str(e)
            }

    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================

    def _build_script_generation_prompt(
        self,
        product_info: str,
        target_audience: str,
        platform: str,
        tone: str
    ) -> str:
        """Build comprehensive prompt for script generation"""
        platform_specs = {
            "tiktok": "15-60 seconds, fast-paced, trending audio",
            "instagram": "15-90 seconds, visually appealing, story-driven",
            "youtube": "30-180 seconds, educational, in-depth"
        }

        spec = platform_specs.get(platform, platform_specs["tiktok"])

        return f"""Generate viral UGC video scripts for {platform}.

PRODUCT INFORMATION:
{product_info}

TARGET AUDIENCE:
{target_audience}

PLATFORM SPECS:
{spec}

TONE: {tone}

Generate 5 complete scripts following this structure:
1. HOOK (first 3 seconds - attention-grabbing)
2. PROBLEM (relate to audience pain point)
3. SOLUTION (introduce product naturally)
4. PROOF (social proof, benefits, results)
5. CTA (clear call-to-action)

Each script should:
- Be authentic and conversational (UGC style)
- Include natural pauses and emphasis markers
- Be 50-150 words
- Feel like a real person talking, not an ad
- Include specific product benefits
- End with a compelling CTA

Return as JSON array with format:
[
  {{
    "hook": "Opening line...",
    "script": "Full script text...",
    "duration_estimate": 30,
    "viral_elements": ["list", "of", "elements"],
    "recommended_visuals": ["visual", "suggestions"]
  }}
]"""

    async def _call_openai(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> str:
        """Make API call to OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert UGC content creator and viral marketing specialist. "
                                   "You understand what makes content go viral and how to write authentic, "
                                   "engaging scripts that drive conversions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )

            return response.choices[0].message.content

        except openai.error.RateLimitError:
            logger.warning("Rate limit hit, trying fallback model")
            # Try fallback model
            response = openai.ChatCompletion.create(
                model=self.fallback_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise

    def _parse_script_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse script generation response"""
        try:
            # Try parsing as JSON first
            scripts = json.loads(response)
            if isinstance(scripts, list):
                return scripts
        except json.JSONDecodeError:
            pass

        # Fallback: parse as structured text
        scripts = []
        lines = response.split('\n')
        current_script = {}

        for line in lines:
            if line.strip().startswith('HOOK:'):
                if current_script:
                    scripts.append(current_script)
                current_script = {"hook": line.replace('HOOK:', '').strip()}
            elif line.strip().startswith('SCRIPT:'):
                current_script["script"] = line.replace('SCRIPT:', '').strip()

        if current_script:
            scripts.append(current_script)

        return scripts

    def _parse_list_response(self, response: str) -> List[str]:
        """Parse numbered list response"""
        items = []
        for line in response.split('\n'):
            # Remove numbering (1., 2., etc.)
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove leading number/dash and clean
                clean_line = line.lstrip('0123456789.-) ').strip()
                if clean_line:
                    items.append(clean_line)

        return items

    def _generate_mock_scripts(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock scripts for testing/fallback"""
        return [
            {
                "hook": f"Stop scrolling! You need to see this (Script {i+1})",
                "script": f"Hey! So I've been using this product for 30 days and honestly? "
                          f"Game changer. Before, I was struggling with [problem]. "
                          f"But now? Everything's different. The best part? It's super easy. "
                          f"Link in bio - you won't regret it!",
                "duration_estimate": 30,
                "viral_elements": ["pattern interrupt", "social proof", "transformation"],
                "score": 0.8
            }
            for i in range(count)
        ]

    def _generate_mock_hooks(self, count: int) -> List[str]:
        """Generate mock hooks"""
        return [
            "POV: You just discovered the secret...",
            "No one talks about this hack",
            "Stop wasting money on [problem]",
            "This changed everything for me",
            "I can't believe this actually works"
        ][:count]

    def _generate_mock_ctas(self, count: int) -> List[str]:
        """Generate mock CTAs"""
        return [
            "Grab yours before they sell out!",
            "Link in bio - you won't regret it",
            "Try it risk-free for 30 days",
            "Join 100K+ happy customers today",
            "Limited time offer - don't miss out!"
        ][:count]


# Global service instance
openai_service = OpenAIService()
