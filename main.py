from story_teller import StoryTeller
from story_judge import StoryJudge
from config_loader import config

def print_evaluation(evaluation: dict, category: str):
    """Display story evaluation results"""
    display_settings = config.get_display_settings()
    
    if not display_settings["show_detailed_metrics"]:
        # Simple display
        print(f"\nStory Category: {category.title()}")
        print(f"Overall Score: {evaluation['overall_score']:.0f}/100")
        return
    
    print("\n" + "="*60)
    print("BEDTIME STORY EVALUATION")
    print("="*60)
    
    print(f"\nStory Category: {category.title()}")
    
    print("\nLLM Judge Evaluation:")
    for key, value in evaluation["llm_judge"].items():
        formatted_key = key.replace("_", " ").title()
        print(f"   {formatted_key}: {value:.0f}/100")
    
    print(f"\nOverall Score: {evaluation['overall_score']:.0f}/100")
    
    quality_thresholds = config.get_quality_thresholds()
    quality_thresholds = config.get_quality_thresholds()
    rating = ("Excellent" if evaluation["composite_score"] >= 90 else
              "Very Good" if evaluation["composite_score"] >= quality_thresholds["min_composite_score"] + 10 else
              "Good" if evaluation["composite_score"] >= quality_thresholds["min_composite_score"] else
              "Needs Improvement")
    
    print(f"Comprehensive Metrics ({rating}):")
    print(f"   • Text predictability: {evaluation['metrics']['predictability']:.1f}/100")
    print(f"   • Vocabulary richness: {evaluation['metrics']['vocabulary_richness']:.1f}%")
    print(f"   • Reading level: Grade {evaluation['metrics']['grade_level']:.2f}")
    print(f"   • Content safety: {evaluation['metrics']['safety']:.1f}/100")
    print(f"   • Composite Score: {evaluation['composite_score']:.1f}/100")
    
    story_settings = config.get_story_settings()
    print(f"\nStory Length: {evaluation['metrics']['word_count']} words (target: {story_settings['min_word_count']}-{story_settings['max_word_count']})")
    print("="*60)

def needs_improvement(evaluation: dict) -> bool:
    """Check if story needs improvement"""
    quality_thresholds = config.get_quality_thresholds()
    story_settings = config.get_story_settings()
    
    return (evaluation["composite_score"] < quality_thresholds["min_composite_score"] or 
            evaluation["metrics"]["word_count"] < story_settings["min_word_count"] or 
            evaluation["metrics"]["word_count"] > story_settings["max_word_count"] or
            evaluation["metrics"]["grade_level"] > story_settings["max_grade_level"] or
            evaluation["metrics"]["grade_level"] < story_settings["min_grade_level"])

def get_user_feedback(story: str, category: str):
    """Get user feedback on the generated story"""
    print("\n" + "="*60)
    print("STORY FEEDBACK OPTIONS")
    print("="*60)
    print("1. I love it! (keep as is)")
    print("2. Make it longer")
    print("3. Make it shorter") 
    print("4. Make it more exciting")
    print("5. Make it calmer/gentler")
    print("6. Add more characters")
    print("7. Change the setting")
    print("8. Custom feedback (describe what you'd like changed)")
    print("9. Generate a completely new story")
    
    while True:
        choice = input("\nYour choice (1-9): ").strip()
        
        if choice == "1":
            return None, "keep"
        elif choice == "2":
            return "Please make this story longer with more details and description.", "modify"
        elif choice == "3":
            return "Please make this story shorter and more concise.", "modify"
        elif choice == "4":
            return "Please make this story more exciting with more adventure and action.", "modify"
        elif choice == "5":
            return "Please make this story calmer and more gentle for bedtime.", "modify"
        elif choice == "6":
            return "Please add more characters to make the story more interesting.", "modify"
        elif choice == "7":
            return "Please change the setting to somewhere different and interesting.", "modify"
        elif choice == "8":
            custom_feedback = input("What would you like me to change about the story? ")
            return custom_feedback, "modify"
        elif choice == "9":
            return None, "regenerate"
        else:
            print("Please enter a number between 1-9.")

def main():
    """Main application loop"""
    storyteller = StoryTeller()
    judge = StoryJudge()
    
    print("Welcome to the Bedtime Story Generator for Ages 5-10!")
    print("I create personalized bedtime stories with quality evaluation.")
    print("You can provide feedback to improve any story!")
    print("Type 'quit' to exit the program.\n")
    
    # Show available story categories and examples
    categories = config.get_story_categories()
    print("Available story types:")
    for category, details in categories.items():
        sample_keywords = details['keywords'][:3]  # Show first 3 keywords as examples
        print(f"  • {category.title()}: {', '.join(sample_keywords)}, and more...")
    
    print("\nExample story requests you can try:")
    print("  • 'Tell me a story about a brave lion who helps other animals in the forest'")
    print("  • 'Create a story about a little girl who finds a magical garden'")
    print("  • 'Write a story about two best friends who help a lost puppy find its way home'")
    print("  • 'Tell me about a family that bakes cookies together on a rainy day'")
    print("  • 'A story about a curious child who learns about butterflies in the garden'")
    print("  • 'A sleepy cat getting ready for bed'")
    print("  • 'A friendly dog who likes to play'")
    print("  • Or simply type: 'animals', 'magic', 'adventure', 'family', 'nature', 'learning'\n")
    
    while True:
        user_input = input("What kind of story would you like to hear? ")
        
        if user_input.lower().strip() == 'quit':
            print("Thank you for using the Bedtime Story Generator! Sweet dreams!")
            break
        
        # Story generation and improvement loop
        story_approved = False
        while not story_approved:
            print("\nGenerating your bedtime story...")
            story, category = storyteller.generate_story(user_input)
            
            print(f"Story Category: {category.title()}")
            print("\nEvaluating story quality...")
            evaluation = judge.judge_story(story)
            
            if needs_improvement(evaluation):
                print("Improving story based on evaluation...")
                story = storyteller.improve_story(story, evaluation)
                evaluation = judge.judge_story(story)
            
            print("\n" + "="*60)
            print("YOUR BEDTIME STORY")
            print("="*60)
            print(story)
            
            print_evaluation(evaluation, category)
            
            # Get user feedback
            feedback, action = get_user_feedback(story, category)
            
            if action == "keep":
                story_approved = True
                print("\n Great! Glad you enjoyed your story!")
            elif action == "regenerate":
                print("\n Let's create a completely new story...")
                continue
            elif action == "modify":
                print(f"\n Modifying story based on your feedback...")
                story = storyteller.modify_story_with_feedback(story, feedback, category)
                print("\n" + "="*60)
                print("MODIFIED STORY")
                print("="*60)
                print(story)
                
                # Re-evaluate modified story
                evaluation = judge.judge_story(story)
                print_evaluation(evaluation, category)
                
                # Ask if they're satisfied with the changes
                satisfied = input("\nAre you happy with these changes? (yes/no): ").lower().strip()
                if satisfied in ['yes', 'y']:
                    story_approved = True
                    print("\n Perfect! Enjoy your customized bedtime story!")
                else:
                    print("\n Let's try different changes...")
        
        print("\n" + "="*60)
        print("READY FOR ANOTHER STORY!")
        print("="*60 + "\n")

if __name__ == "__main__":
    main()
