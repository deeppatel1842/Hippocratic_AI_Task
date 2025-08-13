import json
import os
from typing import Dict, Any

class ConfigLoader:
    """Loads and manages configuration from JSON file"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), self.config_file)
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'story_evaluation.default_llm_scores')"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise KeyError(f"Configuration key '{key_path}' not found")
    
    def get_default_llm_scores(self) -> Dict[str, float]:
        """Get default LLM scores"""
        return self.get('story_evaluation.default_llm_scores')
    
    def get_composite_weights(self) -> Dict[str, float]:
        """Get composite score weights"""
        return self.get('story_evaluation.composite_score_weights')
    
    def get_quality_thresholds(self) -> Dict[str, float]:
        """Get quality thresholds"""
        return self.get('story_evaluation.quality_thresholds')
    
    def get_vocabulary_settings(self) -> Dict[str, float]:
        """Get vocabulary settings"""
        return self.get('story_evaluation.vocabulary_settings')
    
    def get_age_level_scoring(self) -> Dict[str, float]:
        """Get age level scoring settings"""
        return self.get('story_evaluation.age_level_scoring')
    
    def get_story_categories(self) -> Dict[str, Dict]:
        """Get story categories configuration"""
        return self.get('story_categories')
    
    def get_safety_filters(self) -> Dict[str, Any]:
        """Get safety filter settings"""
        return self.get('safety_filters')
    
    def get_openai_settings(self) -> Dict[str, Any]:
        """Get OpenAI API settings"""
        return self.get('openai_settings')
    
    def get_story_generation_settings(self) -> Dict[str, str]:
        """Get story generation settings"""
        return self.get('story_generation')
    
    def get_story_settings(self) -> Dict[str, Any]:
        """Get story generation settings"""
        return self.get('story_settings')
    
    def get_display_settings(self) -> Dict[str, Any]:
        """Get display settings"""
        return self.get('display_settings')

# Global configuration instance
config = ConfigLoader()
