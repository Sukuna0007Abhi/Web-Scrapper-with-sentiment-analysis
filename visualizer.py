import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Optional wordcloud import
try:
    from wordcloud import WordCloud
    HAS_WORDCLOUD = True
except ImportError:
    HAS_WORDCLOUD = False
    print("Note: wordcloud package not available. Word cloud functionality disabled.")

class SentimentVisualizer:
    def __init__(self, style='seaborn-v0_8', figsize=(12, 8)):
        """
        Initialize the sentiment visualizer
        
        Args:
            style (str): Matplotlib style to use
            figsize (tuple): Default figure size
        """
        plt.style.use('default')  # Use default style as seaborn-v0_8 might not be available
        sns.set_palette("husl")
        self.figsize = figsize
        
    def plot_sentiment_distribution(self, df, save_path=None):
        """
        Create a pie chart showing sentiment distribution
        
        Args:
            df (pandas.DataFrame): DataFrame with sentiment analysis results
            save_path (str): Path to save the plot (optional)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Pie chart for overall sentiment distribution
        sentiment_counts = df['consensus_sentiment'].value_counts()
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green, Red, Gray
        
        ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax1.set_title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')
        
        # Bar chart for sentiment comparison between methods
        methods_data = {
            'TextBlob': df['textblob_sentiment'].value_counts(),
            'VADER': df['vader_sentiment'].value_counts(),
            'Consensus': df['consensus_sentiment'].value_counts()
        }
        
        methods_df = pd.DataFrame(methods_data).fillna(0)
        methods_df.plot(kind='bar', ax=ax2, color=['#3498db', '#f39c12', '#9b59b6'])
        ax2.set_title('Sentiment Analysis Method Comparison', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Sentiment')
        ax2.set_ylabel('Count')
        ax2.legend(title='Method')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Sentiment distribution plot saved to: {save_path}")
        
        plt.show()
        
    def plot_sentiment_over_time(self, trend_df, save_path=None):
        """
        Create time series plots showing sentiment trends
        
        Args:
            trend_df (pandas.DataFrame): DataFrame with sentiment trends over time
            save_path (str): Path to save the plot (optional)
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Sentiment percentages over time
        ax1.plot(trend_df['period'], trend_df['positive_pct'], marker='o', 
                label='Positive', color='#2ecc71', linewidth=2)
        ax1.plot(trend_df['period'], trend_df['negative_pct'], marker='s', 
                label='Negative', color='#e74c3c', linewidth=2)
        ax1.plot(trend_df['period'], trend_df['neutral_pct'], marker='^', 
                label='Neutral', color='#95a5a6', linewidth=2)
        ax1.set_title('Sentiment Percentages Over Time', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Time Period')
        ax1.set_ylabel('Percentage (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Total posts over time
        ax2.bar(trend_df['period'], trend_df['total_posts'], color='#3498db', alpha=0.7)
        ax2.set_title('Total Posts Over Time', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Time Period')
        ax2.set_ylabel('Number of Posts')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Average sentiment scores over time
        ax3.plot(trend_df['period'], trend_df['avg_textblob_polarity'], marker='o', 
                label='TextBlob Polarity', color='#f39c12', linewidth=2)
        ax3.plot(trend_df['period'], trend_df['avg_vader_compound'], marker='s', 
                label='VADER Compound', color='#9b59b6', linewidth=2)
        ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax3.set_title('Average Sentiment Scores Over Time', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Time Period')
        ax3.set_ylabel('Sentiment Score')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Stacked area chart of sentiment counts
        ax4.stackplot(trend_df['period'], trend_df['positive_count'], trend_df['neutral_count'], 
                     trend_df['negative_count'], labels=['Positive', 'Neutral', 'Negative'],
                     colors=['#2ecc71', '#95a5a6', '#e74c3c'], alpha=0.7)
        ax4.set_title('Sentiment Counts Over Time (Stacked)', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Time Period')
        ax4.set_ylabel('Number of Posts')
        ax4.legend(loc='upper left')
        ax4.grid(True, alpha=0.3)
        
        # Format x-axis dates
        for ax in [ax1, ax2, ax3, ax4]:
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Time series plot saved to: {save_path}")
        
        plt.show()
        
    def plot_sentiment_scores_distribution(self, df, save_path=None):
        """
        Create histograms showing distribution of sentiment scores
        
        Args:
            df (pandas.DataFrame): DataFrame with sentiment analysis results
            save_path (str): Path to save the plot (optional)
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figsize)
        
        # TextBlob polarity distribution
        ax1.hist(df['textblob_polarity'], bins=30, alpha=0.7, color='#3498db', edgecolor='black')
        ax1.axvline(df['textblob_polarity'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["textblob_polarity"].mean():.3f}')
        ax1.set_title('TextBlob Polarity Distribution', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Polarity Score')
        ax1.set_ylabel('Frequency')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # TextBlob subjectivity distribution
        ax2.hist(df['textblob_subjectivity'], bins=30, alpha=0.7, color='#f39c12', edgecolor='black')
        ax2.axvline(df['textblob_subjectivity'].mean(), color='red', linestyle='--',
                   label=f'Mean: {df["textblob_subjectivity"].mean():.3f}')
        ax2.set_title('TextBlob Subjectivity Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Subjectivity Score')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # VADER compound distribution
        ax3.hist(df['vader_compound'], bins=30, alpha=0.7, color='#9b59b6', edgecolor='black')
        ax3.axvline(df['vader_compound'].mean(), color='red', linestyle='--',
                   label=f'Mean: {df["vader_compound"].mean():.3f}')
        ax3.set_title('VADER Compound Score Distribution', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Compound Score')
        ax3.set_ylabel('Frequency')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # VADER components
        vader_components = df[['vader_positive', 'vader_negative', 'vader_neutral']].mean()
        ax4.bar(range(len(vader_components)), vader_components.values, 
               color=['#2ecc71', '#e74c3c', '#95a5a6'])
        ax4.set_title('Average VADER Component Scores', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Sentiment Component')
        ax4.set_ylabel('Average Score')
        ax4.set_xticks(range(len(vader_components)))
        ax4.set_xticklabels(['Positive', 'Negative', 'Neutral'])
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Score distribution plot saved to: {save_path}")
        
        plt.show()
        
    def create_word_cloud(self, df, sentiment_filter=None, save_path=None):
        """
        Create word clouds for different sentiments
        
        Args:
            df (pandas.DataFrame): DataFrame with sentiment analysis results
            sentiment_filter (str): Filter by sentiment ('positive', 'negative', 'neutral', or None for all)
            save_path (str): Path to save the plot (optional)
        """
        if not HAS_WORDCLOUD:
            print("WordCloud package not available. Skipping word cloud generation.")
            return
            
        if sentiment_filter:
            filtered_df = df[df['consensus_sentiment'] == sentiment_filter]
            title = f'{sentiment_filter.title()} Sentiment Word Cloud'
        else:
            filtered_df = df
            title = 'All Sentiments Word Cloud'
        
        if len(filtered_df) == 0:
            print(f"No data available for sentiment: {sentiment_filter}")
            return
        
        # Combine all text
        text = ' '.join(filtered_df['cleaned_text'].astype(str))
        
        # Create word cloud
        wordcloud = WordCloud(width=800, height=400, 
                             background_color='white',
                             max_words=100,
                             colormap='viridis').generate(text)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Word cloud saved to: {save_path}")
        
        plt.show()
        
    def create_sentiment_heatmap(self, df, save_path=None):
        """
        Create a correlation heatmap of sentiment scores
        
        Args:
            df (pandas.DataFrame): DataFrame with sentiment analysis results
            save_path (str): Path to save the plot (optional)
        """
        # Select sentiment score columns
        sentiment_cols = ['textblob_polarity', 'textblob_subjectivity', 
                         'vader_compound', 'vader_positive', 'vader_negative', 'vader_neutral']
        
        correlation_matrix = df[sentiment_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('Sentiment Scores Correlation Heatmap', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Correlation heatmap saved to: {save_path}")
        
        plt.show()
        
    def create_comprehensive_dashboard(self, df, trend_df, save_path=None):
        """
        Create a comprehensive dashboard with multiple visualizations
        
        Args:
            df (pandas.DataFrame): DataFrame with sentiment analysis results
            trend_df (pandas.DataFrame): DataFrame with sentiment trends over time
            save_path (str): Path to save the plot (optional)
        """
        fig = plt.figure(figsize=(20, 12))
        
        # Create a grid layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Sentiment distribution pie chart
        ax1 = fig.add_subplot(gs[0, 0])
        sentiment_counts = df['consensus_sentiment'].value_counts()
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax1.set_title('Sentiment Distribution', fontweight='bold')
        
        # 2. Sentiment over time
        ax2 = fig.add_subplot(gs[0, 1:3])
        ax2.plot(trend_df['period'], trend_df['positive_pct'], marker='o', 
                label='Positive', color='#2ecc71', linewidth=2)
        ax2.plot(trend_df['period'], trend_df['negative_pct'], marker='s', 
                label='Negative', color='#e74c3c', linewidth=2)
        ax2.set_title('Sentiment Trends Over Time', fontweight='bold')
        ax2.set_ylabel('Percentage (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Score distributions
        ax3 = fig.add_subplot(gs[0, 3])
        ax3.hist(df['vader_compound'], bins=20, alpha=0.7, color='#9b59b6', edgecolor='black')
        ax3.set_title('VADER Compound Scores', fontweight='bold')
        ax3.set_xlabel('Score')
        ax3.set_ylabel('Frequency')
        
        # 4. Method comparison
        ax4 = fig.add_subplot(gs[1, 0])
        methods_data = {
            'TextBlob': df['textblob_sentiment'].value_counts(),
            'VADER': df['vader_sentiment'].value_counts()
        }
        methods_df = pd.DataFrame(methods_data).fillna(0)
        methods_df.plot(kind='bar', ax=ax4, color=['#3498db', '#f39c12'])
        ax4.set_title('Method Comparison', fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. Total posts over time
        ax5 = fig.add_subplot(gs[1, 1:3])
        ax5.bar(trend_df['period'], trend_df['total_posts'], color='#3498db', alpha=0.7)
        ax5.set_title('Post Volume Over Time', fontweight='bold')
        ax5.set_ylabel('Number of Posts')
        ax5.tick_params(axis='x', rotation=45)
        
        # 6. VADER components
        ax6 = fig.add_subplot(gs[1, 3])
        vader_components = df[['vader_positive', 'vader_negative', 'vader_neutral']].mean()
        ax6.bar(range(len(vader_components)), vader_components.values, 
               color=['#2ecc71', '#e74c3c', '#95a5a6'])
        ax6.set_title('Avg VADER Components', fontweight='bold')
        ax6.set_xticks(range(len(vader_components)))
        ax6.set_xticklabels(['Pos', 'Neg', 'Neu'], rotation=45)
        
        # 7. Correlation heatmap
        ax7 = fig.add_subplot(gs[2, :2])
        sentiment_cols = ['textblob_polarity', 'vader_compound', 'vader_positive', 'vader_negative']
        correlation_matrix = df[sentiment_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', ax=ax7, cbar=False)
        ax7.set_title('Sentiment Scores Correlation', fontweight='bold')
        
        # 8. Average scores over time
        ax8 = fig.add_subplot(gs[2, 2:])
        ax8.plot(trend_df['period'], trend_df['avg_textblob_polarity'], marker='o', 
                label='TextBlob', color='#f39c12', linewidth=2)
        ax8.plot(trend_df['period'], trend_df['avg_vader_compound'], marker='s', 
                label='VADER', color='#9b59b6', linewidth=2)
        ax8.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax8.set_title('Average Sentiment Scores Over Time', fontweight='bold')
        ax8.set_ylabel('Score')
        ax8.legend()
        ax8.grid(True, alpha=0.3)
        ax8.tick_params(axis='x', rotation=45)
        
        plt.suptitle('Sentiment Analysis Dashboard', fontsize=20, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dashboard saved to: {save_path}")
        
        plt.show()
