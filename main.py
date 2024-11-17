# The project's aim is to create a customizable news feed to later be integrated in other projects

import requests
import schedule
import time
from config import API_KEY, BASE_URL

# Define the function to fetch news articles based on topics
def fetch_news(topics, language='en', max_results=5):
    articles = []
    for topic in topics:
        # Define the request parameters
        params = {
            'q': topic,
            'language': language,
            'apiKey': API_KEY,
            'pageSize': max_results,
            'sortBy': 'publishedAt',
            #'from': '2024-11-16'
        }

        # Make a request to News API
        response = requests.get(BASE_URL, params=params)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            for article in data['articles']:
                articles.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'publishedAt': article['publishedAt']
                })
        else:
            print(f"Error fetching news for topic '{topic}': {response.status_code}")

    return articles


# Define a function to display the news articles
def display_news(articles):
    print('\n' + '-' * 80)
    print(f"{'-'*34} Latest  News {'-'*34}")
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Published At: {article['publishedAt']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
    print('-' * 80)


# Schedule the news fetching function to run periodically
def scheduled_news_feed(topics, interval=1):
    def job():
        articles = fetch_news(topics)
        display_news(articles)

    # Schedule the job to run at a given interval (in minutes)
    schedule.every(interval).minutes.do(job)

    print(f"Starting news feed. Checking for updates every {interval} minutes...")

    # Keep running the scheduled job
    while True:
        schedule.run_pending()
        time.sleep(1)


# Define the topics you're interested in
topics = ["technology", "artificial intelligence"]

# Start the scheduled news feed
scheduled_news_feed(topics, interval=1)
