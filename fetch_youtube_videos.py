import os
import json
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

# Youtube Data API
YOUTUBE_DATA_API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_DATA_API_KEY)

os.makedirs('out', exist_ok=True)


def get_channel_id(channel_url):
    # Extract channel ID from URL
    request = youtube.search().list(
        part='snippet',
        q=channel_url,
        type='channel'
    )
    response = request.execute()
    return response['items'][0]['snippet']['channelId']


def get_top_videos(channel_id, max_results=10):
    # Get top N videos based on view count
    request = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        type='video',
        order='viewCount',
        maxResults=max_results
    )
    response = request.execute()
    return [(item['id']['videoId'], item['snippet']['title']) for item in response['items']]


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except:
        return "Transcript not available"


def chunk_transcript(transcript, max_length=5000):
    chunks = []
    current_chunk = ""
    words = transcript.split()

    for word in words:
        if len(current_chunk) + len(word) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
        else:
            current_chunk += word + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def save_to_json(data, filename='video_transcripts.json'):
    filepath = os.path.join('out', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Transcripts for saved to {filename}")


def save_to_csv(data, filename='video_transcripts.csv'):
    filepath = os.path.join('out', filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Video ID', 'Title', 'Transcript'])  # Header
        for item in data:
            writer.writerow(
                [item['video_id'], item['title'], item['transcript'][:1000]])

    print(f"Transcripts for saved to {filename}")


def main(channel_url, max_results=10):
    channel_id = get_channel_id(channel_url)
    top_videos = get_top_videos(channel_id, max_results)

    results = []
    for video_id, title in top_videos:
        transcript = get_transcript(video_id)
        results.append({
            'video_id': video_id,
            'title': title,
            'transcript': transcript
        })

    # print(results)

    save_to_json(results, f'video_transcripts_{channel_id}.json')
    save_to_csv(results, f'video_transcripts_{channel_id}.csv')


if __name__ == '__main__':
    # channel_url = input("Enter the YouTube channel URL: ")
    # max_results = int(input("Enter the number of top videos to fetch: "))

    channel_url = "https://www.youtube.com/@sadhguru"
    max_results = 25

    main(channel_url, max_results)
