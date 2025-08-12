"""
Configuration file for the Web Scraper with Sentiment Analysis project.

Edit these settings to customize the behavior of the application.
"""

# =============================================================================
# SCRAPING CONFIGURATION
# =============================================================================

# Reddit configuration
REDDIT_CONFIG = {
    'subreddit': 'technology',  # Change to any subreddit: 'worldnews', 'politics', 'movies', etc.
    'topic': 'artificial intelligence',  # Topic to search for
    'limit': 30  # Number of posts to scrape (max recommended: 100)
}

# News sources configuration (optional)
NEWS_CONFIG = {
    'topic': 'artificial intelligence',
    'urls': [
        'https://news.google.com/search?q=artificial+intelligence',
        'https://www.bbc.com/search?q=artificial+intelligence'
    ]
}

# Web scraping settings
SCRAPING_SETTINGS = {
    'delay': 1,  # Delay between requests (seconds) - be respectful!
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# =============================================================================
# ANALYSIS CONFIGURATION
# =============================================================================

# Sentiment analysis settings
SENTIMENT_SETTINGS = {
    'enable_textblob': True,
    'enable_vader': True,
    'consensus_method': 'strongest_signal',  # 'majority_vote' or 'strongest_signal'
}

# Time analysis settings
TIME_ANALYSIS = {
    'time_period': '1H',  # Group by: '1H' (hour), '1D' (day), '1W' (week)
    'timezone': 'UTC'
}

# =============================================================================
# VISUALIZATION CONFIGURATION
# =============================================================================

# Plot settings
PLOT_SETTINGS = {
    'style': 'default',  # matplotlib style
    'figsize': (12, 8),  # default figure size
    'dpi': 300,  # resolution for saved plots
    'save_plots': True,
    'show_plots': True  # Set to False if running on server without display
}

# Output settings
OUTPUT_SETTINGS = {
    'output_directory': 'sentiment_analysis_results',
    'save_csv': True,
    'save_json': True,
    'create_dashboard': True,
    'create_wordcloud': True  # Only works if wordcloud package is installed
}

# Plot types to generate
PLOT_TYPES = {
    'sentiment_distribution': True,
    'time_series': True,
    'score_distributions': True,
    'correlation_heatmap': True,
    'word_cloud': True,
    'comprehensive_dashboard': True
}

# =============================================================================
# ADVANCED CONFIGURATION
# =============================================================================

# Text preprocessing settings
TEXT_PROCESSING = {
    'remove_urls': True,
    'remove_special_chars': True,
    'remove_extra_whitespace': True,
    'min_text_length': 10,  # Minimum characters for text to be included
    'max_text_length': 1000  # Maximum characters (longer texts will be truncated)
}

# Sample data configuration (used when scraping fails)
SAMPLE_DATA_CONFIG = {
    'use_sample_data': True,  # Fallback to sample data if scraping fails
    'sample_size': 20,
    'sample_topics': [
        'artificial intelligence',
        'machine learning',
        'technology',
        'programming',
        'data science'
    ]
}

# =============================================================================
# EASY PRESETS
# =============================================================================

# Predefined configurations for common use cases
PRESETS = {
    'tech_news': {
        'reddit': {'subreddit': 'technology', 'topic': 'artificial intelligence', 'limit': 50},
        'description': 'Analyze sentiment about AI in technology discussions'
    },
    
    'political_sentiment': {
        'reddit': {'subreddit': 'politics', 'topic': 'election', 'limit': 50},
        'description': 'Analyze political sentiment about elections'
    },
    
    'movie_reviews': {
        'reddit': {'subreddit': 'movies', 'topic': 'review', 'limit': 30},
        'description': 'Analyze sentiment in movie reviews'
    },
    
    'crypto_discussion': {
        'reddit': {'subreddit': 'cryptocurrency', 'topic': 'bitcoin', 'limit': 40},
        'description': 'Analyze sentiment about Bitcoin in crypto communities'
    },
    
    'climate_change': {
        'reddit': {'subreddit': 'environment', 'topic': 'climate change', 'limit': 30},
        'description': 'Analyze sentiment about climate change discussions'
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_preset(preset_name):
    """
    Get a predefined configuration preset.
    
    Args:
        preset_name (str): Name of the preset to use
        
    Returns:
        dict: Configuration dictionary for the preset
    """
    if preset_name in PRESETS:
        return PRESETS[preset_name]
    else:
        available = ', '.join(PRESETS.keys())
        raise ValueError(f"Preset '{preset_name}' not found. Available presets: {available}")

def list_presets():
    """List all available configuration presets."""
    print("Available configuration presets:")
    print("=" * 50)
    for name, config in PRESETS.items():
        print(f"🔹 {name}: {config['description']}")
    print("\nUsage: config.get_preset('preset_name')")

def validate_config():
    """Validate the current configuration settings."""
    issues = []
    
    # Check required fields
    if not REDDIT_CONFIG.get('subreddit'):
        issues.append("REDDIT_CONFIG['subreddit'] is required")
    
    if not REDDIT_CONFIG.get('topic'):
        issues.append("REDDIT_CONFIG['topic'] is required")
    
    if REDDIT_CONFIG.get('limit', 0) <= 0:
        issues.append("REDDIT_CONFIG['limit'] must be greater than 0")
    
    # Check output directory
    if not OUTPUT_SETTINGS.get('output_directory'):
        issues.append("OUTPUT_SETTINGS['output_directory'] is required")
    
    # Check time period format
    valid_periods = ['1H', '1D', '1W', '1M']
    if TIME_ANALYSIS.get('time_period') not in valid_periods:
        issues.append(f"TIME_ANALYSIS['time_period'] must be one of: {valid_periods}")
    
    if issues:
        print("❌ Configuration issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Configuration is valid!")
        return True

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

if __name__ == "__main__":
    # Example: List available presets
    list_presets()
    
    print("\n" + "=" * 50)
    
    # Example: Validate current configuration
    validate_config()
    
    print("\n" + "=" * 50)
    
    # Example: Get a preset configuration
    try:
        tech_config = get_preset('tech_news')
        print(f"Tech news preset: {tech_config}")
    except ValueError as e:
        print(f"Error: {e}")
