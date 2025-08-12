#!/usr/bin/env python3
"""
Web Scraper with Sentiment Analysis

This script demonstrates how to scrape web content and analyze sentiment.
It combines web scraping, data cleaning, sentiment analysis, and visualization.

Usage:
    python main.py

Author: GitHub Copilot
Date: August 12, 2025
"""

import os
import sys
from datetime import datetime, timedelta
import json

# Import our custom modules
from web_scraper import WebScraper
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer, HAS_WORDCLOUD

def main():
    """Main function to run the web scraper with sentiment analysis"""
    
    print("🔍 Web Scraper with Sentiment Analysis")
    print("=" * 50)
    
    # Configuration for scraping
    config = {
        'reddit': {
            'subreddit': 'technology',  # You can change this to any subreddit
            'topic': 'artificial intelligence',  # The topic to search for
            'limit': 30  # Number of posts to scrape
        },
        'news': {
            'topic': 'artificial intelligence',
            'urls': [
                'https://news.google.com/search?q=artificial+intelligence',
                'https://www.bbc.com/search?q=artificial+intelligence'
            ]
        }
    }
    
    # Initialize components
    print("🚀 Initializing components...")
    scraper = WebScraper(delay=1)  # 1 second delay between requests
    analyzer = SentimentAnalyzer()
    visualizer = SentimentVisualizer()
    
    # Step 1: Scrape data
    print(f"\n📥 Scraping data about '{config['reddit']['topic']}'...")
    try:
        # Scrape from Reddit (easier and more reliable than news sites)
        reddit_data = scraper.scrape_reddit_comments(
            config['reddit']['subreddit'],
            config['reddit']['topic'],
            config['reddit']['limit']
        )
        
        if not reddit_data:
            print("⚠️  No data found. Let's create some sample data for demonstration...")
            reddit_data = create_sample_data()
        
        print(f"✅ Successfully scraped {len(reddit_data)} posts")
        
        # Convert to DataFrame and clean
        import pandas as pd
        df = pd.DataFrame(reddit_data)
        
        if not df.empty:
            # Clean the text data
            df['cleaned_text'] = df['combined_text'].apply(scraper.clean_text)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Remove empty texts
            df = df[df['cleaned_text'].str.len() > 0]
            
            # Sort by timestamp
            df = df.sort_values('timestamp')
        
        if df.empty:
            print("❌ No data to analyze. Exiting...")
            return
            
        print(f"📊 Data cleaned. {len(df)} posts ready for analysis.")
        
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        print("🔄 Using sample data instead...")
        reddit_data = create_sample_data()
        
        # Convert to DataFrame and clean
        import pandas as pd
        df = pd.DataFrame(reddit_data)
        
        if not df.empty:
            # Clean the text data
            df['cleaned_text'] = df['combined_text'].apply(scraper.clean_text)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Remove empty texts
            df = df[df['cleaned_text'].str.len() > 0]
            
            # Sort by timestamp
            df = df.sort_values('timestamp')
    
    # Step 2: Perform sentiment analysis
    print(f"\n🧠 Analyzing sentiment for {len(df)} texts...")
    df_with_sentiment = analyzer.analyze_batch(df)
    
    # Step 3: Get summary statistics
    print("\n📈 Generating summary statistics...")
    summary = analyzer.get_sentiment_summary(df_with_sentiment)
    
    # Print summary
    print("\n" + "="*50)
    print("📊 SENTIMENT ANALYSIS RESULTS")
    print("="*50)
    
    dist = summary['sentiment_distribution']
    print(f"Total posts analyzed: {len(df_with_sentiment)}")
    print(f"Positive: {dist['positive']} ({dist['positive_pct']:.1f}%)")
    print(f"Negative: {dist['negative']} ({dist['negative_pct']:.1f}%)")
    print(f"Neutral: {dist['neutral']} ({dist['neutral_pct']:.1f}%)")
    
    scores = summary['average_scores']
    print(f"\nAverage Sentiment Scores:")
    print(f"TextBlob Polarity: {scores['textblob_polarity']:.3f} (-1 to 1)")
    print(f"VADER Compound: {scores['vader_compound']:.3f} (-1 to 1)")
    print(f"TextBlob Subjectivity: {scores['textblob_subjectivity']:.3f} (0 to 1)")
    
    # Show most positive and negative examples
    print(f"\n🟢 Most Positive (Score: {summary['extremes']['most_positive']['score']:.3f}):")
    print(f"   \"{summary['extremes']['most_positive']['text']}\"")
    
    print(f"\n🔴 Most Negative (Score: {summary['extremes']['most_negative']['score']:.3f}):")
    print(f"   \"{summary['extremes']['most_negative']['text']}\"")
    
    # Step 4: Analyze trends over time
    print(f"\n📅 Analyzing sentiment trends over time...")
    trend_df = analyzer.analyze_sentiment_over_time(df_with_sentiment, time_period='1H')
    
    if len(trend_df) > 1:
        print(f"✅ Generated trend analysis for {len(trend_df)} time periods")
    else:
        # If not enough time variation, create hourly trends for demo
        trend_df = create_sample_trends(df_with_sentiment)
        print(f"✅ Generated sample trend analysis for demonstration")
    
    # Step 5: Create visualizations
    print(f"\n📊 Creating visualizations...")
    
    try:
        # Create output directory
        output_dir = "sentiment_analysis_results"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate plots
        print("  📈 Creating sentiment distribution plot...")
        visualizer.plot_sentiment_distribution(
            df_with_sentiment, 
            save_path=f"{output_dir}/sentiment_distribution.png"
        )
        
        if len(trend_df) > 1:
            print("  📊 Creating time series plot...")
            visualizer.plot_sentiment_over_time(
                trend_df, 
                save_path=f"{output_dir}/sentiment_trends.png"
            )
        
        print("  📋 Creating sentiment scores distribution...")
        visualizer.plot_sentiment_scores_distribution(
            df_with_sentiment, 
            save_path=f"{output_dir}/score_distributions.png"
        )
        
        print("  ☁️  Creating word cloud...")
        if HAS_WORDCLOUD:
            visualizer.create_word_cloud(
                df_with_sentiment, 
                save_path=f"{output_dir}/wordcloud_all.png"
            )
        else:
            print("    Word cloud skipped (package not available)")
        
        print("  🔥 Creating correlation heatmap...")
        visualizer.create_sentiment_heatmap(
            df_with_sentiment, 
            save_path=f"{output_dir}/correlation_heatmap.png"
        )
        
        if len(trend_df) > 1:
            print("  🎯 Creating comprehensive dashboard...")
            visualizer.create_comprehensive_dashboard(
                df_with_sentiment, 
                trend_df, 
                save_path=f"{output_dir}/dashboard.png"
            )
        
    except Exception as e:
        print(f"⚠️  Error creating some visualizations: {e}")
        print("This might be due to missing GUI support or display issues.")
    
    # Step 6: Save results
    print(f"\n💾 Saving results...")
    
    # Save data to CSV
    df_with_sentiment.to_csv(f"{output_dir}/sentiment_analysis_data.csv", index=False)
    trend_df.to_csv(f"{output_dir}/sentiment_trends.csv", index=False)
    
    # Save summary to JSON
    with open(f"{output_dir}/sentiment_summary.json", 'w') as f:
        # Convert numpy types to Python types for JSON serialization
        json_summary = convert_numpy_types(summary)
        json.dump(json_summary, f, indent=2, default=str)
    
    print(f"✅ Results saved to '{output_dir}' directory")
    print(f"   - sentiment_analysis_data.csv: Full dataset with sentiment scores")
    print(f"   - sentiment_trends.csv: Sentiment trends over time")
    print(f"   - sentiment_summary.json: Summary statistics")
    print(f"   - *.png: Various visualization plots")
    
    print(f"\n🎉 Analysis complete! Check the '{output_dir}' folder for all results.")

