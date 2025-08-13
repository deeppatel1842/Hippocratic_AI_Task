# Bedtime Story Generator - AI-Powered Stories for Kids

Welcome to the Bedtime Story Generator! This is an intelligent system that creates personalized, safe, and engaging bedtime stories for children ages 5-10. What makes this special? Everything is automated through smart configuration - no hardcoded values, just pure adaptability.

## What Makes This Special

I built this system to solve a real problem: how do you create consistently good bedtime stories that are always age-appropriate, safe, and engaging? The answer was automation through intelligent configuration.

###  Key Features

- **Fully Automated Quality Control**: Every story is automatically evaluated for safety, reading level, and appropriateness
- **Smart Story Categorization**: Just describe what you want - the system automatically figures out the best approach
- **Zero Hardcoded Values**: Everything is configurable through JSON - want stricter quality? Just change a number
- **Interactive Feedback System**: Don't like something? Tell the system and it will adjust the story
- **Comprehensive Safety**: Multiple layers of content filtering ensure stories are always appropriate


## How It Works

When you run the program, you'll see helpful examples like these:

### Example Story Requests You Can Try:
- "Tell me a story about a brave lion who helps other animals in the forest"
- "Create a story about a little girl who finds a magical garden"  
- "Write a story about two best friends who help a lost puppy find its way home"
- "A sleepy cat getting ready for bed"
- Or simply type: "animals", "magic", "adventure"

### What Happens Next:
1. **Smart Detection**: The system automatically categorizes your request
2. **Story Generation**: Creates a story tailored to your request
3. **Quality Check**: Automatically evaluates the story on multiple criteria
4. **Your Choice**: Keep it, modify it, or generate a new one

## The Magic Behind the Scenes

### Automated Configuration System

Everything in this system is controlled by the `config.json` file. Want to change how it works? Just edit the configuration:

```json
{
  "story_settings": {
    "min_word_count": 250,
    "max_word_count": 500,
    "min_grade_level": 3.0,
    "max_grade_level": 6.5
  },
  "quality_thresholds": {
    "min_composite_score": 70,
    "min_safety_score": 80
  }
}
```

### Quality Evaluation (Completely Automated)

Every story is automatically checked for:

- **Reading Level**: Ensures Grade 43.0-5.5 difficulty
- **Word Count**: Maintains 250-500 word stories  
- **Safety Score**: Filters any inappropriate content
- **Story Structure**: Checks for beginning, middle, end
- **Age Appropriateness**: Validates content for 5-10 year olds
- **Bedtime Suitability**: Ensures calming, sleep-friendly themes

## 📁 System Architecture

### Comprehensive Block Diagram

