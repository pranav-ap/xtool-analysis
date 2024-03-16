import json
from collections import defaultdict

likes_weight = 0.1
replies_weight = 0.4
reposts_weight = 0.3
views_weight = 0.2

file_path = './crawlingDB.json'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"The file at {file_path} was not found.")

tweets = data['tweets']

daily_scores = defaultdict(lambda: {'total_signed_score': 0, 'total_score': 0})
sentiment_scores = defaultdict(lambda: 0)

for tweet in tweets:
    likes = tweet['likes']
    replies = tweet['replies']
    reposts = tweet['reposts']
    views = tweet['views']
    sentiment = tweet['sentiment']
    date = tweet['time']  

    total_weight = (
        likes * likes_weight +
        replies * replies_weight +
        reposts * reposts_weight +
        views * views_weight
    )

    label = 0

    if sentiment == 'positive':
        label = 1
    elif sentiment == 'negative':
        label = -1

    numerator = label * total_weight

    daily_scores[date]['total_signed_score'] += numerator
    daily_scores[date]['total_score'] += total_weight


for date, scores in daily_scores.items():
    if scores['total_score'] > 0: 
        sentiment_scores[date] = scores['total_signed_score'] / scores['total_score']
    

data['sentiment_scores'] = sentiment_scores

with open(file_path, 'w') as file:
    try:
        json.dump(data, file, indent=4)
    except:
        print("Error writing to JSON file")
        exit(1)
