from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
import json
import requests
from bs4 import BeautifulSoup
import re
import asyncio

from ..core.config import settings
from ..services.openai_service import openai_service


class TrendResearchTool(BaseTool):
    """Tool for researching trends and pain points"""
    
    name: str = "trend_research"
    description: str = "Research trending topics, pain points, and viral content patterns"
    
    def _run(self, query: str) -> str:
        """Research trends and pain points"""
        try:
            # Search for trending topics
            search_results = self._search_trends(query)
            
            # Extract pain points from Reddit
            reddit_pains = self._get_reddit_pains(query)
            
            # Get viral content patterns
            viral_patterns = self._analyze_viral_patterns(query)
            
            return json.dumps({
                "trending_topics": search_results,
                "pain_points": reddit_pains,
                "viral_patterns": viral_patterns
            }, indent=2)
        except Exception as e:
            return f"Error researching trends: {str(e)}"
    
    def _search_trends(self, query: str) -> List[Dict]:
        """Search for trending topics"""
        # This would integrate with Google Trends, Twitter API, etc.
        # For now, return mock data
        return [
            {"topic": "sustainable living", "trend_score": 85},
            {"topic": "remote work productivity", "trend_score": 92},
            {"topic": "mental health awareness", "trend_score": 78}
        ]
    
    def _get_reddit_pains(self, query: str) -> List[str]:
        """Extract pain points from Reddit"""
        # This would use Reddit API to search for pain points
        # For now, return mock data
        return [
            "I can't seem to stay focused while working from home",
            "My productivity has dropped since switching to remote work",
            "I need help organizing my daily routine"
        ]
    
    def _analyze_viral_patterns(self, query: str) -> List[Dict]:
        """Analyze viral content patterns"""
        return [
            {"pattern": "hook + problem + solution", "effectiveness": 0.85},
            {"pattern": "before/after transformation", "effectiveness": 0.78},
            {"pattern": "social proof + testimonial", "effectiveness": 0.92}
        ]


class ScriptGenerationTool(BaseTool):
    """Tool for generating viral scripts"""
    
    name: str = "script_generation"
    description: str = "Generate viral UGC scripts based on research and product info"
    
    def _run(self, research_data: str, product_info: str, target_audience: str) -> str:
        """Generate viral scripts"""
        try:
            # Parse research data
            research = json.loads(research_data)
            
            # Generate multiple script variants
            scripts = []
            
            # Hook-focused script
            hook_script = self._generate_hook_script(research, product_info, target_audience)
            scripts.append({"type": "hook_focused", "script": hook_script})
            
            # Problem-solution script
            problem_script = self._generate_problem_script(research, product_info, target_audience)
            scripts.append({"type": "problem_solution", "script": problem_script})
            
            # Social proof script
            proof_script = self._generate_social_proof_script(research, product_info, target_audience)
            scripts.append({"type": "social_proof", "script": proof_script})
            
            return json.dumps({"scripts": scripts}, indent=2)
        except Exception as e:
            return f"Error generating scripts: {str(e)}"
    
    def _generate_hook_script(self, research: Dict, product_info: str, audience: str) -> str:
        """Generate hook-focused script"""
        # This would use OpenAI to generate the script
        # For now, return a template
        return f"""
        [HOOK] Stop struggling with {audience} problems!
        
        [PROBLEM] I used to spend hours trying to figure this out...
        
        [SOLUTION] But then I discovered {product_info} and everything changed!
        
        [PROOF] Here's what happened in just 30 days...
        
        [CTA] Click the link below to get started today!
        """
    
    def _generate_problem_script(self, research: Dict, product_info: str, audience: str) -> str:
        """Generate problem-solution script"""
        return f"""
        [PROBLEM] Are you tired of dealing with {audience} issues?
        
        [AGITATION] Every day, thousands of people struggle with this...
        
        [SOLUTION] {product_info} is the answer you've been looking for!
        
        [BENEFITS] Here's what you'll get:
        • Benefit 1
        • Benefit 2
        • Benefit 3
        
        [CTA] Don't wait - start transforming your life today!
        """
    
    def _generate_social_proof_script(self, research: Dict, product_info: str, audience: str) -> str:
        """Generate social proof script"""
        return f"""
        [STORY] I was skeptical at first, but then I tried {product_info}...
        
        [TRANSFORMATION] The results were incredible! Here's my journey:
        
        [BEFORE] Before: Struggling with {audience} problems
        
        [AFTER] After: Complete transformation in just 30 days!
        
        [PROOF] Don't just take my word for it - thousands of others agree!
        
        [CTA] Join the success story - click below!
        """


