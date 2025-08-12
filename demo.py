#!/usr/bin/env python3
"""
Demo script showing different customization options for the sentiment analyzer.

This script demonstrates how to:
1. Analyze different topics
2. Use different subreddits
3. Analyze custom text data
4. Create specific visualizations

Usage:
    python demo.py
"""

import pandas as pd
from web_scraper import WebScraper
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer

def demo_custom_topic():
    """Demo: Analyze sentiment about a different topic"""
    print("🎯 Demo 1: Analyzing sentiment about 'climate change'")
    print("=" * 50)
    
    scraper = WebScraper()
    analyzer = SentimentAnalyzer()
    
    # Create sample data about climate change
    climate_texts = [
        "Climate change is the most urgent crisis of our time. We need immediate action!",
        "I'm skeptical about climate change. The science isn't settled yet.",
        "Renewable energy is becoming more affordable and efficient every year.",
        "The latest climate report shows alarming trends in global temperatures.",
        "Electric vehicles are a step in the right direction for reducing emissions.",
        "Climate policies are hurting the economy and killing jobs.",
        "We need to invest more in green technology and sustainable practices.",
        "The climate activists are being too alarmist about everything.",
        "Solar and wind power are now cheaper than fossil fuels in many regions.",
        "Climate change is a natural cycle that has happened before in history."
    ]
    
    # Create DataFrame
    data = []
    for i, text in enumerate(climate_texts):
        data.append({
            'title': f'Climate Post {i+1}',
            'text': text,
            'combined_text': text,
            'score': '',
            'timestamp': pd.Timestamp.now(),
            'source': 'demo',
            'topic': 'climate change'
        })
    
    df = pd.DataFrame(data)
    df['cleaned_text'] = df['combined_text'].apply(scraper.clean_text)
    
    # Analyze sentiment
    df_with_sentiment = analyzer.analyze_batch(df)
    
    # Show results
    summary = analyzer.get_sentiment_summary(df_with_sentiment)
    dist = summary['sentiment_distribution']
    
    print(f"Climate Change Sentiment Analysis:")
    print(f"Positive: {dist['positive']} ({dist['positive_pct']:.1f}%)")
    print(f"Negative: {dist['negative']} ({dist['negative_pct']:.1f}%)")
    print(f"Neutral: {dist['neutral']} ({dist['neutral_pct']:.1f}%)")
    print()

def demo_custom_visualization():
    """Demo: Create specific visualizations"""
    print("📊 Demo 2: Creating custom visualizations")
    print("=" * 50)
    
    analyzer = SentimentAnalyzer()
    visualizer = SentimentVisualizer()
    
    # Create sample data with varied sentiments
    mixed_texts = [
        "I absolutely love this new technology! It's fantastic!",
        "This is terrible. I hate how complicated everything is.",
        "The weather is okay today, nothing special.",
        "Amazing breakthrough in science! This will change everything!",
        "I'm really disappointed with the service quality.",
        "The presentation was informative and well-structured.",
        "This is the worst experience I've ever had!",
        "Pretty good results, could be better though.",
        "Outstanding performance! Exceeded all my expectations!",
        "Not impressed at all. Very mediocre quality."
    ]
    
    # Create DataFrame
    data = []
    for i, text in enumerate(mixed_texts):
        data.append({
            'cleaned_text': text,
            'timestamp': pd.Timestamp.now()
        })
    
    df = pd.DataFrame(data)
    
    # Analyze sentiment
    df_with_sentiment = analyzer.analyze_batch(df)
    
    # Create only specific visualizations
    print("Creating sentiment distribution plot...")
    visualizer.plot_sentiment_distribution(df_with_sentiment, save_path="demo_distribution.png")
    
    print("Creating sentiment scores distribution...")
    visualizer.plot_sentiment_scores_distribution(df_with_sentiment, save_path="demo_scores.png")
    
    print("Custom visualizations saved as demo_*.png")
    print()

def demo_analyze_custom_data():
    """Demo: Analyze your own text data"""
    print("📝 Demo 3: Analyzing custom text data")
    print("=" * 50)
    
    # You can replace this with your own text data
    your_texts = [
        "Enter your own text here for analysis",
        "Add as many texts as you want to analyze",
        "The sentiment analyzer will process all of them",
        "You can analyze reviews, comments, surveys, etc.",
        "This is a flexible tool for any text analysis needs"
    ]
    
    analyzer = SentimentAnalyzer()
    
    # Analyze each text individually
    print("Individual sentiment analysis:")
    for i, text in enumerate(your_texts):
        textblob_result = analyzer.analyze_textblob_sentiment(text)
        vader_result = analyzer.analyze_vader_sentiment(text)
        
        print(f"\nText {i+1}: \"{text[:50]}...\"")
        print(f"  TextBlob: {textblob_result['textblob_sentiment']} (polarity: {textblob_result['textblob_polarity']:.3f})")
        print(f"  VADER: {vader_result['vader_sentiment']} (compound: {vader_result['vader_compound']:.3f})")

def demo_compare_methods():
    """Demo: Compare TextBlob vs VADER performance"""
    print("⚔️ Demo 4: Comparing TextBlob vs VADER")
    print("=" * 50)
    
    # Test texts with clear sentiments
    test_cases = [
        ("I love this so much! It's absolutely amazing!", "positive"),
        ("This is terrible and I hate it completely.", "negative"),
        ("The weather is fine today.", "neutral"),
        ("OMG this is AWESOME!!! 😍❤️", "positive"),
        ("Ugh, this sucks badly 😠", "negative"),
        ("It's okay, I guess. Not bad, not great.", "neutral")
    ]
    
    analyzer = SentimentAnalyzer()
    
    print("Comparing sentiment analysis methods:")
    print("-" * 70)
    print(f"{'Text':<40} {'Expected':<10} {'TextBlob':<10} {'VADER':<10}")
    print("-" * 70)
    
    textblob_correct = 0
    vader_correct = 0
    
    for text, expected in test_cases:
        tb_result = analyzer.analyze_textblob_sentiment(text)
        vader_result = analyzer.analyze_vader_sentiment(text)
        
        tb_sentiment = tb_result['textblob_sentiment']
        vader_sentiment = vader_result['vader_sentiment']
        
        # Check accuracy
        if tb_sentiment == expected:
            textblob_correct += 1
        if vader_sentiment == expected:
            vader_correct += 1
        
        display_text = text[:35] + "..." if len(text) > 35 else text
        print(f"{display_text:<40} {expected:<10} {tb_sentiment:<10} {vader_sentiment:<10}")
    
    print("-" * 70)
    print(f"TextBlob accuracy: {textblob_correct}/{len(test_cases)} ({textblob_correct/len(test_cases)*100:.1f}%)")
    print(f"VADER accuracy: {vader_correct}/{len(test_cases)} ({vader_correct/len(test_cases)*100:.1f}%)")
    print()

def main():
    """Run all demo functions"""
    print("🚀 Web Scraper with Sentiment Analysis - Demo")
    print("=" * 60)
    print()
    
    # Run all demos
    demo_custom_topic()
    demo_custom_visualization()
    demo_analyze_custom_data()
    demo_compare_methods()
    
    print("✅ All demos completed!")
    print("\nTo customize the main application:")
    print("1. Edit the config in main.py to change topics/subreddits")
    print("2. Modify the scraping functions in web_scraper.py")
    print("3. Add custom visualization methods in visualizer.py")
    print("4. Use the individual components as shown in these demos")

if __name__ == "__main__":
    main()
