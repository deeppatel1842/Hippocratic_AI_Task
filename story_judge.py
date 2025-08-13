from openai_client import OpenAIClient
import textstat
from typing import Dict
from config_loader import config

class StoryJudge:
    """Evaluates story quality using LLM judge and automated metrics"""
    
    def __init__(self):
        self.client = OpenAIClient()
        self.safety_filters = config.get_safety_filters()
        self.quality_thresholds = config.get_quality_thresholds()
        self.vocabulary_settings = config.get_vocabulary_settings()
        self.age_level_scoring = config.get_age_level_scoring()
        self.composite_weights = config.get_composite_weights()
        self.default_llm_scores = config.get_default_llm_scores()
    
    def analyze_metrics(self, story: str) -> Dict:
        """Calculate automated story metrics"""
        words = story.split()
        unique_words = set(word.lower() for word in words)
        
        return {
            "word_count": len(words),
            "grade_level": textstat.flesch_kincaid_grade(story),
            "vocabulary_richness": (len(unique_words) / len(words)) * 100,
            "predictability": self._calculate_predictability(story),
            "safety": self._check_safety(story)
        }
    
    def _calculate_predictability(self, story: str) -> float:
        """Calculate how predictable/calming the story is"""
        calming_words = self.safety_filters["calming_words"]
        story_lower = story.lower()
        found_words = sum(1 for word in calming_words if word in story_lower)
        return min((found_words / len(calming_words)) * 100, 100)
    
    def _check_safety(self, story: str) -> float:
        """Check content safety for bedtime stories"""
        unsafe_words = self.safety_filters["unsafe_words"]
        story_lower = story.lower()
        unsafe_count = sum(1 for word in unsafe_words if word in story_lower)
        penalty_per_word = self.safety_filters["safety_penalty_per_word"]
        return max(100 - (unsafe_count * penalty_per_word), 0)
    
    def get_llm_judgment(self, story: str) -> Dict:
        """Get LLM evaluation of story quality"""
        prompt = f"""
            Rate this bedtime story for children ages 5-10 (0-100 each):

            Story: {story}

            Rate these aspects:
            1. Age Appropriateness
            2. Bedtime Suitability
            3. Story Structure
            4. Engagement
            5. Originality
            6. Educational Value

            Respond with only numbers separated by commas in this order.
            """
        
        try:
            openai_settings = config.get_openai_settings()
            response = self.client.call_model(
                prompt, 
                max_tokens=openai_settings["judge_max_tokens"], 
                temperature=openai_settings["judge_temperature"]
            )
            scores = [float(x.strip()) for x in response.split(',')]
            
            if len(scores) == 6:
                return {
                    "age_appropriateness": scores[0],
                    "bedtime_suitability": scores[1],
                    "story_structure": scores[2],
                    "engagement": scores[3],
                    "originality": scores[4],
                    "educational_value": scores[5]
                }
        except:
            pass
        
        # Default scores if LLM fails
        return self.default_llm_scores.copy()
    
    def judge_story(self, story: str) -> Dict:
        """Complete story evaluation"""
        metrics = self.analyze_metrics(story)
        llm_scores = self.get_llm_judgment(story)
        
        overall_score = sum(llm_scores.values()) / len(llm_scores)
        
        # Component breakdown for composite score
        target_grade = self.age_level_scoring["target_grade"]
        penalty_per_diff = self.age_level_scoring["penalty_per_grade_diff"]
        min_age_score = self.age_level_scoring["min_age_score"]
        max_age_score = self.age_level_scoring["max_age_score"]
        
        age_level_score = max_age_score if self.quality_thresholds["min_reading_level"] <= metrics["grade_level"] <= self.quality_thresholds["max_reading_level"] else max(min_age_score, max_age_score - abs(metrics["grade_level"] - target_grade) * penalty_per_diff)
        
        vocabulary_score = min(
            metrics["vocabulary_richness"] * self.vocabulary_settings["richness_multiplier"], 
            self.vocabulary_settings["max_vocabulary_score"]
        )
        
        composite_score = (
            metrics["predictability"] * self.composite_weights["predictability"] +
            vocabulary_score * self.composite_weights["vocabulary"] +
            age_level_score * self.composite_weights["age_level"] +
            metrics["safety"] * self.composite_weights["safety"]
        )
        
        return {
            "llm_judge": llm_scores,
            "overall_score": overall_score,
            "metrics": metrics,
            "composite_score": composite_score,
            "component_breakdown": {
                "predictability": metrics["predictability"],
                "vocabulary": vocabulary_score,
                "age_level": age_level_score,
                "safety": metrics["safety"]
            }
        }
