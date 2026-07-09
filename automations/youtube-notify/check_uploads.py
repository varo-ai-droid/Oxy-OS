#!/usr/bin/env python3
"""
YouTube Upload Notifier - Checks RSS feeds for new videos and sends Telegram notifications
"""

import feedparser
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / '.env')

BOT_TOKEN_NOTIFY = os.getenv('BOT_TOKEN_NOTIFY')
CHAT_ID_NOTIFY = os.getenv('CHAT_ID_NOTIFY')

# State tracking file
STATE_FILE = 'last_videos.json'
NOTIFIED_FILE = 'notified_videos.txt'

# All 88 YouTube channels from your subscriptions
CHANNELS = [
    ('Daniel Barada', 'UC-Pr8PZsZ9ok7Ith3LlFZDw'),
    ('Bilal Kamarieh', 'UC07lRcBhjIJYbw1AHmVXYvw'),
    ('UrsKalecinskiTV', 'UC110sPkp4cqssvlFBI6iOTw'),
    ('RepOne', 'UC1YADBsoDnowlqQbtx0PjbA'),
    ('Aba William', 'UC1uEIIdQo0F6wLV-XSMCSvQ'),
    ('Fabian Huber', 'UC2qwc_3-QDMaqpkROR6r7wA'),
    ('Ben AI', 'UC3KK7ENB_ierAXvrxVNnbZQ'),
    ('Theo Tanchak', 'UC3hbdzgSzisn5GONpk0Xlzg'),
    ('Chris Bumstead', 'UC4514FwdRy5gI6CdC9GPb0w'),
    ('Rowan', 'UC4VRuIXIYtZd0yh1MRd9DCg'),
    ('Dylan Calisthenx', 'UC4meh_SCbsNM2R49iwQZ8uA'),
    ('Tristyn Lee', 'UC53s-VII9tDkMRzg2zqFzmw'),
    ('Jeff Nippard', 'UC68TLK0mAEzUyHx5x5k-S1Q'),
    ('Greg Lav', 'UC6vuqBzXNU8mLQvZmjl__Cg'),
    ('JAN', 'UC8-g7Rs0k7vWAoUZHEBdtaw'),
    ('William Niewiara', 'UC9wj8KPMMTnZyk0lFGlnicg'),
    ('EINFACH FUSSBALL.', 'UCAWasvnUzSnIfNkAHIifNFg'),
    ('DAZN UEFA Champions League', 'UCB-GdMjyokO9lZkKU_oIK6g'),
    ('Will Tennyson', 'UCB2wtYpfbCpYDc5TeTwuqFA'),
    ('SuperSimpleDev', 'UCB6dvaWu0N8uVq2yKsZ5s5g'),
    ('Lukas Liebing', 'UCBBugia9zqyt3P7TPORlxqg'),
    ('Mike and Matty', 'UCBX_-ls-dXuhFNSWSXcHrTA'),
    ('Iamanael', 'UCDKa1nYob_oHk_g62yLoOAA'),
    ('Bryce Crawford Podcast', 'UCE63fBeQIoJ2P2mlBkQDchA'),
    ('Football Made Simple', 'UCFY0YHhxiIQWYYsLgeUBcbg'),
    ('Kay Gedan', 'UCFc3ac8bjMVcSK252ydB9fg'),
    ('Coach Andy', 'UCFqqXmb6tTzx6jrcf77KTgg'),
    ('Paulo Guga', 'UCFvWOQur3DkGZ0Kfmns-7iw'),
    ('Mr. LiterallyMe', 'UCGaH1eGCrg5paIp5bP9J40w'),
    ('Bodybuilding Bene', 'UCJbAsPk-U9VUUyHZBBiWOfg'),
    ('Borussia Dortmund', 'UCK8rTVgp3-MebXkmeJcQb1Q'),
    ('Simplicissimus', 'UCKGMHVipEvuZudhHD05FOYA'),
    ('Isaac', 'UCKahK37d-asjW3nqAK3KEEA'),
    ('Greg Doucette', 'UCLqH-U2TXzj1h7lyYQZLNQQ'),
    ('Kai Notebook', 'UCNhWSOlt_UoCzS2YSMhHYmA'),
    ('Geoffrey Verity Schofield', 'UCObA5o3mcc1felIMAv6cukw'),
    ('Rising Ballers', 'UCOlRpr6KnYRFSERY5wLUc9Q'),
    ('Anton', 'UCSl6I450DpPuxfCT1z1DHzQ'),
    ('Trstnnlifts', 'UCTLWIfMJ-4GBImYb_LbS7BA'),
    ('Dominik Lebersorger', 'UCTXLdE42aCyk4BdshycdcSA'),
    ('Max || Editor', 'UCU88AMwgEL9An2HpdAV8DTA'),
    ('Alex Hormozi', 'UCUyDOdBWhC1MCxEjC46d-zw'),
    ('Okan Akbalik', 'UCV0D3_F68DunQlWbViDgZRw'),
    ('James Li', 'UCV9Q7hKsPHf82RfoXWBK5uQ'),
    ('Red Corner MMA', 'UCX4Mc5c5eqKtGvfNl--vrSQ'),
    ('Andrej Karpathy', 'UCXUPKJO5MZQN11PqgIvyuvQ'),
    ('Nilliam Wiewiara', 'UCXhq6GISPC2jvpML-_xzcMA'),
    ('Arda Saatçi', 'UCY3nSxSRpnpsjZ4p15iZxow'),
    ('Clark Kent', 'UCY5TuLTxx-f8R84ZMJE5PKg'),
    ('Money Mind Unfiltered', 'UCYHf6eFhOH61PS8NCon5ieA'),
    ('Eric Janicki', 'UCYYZaF5x2nAb-wvmDyTAnwg'),
    ('someunfilteredguy', 'UCZJxnraUMX4BXGCFTZO14xw'),
    ('Dabby', 'UCZmv8aMKJ_NyS5uFJK_R8lg'),
    ('Christian Wolf', 'UC_NsZgQdK4lTleq_siGOdJw'),
    ('Tim Erens', 'UC__k9W3l_AIuY8KYn_L-ICA'),
    ('Germanbull3', 'UcatcB2I-S4rorA_2KzjluSg'),
    ('FranklinTV', 'UCayD7p9ASZYexlAnDu7m1Dw'),
    ('Reysu', 'UCbDmEdLs-SB3FjrDFQJ4TDg'),
    ('BiloBilo', 'UCcGdEaYDZt7HryBWKAfQQGg'),
    ('EliteScholars Football', 'UCeXp_jcXO8GV436t7mPP_4w'),
    ('Basement Bodybuilding', 'UCf33v9eZOy59r7HM44ni_4Q'),
    ('VfL Wolfsburg', 'UCfdfDFNp50xLjAjD0TKOa4g'),
    ('Outdoor Boys', 'UCfpCQ89W9wjkHc8J_6eTbBg'),
    ('Erik Cupsa', 'UCgKFOz_KrMbmypWrawtzDQg'),
    ('Teachingmensfashion', 'UChNN7VBxPTiNrqjUaQd9bxA'),
    ('Russell Wofford', 'UChWoaUKGr4JCI6DGBKn_oBQ'),
    ('Daniel Kubik', 'UCh_1aALCZcgPl3y6kJ6gJpqQ'),
    ('Stratagem', 'UCk3zZzeoP5AquxYS8oYJA9g'),
    ('Mark Builds Brands', 'UCkRbLkvUX5zuwnKOBwFHOjg'),
    ('DylanD', 'UClfh-374xnMUQDzdXvP_yqQ'),
    ('AJ\'s Life', 'UCm9UaqcjedkALtwlbdw4ECQ'),
    ('Arda Saatci Highlights', 'UCn2OICiqbT787uMqS3iQHWA'),
    ('Steven Muka', 'UCnV9NW7dlxSLEALqsTrIALw'),
    ('TNF', 'UCnZH_HMJwxseGWN1qyG4Y1g'),
    ('3.7Million', 'UCohkCVfU-15iRhmInV14AyQ'),
    ('Sleepy Charlie', 'UCp-R630BEr1UHsvh6HUh8fQ'),
    ('Jacob Juul Hansen', 'UCpJ9TnY2lTA3vBgnq7r5Wmg'),
    ('Found And Explained', 'UCpM4zrZ9c_apiEj6CApj2yw'),
    ('Urs Kalecinski', 'UCpTQ3wtr2BSG1J9VESsDOwA'),
    ('The Franklin', 'UCribK282VRISPZYnW1WIieA'),
    ('GYMDANN', 'UCrjEFYWF5MSMXEPRfUKo3Ww'),
    ('Jeff Nippard Extras', 'UCsUa0GdUH7n0WGG1qqrGXsQ'),
    ('SkillersTV', 'UCsYFm-9E1zC-UThnMWOUCyQ'),
    ('Edmund Yong', 'UCuKVsDS3oVzTuNjnQ79pEEg'),
    ('Sky Sport DE', 'UCuOwl-VgqBHOzR8hWnonBcA'),
    ('UFC', 'UCvgfXK4nTYKudb0rFR6noLA'),
    ('PowerfulJRE', 'UCzQUP1qoWDoEbmsQxvdjxgQ'),
]

