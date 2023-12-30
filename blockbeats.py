import requests
from datetime import datetime, timedelta
from snownlp import SnowNLP

def get_recent_news_and_analyze_sentiment_snownlp():
    # API endpoint
    api_endpoint = "https://api.theblockbeats.news/v1/open-api/open-flash"

    # Calculate the date two days ago
    two_days_ago = datetime.now() - timedelta(days=2)
    two_days_ago_timestamp = int(two_days_ago.timestamp())

    # Parameters for the API request
    params = {
        "size": 10,  # Number of items per page
        "page": 1,  # Page number
        "type": "push",  # Type of news
        "lang": "cn"  # Language
    }

    # Making a GET request to the API
    response = requests.get(api_endpoint, params=params)

    # Initialize sentiment analysis variables
    total_sentiment_score = 0
    news_count = 0

    if response.status_code == 200:
        # Parsing the response
        data = response.json()
        # Filtering news from the last two days
        recent_news = [item for item in data['data']['data'] if int(item['create_time']) >= two_days_ago_timestamp]

        # Analyze sentiment for each news item
        for item in recent_news:
            content = item['content']
            analysis = SnowNLP(content)
            sentiment_score = analysis.sentiments
            total_sentiment_score += sentiment_score
            news_count += 1

            print(f"Content: {content}\nSentiment Score: {sentiment_score}\n")

        if news_count > 0:
            average_sentiment_score = total_sentiment_score / news_count
            print(f"Average Sentiment Score: {average_sentiment_score}")
        else:
            print("No recent news found.")
    else:
        print("Error:", response.status_code)

get_recent_news_and_analyze_sentiment_snownlp()
