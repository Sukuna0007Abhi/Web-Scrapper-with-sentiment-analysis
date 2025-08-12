import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime

class WebScraper:
    def __init__(self, delay=1):
        """
        Initialize the web scraper
        
        Args:
            delay (int): Delay between requests to be respectful to the server
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_reddit_comments(self, subreddit, topic, limit=50):
        """
        Scrape Reddit posts and comments about a specific topic
        
        Args:
            subreddit (str): The subreddit to scrape from
            topic (str): The topic to search for
            limit (int): Maximum number of posts to scrape
            
        Returns:
            list: List of dictionaries containing post data
        """
        posts_data = []
        
        # Search URL for Reddit
        search_url = f"https://old.reddit.com/r/{subreddit}/search"
        params = {
            'q': topic,
            'restrict_sr': 'on',
            'sort': 'new',
            'limit': limit
        }
        
        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all post containers
            posts = soup.find_all('div', class_='thing')
            
            for post in posts[:limit]:
                try:
                    # Extract post title
                    title_element = post.find('a', class_='title')
                    title = title_element.text.strip() if title_element else ""
                    
                    # Extract post text/selftext
                    text_element = post.find('div', class_='usertext-body')
                    text = text_element.text.strip() if text_element else ""
                    
                    # Extract score
                    score_element = post.find('div', class_='score unvoted')
                    score = score_element.text.strip() if score_element else "0"
                    
                    # Extract timestamp
                    time_element = post.find('time')
                    timestamp = time_element.get('datetime') if time_element else datetime.now().isoformat()
                    
                    # Combine title and text for analysis
                    combined_text = f"{title} {text}".strip()
                    
                    if combined_text:  # Only add if there's actual content
                        posts_data.append({
                            'title': title,
                            'text': text,
                            'combined_text': combined_text,
                            'score': score,
                            'timestamp': timestamp,
                            'source': 'reddit',
                            'subreddit': subreddit,
                            'topic': topic
                        })
                        
                except Exception as e:
                    print(f"Error processing post: {e}")
                    continue
                    
                time.sleep(self.delay)
                
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            
        return posts_data
    
    def scrape_news_headlines(self, topic, source_urls=None):
        """
        Scrape news headlines from various sources
        
        Args:
            topic (str): The topic to search for
            source_urls (list): List of news website URLs to scrape
            
        Returns:
            list: List of dictionaries containing news data
        """
        if source_urls is None:
            # Default news sources (these are example URLs - some may require API keys)
            source_urls = [
                f"https://news.google.com/search?q={topic}",
                f"https://www.bbc.com/search?q={topic}",
            ]
        
        news_data = []
        
        for url in source_urls:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Generic headline selectors (you may need to adjust for specific sites)
                headline_selectors = [
                    'h1', 'h2', 'h3',
                    '.headline', '.title',
                    '[data-testid="headline"]',
                    'article h1', 'article h2'
                ]
                
                for selector in headline_selectors:
                    headlines = soup.select(selector)
                    
                    for headline in headlines:
                        text = headline.get_text().strip()
                        if len(text) > 10 and topic.lower() in text.lower():
                            news_data.append({
                                'title': text,
                                'text': '',
                                'combined_text': text,
                                'score': '',
                                'timestamp': datetime.now().isoformat(),
                                'source': urlparse(url).netloc,
                                'topic': topic
                            })
                
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue
                
        return news_data
    
    def clean_text(self, text):
        """
        Clean and preprocess text data
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
            
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s,.!?-]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def scrape_and_clean(self, sources_config):
        """
        Scrape data from multiple sources and clean it
        
        Args:
            sources_config (dict): Configuration for different sources
            
        Returns:
            pandas.DataFrame: Cleaned data ready for sentiment analysis
        """
        all_data = []
        
        # Scrape Reddit if configured
        if 'reddit' in sources_config:
            reddit_config = sources_config['reddit']
            reddit_data = self.scrape_reddit_comments(
                reddit_config['subreddit'],
                reddit_config['topic'],
                reddit_config.get('limit', 50)
            )
            all_data.extend(reddit_data)
        
        # Scrape news if configured
        if 'news' in sources_config:
            news_config = sources_config['news']
            news_data = self.scrape_news_headlines(
                news_config['topic'],
                news_config.get('urls', None)
            )
            all_data.extend(news_data)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        if not df.empty:
            # Clean the text data
            df['cleaned_text'] = df['combined_text'].apply(self.clean_text)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Remove empty texts
            df = df[df['cleaned_text'].str.len() > 0]
            
            # Sort by timestamp
            df = df.sort_values('timestamp')
            
        return df
