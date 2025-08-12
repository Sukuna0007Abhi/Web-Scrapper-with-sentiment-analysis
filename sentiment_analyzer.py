from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analyzer with both TextBlob and VADER"""
        self.setup_nltk()
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            print("Downloading VADER lexicon...")
            nltk.download('vader_lexicon', quiet=True)
    
    def analyze_textblob_sentiment(self, text):
        """
        Analyze sentiment using TextBlob
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment scores and classification
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'textblob_polarity': polarity,
                'textblob_subjectivity': subjectivity,
                'textblob_sentiment': sentiment
            }
        except Exception as e:
            print(f"Error in TextBlob analysis: {e}")
            return {
                'textblob_polarity': 0,
                'textblob_subjectivity': 0,
                'textblob_sentiment': 'neutral'
            }
    
    def analyze_vader_sentiment(self, text):
        """
        Analyze sentiment using NLTK's VADER
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: VADER sentiment scores and classification
        """
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            
            # Classify sentiment based on compound score
            compound = scores['compound']
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'vader_positive': scores['pos'],
                'vader_negative': scores['neg'],
                'vader_neutral': scores['neu'],
                'vader_compound': compound,
                'vader_sentiment': sentiment
            }
        except Exception as e:
            print(f"Error in VADER analysis: {e}")
            return {
                'vader_positive': 0,
                'vader_negative': 0,
                'vader_neutral': 1,
                'vader_compound': 0,
                'vader_sentiment': 'neutral'
            }
    
    def analyze_batch(self, df, text_column='cleaned_text'):
        """
        Analyze sentiment for a batch of texts
        
        Args:
            df (pandas.DataFrame): DataFrame containing text data
            text_column (str): Name of the column containing text to analyze
            
        Returns:
            pandas.DataFrame: DataFrame with sentiment analysis results
        """
        print(f"Analyzing sentiment for {len(df)} texts...")
        
        # Initialize result lists
        textblob_results = []
        vader_results = []
        
        for idx, text in enumerate(df[text_column]):
            if idx % 10 == 0:
                print(f"Processing {idx}/{len(df)}...")
            
            # Analyze with TextBlob
            tb_result = self.analyze_textblob_sentiment(str(text))
            textblob_results.append(tb_result)
            
            # Analyze with VADER
            vader_result = self.analyze_vader_sentiment(str(text))
            vader_results.append(vader_result)
        
        # Convert results to DataFrames and merge
        textblob_df = pd.DataFrame(textblob_results)
        vader_df = pd.DataFrame(vader_results)
        
        # Combine with original DataFrame
        result_df = pd.concat([df.reset_index(drop=True), textblob_df, vader_df], axis=1)
        
        # Add consensus sentiment (majority vote between TextBlob and VADER)
        result_df['consensus_sentiment'] = result_df.apply(self._get_consensus_sentiment, axis=1)
        
        print("Sentiment analysis completed!")
        return result_df
    
    def _get_consensus_sentiment(self, row):
        """Get consensus sentiment between TextBlob and VADER"""
        tb_sentiment = row['textblob_sentiment']
        vader_sentiment = row['vader_sentiment']
        
        if tb_sentiment == vader_sentiment:
            return tb_sentiment
        
        # If they disagree, use the stronger signal
        tb_polarity = abs(row['textblob_polarity'])
        vader_compound = abs(row['vader_compound'])
        
        if tb_polarity > vader_compound:
            return tb_sentiment
        else:
            return vader_sentiment
    
    def get_sentiment_summary(self, df):
        """
        Get summary statistics of sentiment analysis
        
        Args:
            df (pandas.DataFrame): DataFrame with sentiment analysis results
            
        Returns:
            dict: Summary statistics
        """
        summary = {}
        
        # Overall sentiment distribution
        sentiment_counts = df['consensus_sentiment'].value_counts()
        total_count = len(df)
        
        summary['sentiment_distribution'] = {
            'positive': sentiment_counts.get('positive', 0),
            'negative': sentiment_counts.get('negative', 0),
            'neutral': sentiment_counts.get('neutral', 0),
            'positive_pct': (sentiment_counts.get('positive', 0) / total_count) * 100,
            'negative_pct': (sentiment_counts.get('negative', 0) / total_count) * 100,
            'neutral_pct': (sentiment_counts.get('neutral', 0) / total_count) * 100
        }
        
        # Average sentiment scores
        summary['average_scores'] = {
            'textblob_polarity': df['textblob_polarity'].mean(),
            'textblob_subjectivity': df['textblob_subjectivity'].mean(),
            'vader_compound': df['vader_compound'].mean(),
            'vader_positive': df['vader_positive'].mean(),
            'vader_negative': df['vader_negative'].mean()
        }
        
        # Most positive and negative texts
        most_positive_idx = df['vader_compound'].idxmax()
        most_negative_idx = df['vader_compound'].idxmin()
        
        summary['extremes'] = {
            'most_positive': {
                'text': df.loc[most_positive_idx, 'cleaned_text'][:200] + "..." if len(df.loc[most_positive_idx, 'cleaned_text']) > 200 else df.loc[most_positive_idx, 'cleaned_text'],
                'score': df.loc[most_positive_idx, 'vader_compound']
            },
            'most_negative': {
                'text': df.loc[most_negative_idx, 'cleaned_text'][:200] + "..." if len(df.loc[most_negative_idx, 'cleaned_text']) > 200 else df.loc[most_negative_idx, 'cleaned_text'],
                'score': df.loc[most_negative_idx, 'vader_compound']
            }
        }
        
        return summary
    
    def analyze_sentiment_over_time(self, df, time_period='1D'):
        """
        Analyze sentiment trends over time
        
        Args:
            df (pandas.DataFrame): DataFrame with timestamp and sentiment data
            time_period (str): Time period for grouping ('1H', '1D', '1W', etc.)
            
        Returns:
            pandas.DataFrame: Sentiment trends over time
        """
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by time period
        time_groups = df.groupby(pd.Grouper(key='timestamp', freq=time_period))
        
        trend_data = []
        
        for period, group in time_groups:
            if len(group) > 0:
                sentiment_counts = group['consensus_sentiment'].value_counts()
                
                trend_data.append({
                    'period': period,
                    'total_posts': len(group),
                    'positive_count': sentiment_counts.get('positive', 0),
                    'negative_count': sentiment_counts.get('negative', 0),
                    'neutral_count': sentiment_counts.get('neutral', 0),
                    'positive_pct': (sentiment_counts.get('positive', 0) / len(group)) * 100,
                    'negative_pct': (sentiment_counts.get('negative', 0) / len(group)) * 100,
                    'neutral_pct': (sentiment_counts.get('neutral', 0) / len(group)) * 100,
                    'avg_textblob_polarity': group['textblob_polarity'].mean(),
                    'avg_vader_compound': group['vader_compound'].mean()
                })
        
        return pd.DataFrame(trend_data)
