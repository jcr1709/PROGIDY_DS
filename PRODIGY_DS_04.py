import os
import json
import csv
import pandas as pd
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon
import nltk
nltk.download('vader_lexicon')

def get_sentiment_vader(text):
    sid = SentimentIntensityAnalyzer()
    # Get the sentiment compound score
    compound_score = sid.polarity_scores(text)['compound']

    # Classify the sentiment based on the compound score
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def get_youtube_comments(api_key, video_id):
    # Create a YouTube API service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get video comments
    comments_data = []
    nextPageToken = None

    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            pageToken=nextPageToken
        ).execute()

        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            sentiment = get_sentiment_vader(comment_text)
            comments_data.append({'Comment': comment_text, 'Sentiment': sentiment})

        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

    return comments_data

def save_to_csv(comments_data, csv_filename):
    # Save comments and sentiment to CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Comment', 'Sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for comment_data in comments_data:
            writer.writerow(comment_data)

def main():
    # Replace 'YOUR_API_KEY' and 'VIDEO_ID' with your actual YouTube Data API key and video ID
    api_key = 'AIzaSyARf8B51rzzXnSHrUbpoQK5KG8knoxWBPE'
    video_id = 'EbSBgUJYl0s'

    # Get comments and sentiment using VADER
    comments_data = get_youtube_comments(api_key, video_id)

    # Save comments and sentiment to CSV
    csv_filename = 'youtube_comments_with_sentiment_vader.csv'
    save_to_csv(comments_data, csv_filename)

    print(f'Comments and sentiment saved to {csv_filename}')

if __name__ == '__main__':
    main()