```
                            ┌─────────────────────────────────────────────────────┐
                            │                 USER REQUEST                        │
                            │              "magical garden story"                 │
                            └─────────────────────┬───────────────────────────────┘
                                                  │
                            ┌─────────────────────▼───────────────────────────────┐
                            │              CONFIG LOADER                          │
                            │         • Loads all settings from JSON             │
                            │         • Story categories & keywords              │
                            │         • Quality thresholds                       │
                            │         • No hardcoded values!                     │
                            └─────────────────────┬───────────────────────────────┘
                                                  │
                            ┌─────────────────────▼───────────────────────────────┐
                            │           STORY CATEGORIZATION                      │
                            │      • Keyword matching algorithm                  │
                            │      • Automatic category detection                │
                            │      • Tailored prompt selection                   │
                            └─────────────────────┬───────────────────────────────┘
                                                  │
                                    ┌─────────────▼─────────────┐
                                    │     CATEGORY: MAGIC       │
                                    │   Strategy: "soft magic   │
                                    │   and wonder without fear" │
                                    └─────────────┬─────────────┘
                                                  │
                            ┌─────────────────────▼───────────────────────────────┐
                            │              STORY GENERATION                       │
                            │           • GPT-3.5-turbo API call                 │
                            │           • Dynamic prompt creation                 │
                            │           • Config-driven parameters               │
                            │           • Word count: 350-500 words              │
                            └─────────────────────┬───────────────────────────────┘
                                                  │
                            ┌─────────────────────▼───────────────────────────────┐
                            │                GENERATED STORY                      │
                            │        "Luna's Magical Garden Adventure..."        │
                            └─────────────────────┬───────────────────────────────┘
                                                  │
                    ┌─────────────────────────────▼─────────────────────────────┐
                    │                    DUAL QUALITY EVALUATION                │
                    └─────────────────────┬─────────────────┬─────────────────────┘
                                          │                 │
                    ┌─────────────────────▼──────────┐     ┌▼─────────────────────────┐
                    │     AUTOMATED METRICS          │     │     LLM JUDGE            │
                    │  • Word count: 387 ✓           │     │  • Age appropriateness   │
                    │  • Reading level: 4.8 ✓        │     │  • Bedtime suitability   │
                    │  • Safety check: 95/100 ✓      │     │  • Story structure       │
                    │  • Vocabulary richness: 82%    │     │  • Engagement level      │
                    └─────────────────────┬──────────┘     └┬─────────────────────────┘
                                          │                 │
                    ┌─────────────────────▼─────────────────▼─────────────────────────┐
                    │                 COMPOSITE SCORING                               │
                    │        • Combines all metrics using config weights             │
                    │        • Overall Score: 87/100 (Above 70 threshold)            │
                    │        • Rating: "Very Good"                                   │
                    └─────────────────────┬───────────────────────────────────────────┘
                                          │
                            ┌─────────────▼───────────────────────────────┐
                            │            QUALITY DECISION                 │
                            │     Score ≥ Threshold? YES → APPROVED       │
                            └─────────────┬───────────────────────────────┘
                                          │
                            ┌─────────────▼───────────────────────────────┐
                            │            STORY DISPLAY                    │
                            │     • Show story to user                    │
                            │     • Display evaluation metrics            │
                            │     • Present feedback options              │
                            └─────────────┬───────────────────────────────┘
                                          │
                            ┌─────────────▼───────────────────────────────┐
                            │            USER FEEDBACK                    │
                            │   1. I love it! (keep as is)               │
                            │   2. Make it longer/shorter                 │
                            │   3. Make it more exciting/calmer           │
                            │   4. Add characters/change setting          │
                            │   5. Custom feedback                        │
                            │   6. Generate new story                     │
                            └─────────────┬───────────────────────────────┘
                                          │
                    ┌─────────────────────▼─────────────────────────────────────┐
                    │                 FEEDBACK PROCESSING                       │
                    └┬────────────────────────────────────────────────────────┬─┘
                     │                                                        │
    ┌────────────────▼──────────┐                              ┌──────────────▼────────────┐
    │    STORY MODIFICATION     │                              │     NEW STORY REQUEST     │
    │  • Apply user feedback    │                              │   • Generate completely   │
    │  • Maintain story essence │                              │     new story             │
    │  • Re-evaluate quality    │                              │   • Return to category    │
    └────────────────┬──────────┘                              │     detection             │
                     │                                         └───────────────────────────┘
    ┌────────────────▼──────────┐                                           │
    │    CONTINUE/EXIT          │◄──────────────────────────────────────────┘
    │  • Another story?         │
    │  • Modify current?        │
    │  • Quit program?          │
    └───────────────────────────┘
```

### File Structure
```
hippocriptic.ai/
├── main.py              # Main application with example prompts
├── story_teller.py      # Story generation and categorization  
├── story_judge.py       # Automated quality evaluation
├── openai_client.py     # API communication
├── config_loader.py     # Configuration management
├── config.json          # All system settings (no hardcoded values!)
├── test.py              # Comprehensive testing with examples
└── README.md            # This file
```

## 🎭 Real Examples

Here's what the system actually produces:

### Example 1: Animal Story
**Your Request**: "Tell me about a brave rabbit"

**System Response**: 
```
Story Category: Animals
Generating your bedtime story...

YOUR BEDTIME STORY
============================================================

Luna the Little Rabbit and the Moonbeam Adventure

Once upon a time, in a peaceful meadow surrounded by tall oak trees, 
lived a small rabbit named Luna. She had the softest gray fur and the 
brightest brown eyes in the entire meadow...

[387-word story follows]

BEDTIME STORY EVALUATION  
============================================================
Overall Score: 87/100
Rating: Very Good

Comprehensive Metrics:
• Text predictability: 78.5/100
• Vocabulary richness: 82.3%  
• Reading level: Grade 4.8
• Content safety: 95.0/100
• Story Length: 387 words (target: 350-500)
```