class VideoOptimizationTool(BaseTool):
    """Tool for optimizing video content"""
    
    name: str = "video_optimization"
    description: str = "Optimize video content for maximum engagement and virality"
    
    def _run(self, script: str, platform: str, target_audience: str) -> str:
        """Optimize video content"""
        try:
            optimizations = {
                "script_optimization": self._optimize_script(script, platform),
                "visual_elements": self._suggest_visual_elements(platform),
                "audio_optimization": self._optimize_audio(platform),
                "engagement_hooks": self._generate_engagement_hooks(platform),
                "cta_optimization": self._optimize_cta(platform)
            }
            
            return json.dumps(optimizations, indent=2)
        except Exception as e:
            return f"Error optimizing video: {str(e)}"
    
    def _optimize_script(self, script: str, platform: str) -> Dict:
        """Optimize script for specific platform"""
        platform_optimizations = {
            "tiktok": {
                "max_duration": "15-60 seconds",
                "hook_timing": "0-3 seconds",
                "text_overlay": "Large, bold text",
                "trending_sounds": "Use trending audio"
            },
            "instagram": {
                "max_duration": "15-60 seconds",
                "visual_focus": "High-quality visuals",
                "storytelling": "Emotional connection"
            },
            "youtube": {
                "max_duration": "30-120 seconds",
                "detailed_explanation": "More in-depth content",
                "seo_optimization": "Include keywords"
            }
        }
        
        return platform_optimizations.get(platform, {})
    
    def _suggest_visual_elements(self, platform: str) -> List[str]:
        """Suggest visual elements for platform"""
        elements = {
            "tiktok": ["Text overlays", "Trending effects", "Quick cuts", "B-roll"],
            "instagram": ["High-quality footage", "Brand colors", "Smooth transitions"],
            "youtube": ["Professional lighting", "Clear audio", "Detailed graphics"]
        }
        return elements.get(platform, [])
    
    def _optimize_audio(self, platform: str) -> Dict:
        """Optimize audio for platform"""
        return {
            "tiktok": "Use trending sounds and music",
            "instagram": "Clear voiceover with background music",
            "youtube": "Professional voiceover with high-quality audio"
        }
    
    def _generate_engagement_hooks(self, platform: str) -> List[str]:
        """Generate engagement hooks for platform"""
        hooks = [
            "Stop scrolling! This will change everything...",
            "You won't believe what happened next...",
            "The secret that nobody talks about...",
            "I tried this for 30 days and here's what happened..."
        ]
        return hooks
    
    def _optimize_cta(self, platform: str) -> str:
        """Optimize call-to-action for platform"""
        ctas = {
            "tiktok": "Click the link in bio! 🔗",
            "instagram": "Swipe up to learn more! ⬆️",
            "youtube": "Subscribe and hit the bell! 🔔"
        }
        return ctas.get(platform, "Click the link below!")


class TrendResearcherAgent(Agent):
    """Agent for researching trends and pain points"""
    
    def __init__(self):
        super().__init__(
            role="Trend Research Specialist",
            goal="Research trending topics, pain points, and viral content patterns",
            backstory="""You are an expert at identifying viral trends and understanding 
            what makes content go viral. You have years of experience analyzing social 
            media patterns and consumer behavior.""",
            tools=[TrendResearchTool()],
            verbose=True,
            allow_delegation=False
        )


class ScriptWriterAgent(Agent):
    """Agent for writing viral scripts"""
    
    def __init__(self):
        super().__init__(
            role="Viral Script Writer",
            goal="Create compelling, viral UGC scripts that drive engagement and conversions",
            backstory="""You are a master copywriter who specializes in creating viral 
            content. You understand psychology, persuasion, and what makes people take action. 
            You've helped create content that has generated millions of views and sales.""",
            tools=[ScriptGenerationTool()],
            verbose=True,
            allow_delegation=False
        )


class VideoOptimizerAgent(Agent):
    """Agent for optimizing video content"""
    
    def __init__(self):
        super().__init__(
            role="Video Optimization Specialist",
            goal="Optimize video content for maximum engagement and platform-specific performance",
            backstory="""You are an expert in video optimization and platform-specific 
            best practices. You understand what makes videos perform well on different 
            platforms and how to maximize engagement and conversions.""",
            tools=[VideoOptimizationTool()],
            verbose=True,
            allow_delegation=False
        )


