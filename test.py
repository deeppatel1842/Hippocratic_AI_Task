import sys
import os
sys.path.append(os.getcwd())

from story_teller import StoryTeller
from story_judge import StoryJudge
from config_loader import config

def test_prompt(prompt_text, prompt_name):
    storyteller = StoryTeller()
    judge = StoryJudge()
    
    print(f"\n{'='*80}")
    print(f"TESTING: {prompt_name}")
    print(f"PROMPT: {prompt_text}")
    print(f"{'='*80}")
    
    try:
        # Generate story
        story, category = storyteller.generate_story(prompt_text)
        print(f"\nStory Category: {category.title()}")
        
        # Evaluate story
        evaluation = judge.evaluate_story(story)
        
        # Get thresholds from config
        quality_thresholds = config.get_quality_thresholds()
        story_settings = config.get_story_settings()
        
        # Check if improvement needed using config values
        if (evaluation["composite_score"] < quality_thresholds["min_composite_score"] or 
            evaluation["metrics"]["word_count"] < story_settings["min_word_count"] or 
            evaluation["metrics"]["word_count"] > story_settings["max_word_count"] or
            evaluation["metrics"]["grade_level"] > story_settings["max_grade_level"] or
            evaluation["metrics"]["grade_level"] < story_settings["min_grade_level"]):
            
            print("Improving story based on evaluation...")
            story = storyteller.improve_story(story, evaluation)
            evaluation = judge.evaluate_story(story)
        
        # Print story
        print(f"\n{'-'*60}")
        print("YOUR BEDTIME STORY")
        print(f"{'-'*60}")
        print(story)
        
        # Print evaluation
        print(f"\n{'-'*60}")
        print("BEDTIME STORY EVALUATION")
        print(f"{'-'*60}")
        print(f"\nStory Category: {category.title()}")
        print("\nLLM Judge Evaluation:")
        for key, value in evaluation["llm_judge"].items():
            formatted_key = key.replace("_", " ").title()
            print(f"   {formatted_key}: {value:.0f}/100")
        
        print(f"\nOverall Score: {evaluation['overall_score']:.0f}/100")
        
        quality_thresholds = config.get_quality_thresholds()
        composite_rating = "Excellent" if evaluation["composite_score"] >= 90 else \
                          "Very Good" if evaluation["composite_score"] >= quality_thresholds["min_composite_score"] + 10 else \
                          "Good" if evaluation["composite_score"] >= quality_thresholds["min_composite_score"] else \
                          "Needs Improvement"
        
        print(f"Comprehensive Metrics ({composite_rating}):")
        print(f"   Text predictability: {evaluation['metrics']['predictability']:.1f}/100")
        print(f"   Vocabulary richness: {evaluation['metrics']['vocabulary_richness']:.1f}%")
        print(f"   Reading level: Grade {evaluation['metrics']['grade_level']:.2f}")
        print(f"   Content safety: {evaluation['metrics']['safety']:.1f}/100")
        print(f"   Composite Score: {evaluation['composite_score']:.1f}/100")

        story_settings = config.get_story_settings()
        print(f"\nStory Length: {evaluation['metrics']['word_count']} words (target: {story_settings['min_word_count']}-{story_settings['max_word_count']})")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

def main():
    # Easy Level Prompts
    easy_prompts = [
        "A story about a sleepy cat.",
        "A friendly dog who likes to play.",
        "Tell me about a little bird learning to fly.",
        "A story about a bear getting ready for bed.",
        "A rabbit who finds a carrot in the garden."
    ]
    
    # Medium Level Prompts
    medium_prompts = [
        "Tell me a story about a brave lion who helps other animals in the forest.",
        "Create a story about a little girl who finds a magical garden.",
        "Write a story about two best friends who help a lost puppy find its way home.",
        "Tell me about a family that bakes cookies together on a rainy day.",
        "A story about a curious child who learns about butterflies in the garden."
    ]
    
    # Hard Level Prompts
    hard_prompts = [
        "Tell me an adventure story about a young boy who discovers a hidden cave with sparkling crystals and meets a friendly dragon who teaches him about courage and kindness.",
        "Create a magical story about three animal friends who must work together to save their enchanted forest home from losing its magic, learning about teamwork and the power of friendship along the way.",
        "Write a story about a little girl who finds a mysterious music box that transports her to different lands where she meets talking animals and helps them solve problems while learning valuable life lessons."
    ]
    
    print("BEDTIME STORY GENERATOR - COMPREHENSIVE TEST RESULTS")
    print("="*80)
    
    # Test Easy Level
    print(f"\n{'#'*80}")
    print("EASY LEVEL PROMPTS")
    print(f"{'#'*80}")
    
    for i, prompt in enumerate(easy_prompts, 1):
        test_prompt(prompt, f"Easy Level {i}")
    
    # Test Medium Level
    print(f"\n{'#'*80}")
    print("MEDIUM LEVEL PROMPTS")
    print(f"{'#'*80}")
    
    for i, prompt in enumerate(medium_prompts, 1):
        test_prompt(prompt, f"Medium Level {i}")
    
    # Test Hard Level
    print(f"\n{'#'*80}")
    print("HARD LEVEL PROMPTS")
    print(f"{'#'*80}")
    
    for i, prompt in enumerate(hard_prompts, 1):
        test_prompt(prompt, f"Hard Level {i}")

if __name__ == "__main__":
    main()
