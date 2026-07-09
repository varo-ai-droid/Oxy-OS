#!/usr/bin/env python3
"""
Daily News Summary - Fetches RSS feeds and sends to Telegram
"""

import feedparser
import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import requests
from googletrans import Translator

# Load environment variables from root .env
load_dotenv(Path(__file__).parent.parent / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

translator = Translator()
MESSAGE_IDS_FILE = 'message_ids.txt'

# Topic configuration: {topic: (story_count, feeds)}
TOPIC_CONFIG = {
    'P1': {
        'AI': (3, [
            'https://www.artificialintelligence-news.com/feed/',
            'https://techcrunch.com/category/ai/feed/',
            'https://rss.cnn.com/rss/edition_technology.rss'
        ]),
        'Business/Entrepreneurship': (3, [
            'https://www.businessinsider.com/rss',
            'https://feeds.feedburner.com/entrepreneur/latest',
            'https://rss.cnn.com/rss/edition_business.rss'
        ]),
        'Technology': (3, [
            'https://techcrunch.com/feed/',
            'https://www.theverge.com/rss/index.xml',
            'https://arstechnica.com/feed/'
        ])
    },
    'P2': {
        'World News': (2, [
            'https://www.reuters.com/tools/rss',
            'https://rss.cnn.com/rss/edition_world.rss',
            'https://www.bbc.co.uk/news/world/rss.xml'
        ]),
        'Germany': (2, [
            'https://www.tagesschau.de/newsticker.rdf',
            'https://rss.dw.com/de/deutschland/rss',
            'https://www.sueddeutsche.de/rss/news'
        ])
    },
    'P3': {
        'Science': (1, [
            'https://www.nature.com/news/rss',
            'https://www.sciencedaily.com/rss/top',
            'https://rss.sciencemag.org/Science'
        ])
    }
}

def clean_html(text):
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_previous_message_ids():
    """Read previously sent message IDs from file"""
    if os.path.exists(MESSAGE_IDS_FILE):
        with open(MESSAGE_IDS_FILE, 'r') as f:
            return [int(line.strip()) for line in f if line.strip()]
    return []

def save_message_id(msg_id):
    """Save a message ID to file"""
    with open(MESSAGE_IDS_FILE, 'a') as f:
        f.write(f"{msg_id}\n")

def delete_previous_messages():
    """Delete all previous news messages"""
    for msg_id in get_previous_message_ids():
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
            requests.post(url, json={'chat_id': CHAT_ID, 'message_id': msg_id})
        except:
            pass
    # Clear the file after deletion attempt
    if os.path.exists(MESSAGE_IDS_FILE):
        os.remove(MESSAGE_IDS_FILE)

def fetch_stories(topic, count, feeds):
    """Fetch top N stories from topic feeds"""
    stories = []
    seen_titles = set()
    
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:count]:
                if entry.title not in seen_titles:
                    seen_titles.add(entry.title)
                    # Clean HTML from summary
                    summary = entry.get('summary', '')
                    clean_summary = clean_html(summary)
                    stories.append({
                        'title': entry.title,
                        'link': entry.link,
                        'source': feed.feed.get('title', 'Unknown'),
                        'published': entry.get('published', ''),
                        'summary': clean_summary
                    })
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")
    
    return stories[:count]

def summarize(story):
    """Create 2-sentence summary from story content"""
    summary = story['summary']
    # Simple extraction - take first 2 sentences
    if not summary or summary == 'No summary available.':
        return 'No summary available.'
    sentences = summary.split('. ')
    return '. '.join(sentences[:2]) + '.' if sentences else 'No summary available.'

def send_telegram(message):
    """Send message via Telegram bot"""
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN and CHAT_ID not set in .env file")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Telegram error: {response.text}")
    
    return response.json()['result']['message_id']

def main(topic_filter=None):
    """Main function to fetch and send news"""
    # Delete previous messages first
    delete_previous_messages()
    
    message = f"*📰 DAILY NEWS SUMMARY* - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    for priority, topics in TOPIC_CONFIG.items():
        if topic_filter:
            if topic_filter not in str(topics):
                continue
        
        message += f"*{priority} PRIORITY*\n\n"
        
        for topic, (count, feeds) in topics.items():
            if topic_filter and topic_filter.lower() not in topic.lower():
                continue
            
            stories = fetch_stories(topic, count, feeds)
            message += f"*{topic} ({count} stories)*\n"
            
            for i, story in enumerate(stories, 1):
                summary_text = summarize(story)
                try:
                    detected = translator.detect(summary_text[:200])
                    if detected.lang != 'en':
                        summary_text = translator.translate(summary_text, dest='en').text
                except:
                    pass
                
                message += f"*{i}. {story['title']}*\n"
                message += f"   {summary_text[:200]}...\n"
                message += f"   Source: {story['source']} | [Read more]({story['link']})\n\n"
            
            message += "\n"
    
    message += "_Generated by Oxy OS daily-news automation_"
    
    try:
        msg_id = send_telegram(message)
        save_message_id(msg_id)
        print("News sent successfully!")
    except Exception as e:
        with open('errors.log', 'a') as f:
            f.write(f"{datetime.now()}: {e}\n")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    main(topic)