class UGCContentCrew:
    """Crew for creating viral UGC content"""
    
    def __init__(self):
        self.researcher = TrendResearcherAgent()
        self.writer = ScriptWriterAgent()
        self.optimizer = VideoOptimizerAgent()
    
    def create_viral_content(self, product_info: str, target_audience: str, platform: str) -> Dict[str, Any]:
        """Create viral UGC content using the crew"""
        
        # Task 1: Research trends and pain points
        research_task = Task(
            description=f"""Research trending topics, pain points, and viral patterns related to:
            Product: {product_info}
            Target Audience: {target_audience}
            Platform: {platform}
            
            Focus on:
            1. Current trending topics in this niche
            2. Common pain points and frustrations
            3. Viral content patterns that work
            4. Competitor analysis
            """,
            agent=self.researcher,
            expected_output="Comprehensive research data in JSON format"
        )
        
        # Task 2: Generate viral scripts
        script_task = Task(
            description=f"""Using the research data, generate 3 different viral script variants:
            1. Hook-focused script
            2. Problem-solution script  
            3. Social proof script
            
            Product: {product_info}
            Target Audience: {target_audience}
            Platform: {platform}
            
            Make sure each script is optimized for the platform and includes:
            - Compelling hook
            - Clear problem statement
            - Solution presentation
            - Social proof
            - Strong call-to-action
            """,
            agent=self.writer,
            expected_output="3 script variants in JSON format",
            context=[research_task]
        )
        
        # Task 3: Optimize for platform
        optimization_task = Task(
            description=f"""Optimize the best script for {platform}:
            
            Focus on:
            1. Platform-specific best practices
            2. Visual element suggestions
            3. Audio optimization
            4. Engagement hooks
            5. CTA optimization
            
            Make the content highly engaging and optimized for virality.
            """,
            agent=self.optimizer,
            expected_output="Optimized video strategy in JSON format",
            context=[script_task]
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.optimizer],
            tasks=[research_task, script_task, optimization_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "research": result[0],
            "scripts": result[1], 
            "optimization": result[2],
            "final_content": self._compile_final_content(result)
        }
    
    def _compile_final_content(self, results: List[str]) -> Dict[str, Any]:
        """Compile final content from crew results"""
        try:
            # Parse results
            research = json.loads(results[0]) if isinstance(results[0], str) else results[0]
            scripts = json.loads(results[1]) if isinstance(results[1], str) else results[1]
            optimization = json.loads(results[2]) if isinstance(results[2], str) else results[2]
            
            return {
                "research_summary": research,
                "script_variants": scripts.get("scripts", []),
                "optimization_strategy": optimization,
                "recommended_script": scripts.get("scripts", [{}])[0] if scripts.get("scripts") else {},
                "production_notes": self._generate_production_notes(optimization)
            }
        except Exception as e:
            return {
                "error": f"Error compiling content: {str(e)}",
                "raw_results": results
            }
    
    def _generate_production_notes(self, optimization: Dict) -> List[str]:
        """Generate production notes from optimization data"""
        notes = []
        
        if "visual_elements" in optimization:
            notes.append(f"Visual Elements: {', '.join(optimization['visual_elements'])}")
        
        if "audio_optimization" in optimization:
            notes.append(f"Audio: {optimization['audio_optimization']}")
        
        if "engagement_hooks" in optimization:
            notes.append(f"Engagement Hooks: {', '.join(optimization['engagement_hooks'])}")
        
        return notes


# Global crew instance
ugc_crew = UGCContentCrew()


def generate_viral_content(product_info: str, target_audience: str, platform: str = "tiktok") -> Dict[str, Any]:
    """Generate viral UGC content using AI agents"""
    try:
        result = ugc_crew.create_viral_content(product_info, target_audience, platform)
        return result
    except Exception as e:
        return {
            "error": f"Error generating content: {str(e)}",
            "product_info": product_info,
            "target_audience": target_audience,
            "platform": platform
        }


def generate_script_variants(product_info: str, target_audience: str, count: int = 5) -> List[Dict]:
    """Generate multiple script variants using real OpenAI GPT-4"""
    try:
        # Use real OpenAI service
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If event loop is already running, create a new task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    openai_service.generate_viral_script(
                        product_info=product_info,
                        target_audience=target_audience,
                        platform="tiktok",
                        count=count
                    )
                )
                result = future.result()
        else:
            # Run directly if no event loop
            result = loop.run_until_complete(
                openai_service.generate_viral_script(
                    product_info=product_info,
                    target_audience=target_audience,
                    platform="tiktok",
                    count=count
                )
            )

        if result.get("success"):
            return result.get("scripts", [])
        else:
            # Fallback to mock if OpenAI fails
            return result.get("scripts", [{"error": result.get("error", "Unknown error")}])

    except Exception as e:
        return [{"error": f"Error generating scripts: {str(e)}"}]