def get_last_videos():
    """Load previously seen videos from state file"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_last_videos(state):
    """Save video state to file"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_cutoff_time():
    """Get cutoff time: yesterday 16:01"""
    now = datetime.now()
    # Yesterday at 16:01
    cutoff = datetime(now.year, now.month, now.day, 16, 1) - timedelta(days=1)
    return cutoff

def is_video_after_cutoff(published_str, cutoff_time):
    """Check if video was published after cutoff time"""
    try:
        # Parse YouTube RSS timestamp (ISO format)
        pub_time = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        # Convert to naive datetime for comparison
        pub_time = pub_time.replace(tzinfo=None)
        return pub_time >= cutoff_time
    except Exception as e:
        print(f"Error parsing time {published_str}: {e}")
        return False

def get_notified_videos():
    """Load list of already notified video IDs"""
    if os.path.exists(NOTIFIED_FILE):
        with open(NOTIFIED_FILE, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_notified_video(video_id):
    """Save video ID to notified list"""
    with open(NOTIFIED_FILE, 'a') as f:
        f.write(f"{video_id}\n")

def fetch_latest_video(channel_name, channel_id, cutoff_time, notified_ids):
    """Fetch latest video from channel RSS feed published after cutoff"""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            video_id = entry.yt_videoid
            if video_id not in notified_ids and is_video_after_cutoff(entry.published, cutoff_time):
                return {
                    'video_id': video_id,
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published
                }
    except Exception as e:
        print(f"Error fetching {channel_name}: {e}")
    return None

def send_telegram(message):
    """Send message via Telegram bot"""
    if not BOT_TOKEN_NOTIFY or not CHAT_ID_NOTIFY:
        raise ValueError("BOT_TOKEN_NOTIFY and CHAT_ID_NOTIFY not set in .env file")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN_NOTIFY}/sendMessage"
    payload = {
        'chat_id': CHAT_ID_NOTIFY,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Telegram error: {response.text}")
    return response.json()['result']['message_id']

def main():
    """Main function to check and notify"""
    if not BOT_TOKEN_NOTIFY or not CHAT_ID_NOTIFY:
        print("ERROR: BOT_TOKEN_NOTIFY and CHAT_ID_NOTIFY required in .env file")
        return
    
    cutoff_time = get_cutoff_time()
    state = get_last_videos()
    notified_ids = get_notified_videos()
    new_videos = []
    
    for channel_name, channel_id in CHANNELS:
        video = fetch_latest_video(channel_name, channel_id, cutoff_time, notified_ids)
        if video:
            state[channel_id] = video
            save_notified_video(video['video_id'])
            notified_ids.add(video['video_id'])
            new_videos.append((channel_name, video))
    
    if new_videos:
        for channel_name, video in new_videos:
            message = f"*🔔 NEW VIDEO*\n\n*{channel_name}* uploaded:\n\n[{video['title']}]({video['link']})"
            try:
                send_telegram(message)
                print(f"Notified: {channel_name} - {video['title']}")
            except Exception as e:
                print(f"Telegram error for {channel_name}: {e}")
    
    save_last_videos(state)
    print(f"Checked {len(CHANNELS)} channels. Found {len(new_videos)} new videos since {cutoff_time}")

if __name__ == "__main__":
    main()