def create_sample_data():
    """Create sample data for demonstration when scraping fails"""
    from datetime import datetime, timedelta
    
    sample_texts = [
        "I love the new AI developments! This technology is amazing and will change everything for the better.",
        "Artificial intelligence is concerning. We need to be careful about job displacement and privacy.",
        "The latest AI research shows promising results in healthcare applications.",
        "Machine learning algorithms are becoming more sophisticated every day.",
        "I'm worried about the ethical implications of AI in decision making.",
        "This AI tool helped me solve a complex problem quickly. Very impressed!",
        "The debate about AI regulation continues among policymakers worldwide.",
        "Neural networks are fascinating from a technical perspective.",
        "AI companies need to be more transparent about their data usage.",
        "The potential of AI in education is enormous and exciting.",
        "Deep learning models require massive computational resources.",
        "I think AI will create more jobs than it destroys in the long run.",
        "The bias in AI systems is a serious problem that needs addressing.",
        "Automation through AI is transforming manufacturing industries.",
        "Natural language processing has improved dramatically in recent years.",
        "I'm excited about the future of AI in creative applications.",
        "The AI winter was a difficult period for the research community.",
        "Computer vision technology is enabling new possibilities in robotics.",
        "AI safety research is crucial for developing beneficial systems.",
        "The democratization of AI tools is empowering more developers."
    ]
    
    sample_data = []
    base_time = datetime.now() - timedelta(hours=12)
    
    for i, text in enumerate(sample_texts):
        sample_data.append({
            'title': f"AI Discussion Post {i+1}",
            'text': text,
            'combined_text': text,
            'score': str(i % 10),
            'timestamp': (base_time + timedelta(minutes=i*30)).isoformat(),
            'source': 'sample',
            'subreddit': 'technology',
            'topic': 'artificial intelligence'
        })
    
    return sample_data

def create_sample_trends(df):
    """Create sample trend data when there's not enough time variation"""
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Create hourly data for the last 12 hours
    trend_data = []
    base_time = datetime.now() - timedelta(hours=12)
    
    # Distribute the existing data across 12 hours
    posts_per_hour = len(df) // 6  # Spread across 6 hours
    if posts_per_hour == 0:
        posts_per_hour = 1
    
    for i in range(6):
        period_time = base_time + timedelta(hours=i*2)
        
        # Sample some posts for this time period
        start_idx = i * posts_per_hour
        end_idx = min((i + 1) * posts_per_hour, len(df))
        period_df = df.iloc[start_idx:end_idx] if start_idx < len(df) else df.iloc[-1:]
        
        if len(period_df) > 0:
            sentiment_counts = period_df['consensus_sentiment'].value_counts()
            
            trend_data.append({
                'period': period_time,
                'total_posts': len(period_df),
                'positive_count': sentiment_counts.get('positive', 0),
                'negative_count': sentiment_counts.get('negative', 0),
                'neutral_count': sentiment_counts.get('neutral', 0),
                'positive_pct': (sentiment_counts.get('positive', 0) / len(period_df)) * 100,
                'negative_pct': (sentiment_counts.get('negative', 0) / len(period_df)) * 100,
                'neutral_pct': (sentiment_counts.get('neutral', 0) / len(period_df)) * 100,
                'avg_textblob_polarity': period_df['textblob_polarity'].mean(),
                'avg_vader_compound': period_df['vader_compound'].mean()
            })
    
    return pd.DataFrame(trend_data)

def convert_numpy_types(obj):
    """Convert numpy types to Python types for JSON serialization"""
    import numpy as np
    
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

if __name__ == "__main__":
    main()
