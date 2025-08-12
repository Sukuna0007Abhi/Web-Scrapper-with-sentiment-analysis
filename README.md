# Web Scraper with Sentiment Analysis

A comprehensive Python project that combines web scraping and natural language processing to analyze public sentiment on any topic.


## Demo 
<img width="1920" height="1080" alt="Screenshot 2025-08-12 193640" src="https://github.com/user-attachments/assets/898e4da8-2573-4e8a-8d4e-e1328db0622f" />
<img width="1920" height="1080" alt="Screenshot 2025-08-12 193701" src="https://github.com/user-attachments/assets/441c9dcf-00c4-4633-9c15-0d27debb7ce6" />
<img width="1920" height="1080" alt="Screenshot 2025-08-12 193716" src="https://github.com/user-attachments/assets/54e526b1-b2d1-416d-b36d-93824535e833" />
<img width="1920" height="1080" alt="Screenshot 2025-08-12 193740" src="https://github.com/user-attachments/assets/c80126bd-26b8-4d9e-b014-939705068c50" />
Final:
<img width="1920" height="1080" alt="Screenshot 2025-08-12 193754" src="https://github.com/user-attachments/assets/8c8632ea-af7e-4afb-b9b8-f4afcafab062" />

## Features

- **Web Scraping**: Fetch content from Reddit and news websites using `requests` and `BeautifulSoup`
- **Data Processing**: Clean and structure text data with `pandas`
- **Sentiment Analysis**: Dual sentiment scoring using both TextBlob and NLTK's VADER
- **Visualization**: Generate comprehensive plots and dashboards with `matplotlib` and `seaborn`
- **Word Clouds**: Create visual representations of text content
- **Time Series Analysis**: Track sentiment trends over time

## Installation

1. Install Python 3.7 or higher
2. Install required packages:

```bash
pip install -r requirements.txt
```

## Quick Start

Simply run the main script:

```bash
python main.py
```

The script will:
1. Scrape recent posts about "artificial intelligence" from Reddit's r/technology
2. Analyze sentiment using both TextBlob and VADER
3. Generate visualizations and save results
4. Create a comprehensive dashboard

## Project Structure

```
├── main.py                 # Main script to run the analysis
├── web_scraper.py         # Web scraping functionality
├── sentiment_analyzer.py  # Sentiment analysis using TextBlob and VADER
├── visualizer.py          # Data visualization and plotting
├── requirements.txt       # Python dependencies
└── sentiment_analysis_results/  # Output directory (created automatically)
    ├── sentiment_analysis_data.csv
    ├── sentiment_trends.csv
    ├── sentiment_summary.json
    └── *.png (visualization plots)
```

## Components

### 1. Web Scraper (`web_scraper.py`)
- Scrapes Reddit posts and comments
- Supports news website scraping
- Includes text cleaning and preprocessing
- Respectful scraping with delays

### 2. Sentiment Analyzer (`sentiment_analyzer.py`)
- **TextBlob**: Provides polarity (-1 to 1) and subjectivity (0 to 1) scores
- **VADER**: Optimized for social media text, provides compound scores
- Consensus sentiment combining both methods
- Batch processing for efficiency

### 3. Visualizer (`visualizer.py`)
- Sentiment distribution pie charts
- Time series plots showing trends
- Score distribution histograms
- Correlation heatmaps
- Word clouds for different sentiments
- Comprehensive dashboard combining all visualizations

## Customization

### Change the Topic
Edit the configuration in `main.py`:

```python
config = {
    'reddit': {
        'subreddit': 'worldnews',  # Change subreddit
        'topic': 'climate change',  # Change topic
        'limit': 50  # Number of posts
    }
}
```

### Add More Sources
Extend the scraper to include additional websites:

```python
# In web_scraper.py, add custom scraping methods
def scrape_custom_site(self, url, topic):
    # Your custom scraping logic here
    pass
```

### Modify Visualizations
The `SentimentVisualizer` class provides flexible plotting methods that can be customized for your needs.

## Sample Output

The script generates:

- **Sentiment Distribution**: Pie chart showing positive/negative/neutral percentages
- **Time Series**: How sentiment changes over time
- **Score Distributions**: Histograms of sentiment scores
- **Word Clouds**: Visual representation of most common words
- **Dashboard**: Combined view of all metrics

## Example Results

```
📊 SENTIMENT ANALYSIS RESULTS
==================================================
Total posts analyzed: 25
Positive: 12 (48.0%)
Negative: 8 (32.0%)
Neutral: 5 (20.0%)

Average Sentiment Scores:
TextBlob Polarity: 0.145 (-1 to 1)
VADER Compound: 0.231 (-1 to 1)
TextBlob Subjectivity: 0.456 (0 to 1)
```

## Technical Details

### Sentiment Analysis Methods

1. **TextBlob**:
   - Polarity: -1 (negative) to 1 (positive)
   - Subjectivity: 0 (objective) to 1 (subjective)

2. **VADER**:
   - Compound: -1 (negative) to 1 (positive)
   - Individual scores: positive, negative, neutral

3. **Consensus**:
   - Combines both methods for final classification
   - Uses stronger signal when methods disagree

### Data Processing Pipeline

1. **Scraping**: Fetch raw HTML content
2. **Parsing**: Extract text using BeautifulSoup
3. **Cleaning**: Remove URLs, special characters, normalize whitespace
4. **Analysis**: Apply sentiment analysis algorithms
5. **Visualization**: Generate plots and save results

## Error Handling

The script includes robust error handling:
- Falls back to sample data if scraping fails
- Handles missing or malformed data
- Graceful degradation for visualization errors

## Contributing

Feel free to extend this project by:
- Adding new data sources
- Implementing additional sentiment analysis methods
- Creating new visualization types
- Improving the scraping reliability

## License

This project is for educational purposes. Please respect website terms of service when scraping.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all packages are installed with `pip install -r requirements.txt`
2. **No Data Scraped**: The script will use sample data for demonstration
3. **Visualization Errors**: Some environments may not support GUI displays - plots will still be saved as files

### System Requirements

- Python 3.7+
- Internet connection for scraping
- 512MB+ RAM for processing
- GUI support for displaying plots (optional - plots are saved as files)
