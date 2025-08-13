from openai_client import OpenAIClient
from typing import Dict
from config_loader import config

class StoryTeller:
    """Generates bedtime stories with category-based prompting"""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.categories = config.get_story_categories()
        self.generation_settings = config.get_story_generation_settings()
        self.quality_thresholds = config.get_quality_thresholds()
    
    def categorize_request(self, user_input: str) -> str:
        """Categorize story request based on keywords"""
        user_lower = user_input.lower()
        for category, category_config in self.categories.items():
            keywords = category_config["keywords"]
            if any(keyword in user_lower for keyword in keywords):
                return category
        return "general"
    
    def create_prompt(self, user_input: str, category: str) -> str:
        """Create category-specific story prompt"""
        min_words = self.quality_thresholds["min_word_count"]
        max_words = self.quality_thresholds["max_word_count"]
        min_reading = self.quality_thresholds["min_reading_level"]
        max_reading = self.quality_thresholds["max_reading_level"]
        
        # Get category strategy or default
        if category in self.categories:
            category_strategy = self.categories[category]["prompt_strategy"]
        else:
            category_strategy = "warm, comforting universal story"
        
        # Use template from config
        base_prompt = self.generation_settings["base_prompt_template"].format(
            word_count=f"{min_words}-{max_words}",
            min_reading_level=min_reading,
            max_reading_level=max_reading,
            category_strategy=category_strategy
        )
        
        return f"""
        {base_prompt}

        User request: {user_input}

        Additional requirements:
        - Simple vocabulary appropriate for bedtime
        - Clear beginning, middle, and end
        - Positive, uplifting message
        - No scary or disturbing content
        - Include soothing, calming elements

        Write the complete story now:
        """
    
    def generate_story(self, user_input: str) -> tuple:
        """Generate story and return (story, category)"""
        category = self.categorize_request(user_input)
        prompt = self.create_prompt(user_input, category)
        story = self.client.call_model(prompt)
        return story.strip(), category
    
    def improve_story(self, story: str, feedback: Dict) -> str:
        """Improve story based on evaluation feedback"""
        improvements = []
        
        min_words = self.quality_thresholds["min_word_count"]
        max_words = self.quality_thresholds["max_word_count"]
        max_reading = self.quality_thresholds["max_reading_level"]
        min_bedtime_score = self.quality_thresholds["min_safety_score"]
        
        if feedback["metrics"]["word_count"] < min_words:
            improvements.append(f"expand to {min_words}-{max_words} words with more details")
        
        if feedback["metrics"]["grade_level"] > max_reading:
            improvements.append(f"use simpler vocabulary for Grade {self.quality_thresholds['min_reading_level']}-{max_reading}")
        
        if feedback["llm_judge"]["bedtime_suitability"] < min_bedtime_score:
            improvements.append("make more calming and bedtime suitable")
        
        if not improvements:
            return story

        improvement_feedback = '; '.join(improvements)
        improvement_prompt = self.generation_settings["improvement_prompt_template"].format(
            feedback=improvement_feedback
        )
        
        full_prompt = f"""
        {improvement_prompt}

        Requirements:
        - {self.quality_thresholds['min_word_count']}-{self.quality_thresholds['max_word_count']} words
        - Grade {self.quality_thresholds['min_reading_level']}-{self.quality_thresholds['max_reading_level']} reading level
        - Calming and peaceful

        Original story:
        {story}

        Improved story:
        """
        
        openai_settings = config.get_openai_settings()
        return self.client.call_model(
            full_prompt, 
            temperature=openai_settings["temperature"] - 0.2  # Slightly lower for improvements
        )
    
    def modify_story_with_feedback(self, story: str, feedback: str, category: str) -> str:
        """Modify story based on user feedback"""
        # Get category strategy for context
        if category in self.categories:
            category_strategy = self.categories[category]["prompt_strategy"]
            context = f"while maintaining the {category_strategy}"
        else:
            context = "while maintaining the story's essence"
        
        modification_prompt = self.generation_settings["modification_prompt_template"].format(
            user_feedback=feedback
        )
        
        full_prompt = f"""
        {modification_prompt}

        Modification context: {context}

        Requirements:
        - Keep it appropriate for ages 5-10
        - {self.quality_thresholds['min_word_count']}-{self.quality_thresholds['max_word_count']} words
        - Grade {self.quality_thresholds['min_reading_level']}-{self.quality_thresholds['max_reading_level']} reading level
        - Calming and peaceful for bedtime

        Original story:
        {story}

        Modified story:
        """
        
        openai_settings = config.get_openai_settings()
        return self.client.call_model(
            full_prompt, 
            temperature=openai_settings["temperature"]
        )
