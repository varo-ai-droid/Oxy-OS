#!/usr/bin/env python3
"""
Spotify Podcast Transcript Extractor
Uses spotify_scraper with cookie authentication to extract transcripts.
"""

import os
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from spotify_scraper import SpotifyClient
import re

# Load environment variables from root .env
load_dotenv(Path(__file__).parent.parent / '.env')

SPOTIFY_DC_COOKIE = os.getenv("SPOTIFY_DC_COOKIE")
OUTPUT_DIR = Path(__file__).parent / "raw"
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_episode_id(episode_url: str) -> str:
    """Extract episode ID from Spotify episode URL."""
    match = re.search(r'/episode/([a-zA-Z0-9]+)', episode_url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract episode ID from URL: {episode_url}")


def extract_show_id(show_url: str) -> str:
    """Extract show ID from Spotify show URL."""
    match = re.search(r'/show/([a-zA-Z0-9]+)', show_url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract show ID from URL: {show_url}")


def extract_transcripts(urls: list[str], max_results: int = 50) -> list[dict]:
    """Extract transcripts from Spotify podcast URLs."""
    if not SPOTIFY_DC_COOKIE:
        raise ValueError(
            "SPOTIFY_DC_COOKIE not found. Please add your sp_dc cookie to .env file."
        )
    
    client = SpotifyClient(cookies={"sp_dc": SPOTIFY_DC_COOKIE})
    results = []
    
    for url in urls[:max_results]:
        try:
            if '/show/' in url:
                show_id = extract_show_id(url)
                show = client.get_show(show_id, max_episodes=max_results)
                episodes = list(show.episodes)
                
                print(f"Total episodes in show '{show.name}': {show.total_episodes}")
                print(f"Episodes returned: {len(episodes)}")
                
                for episode in episodes:
                    try:
                        transcript = client.get_transcript(episode.id)
                        if transcript and transcript.lines:
                            transcript_text = "\n".join([line.text for line in transcript.lines])
                            results.append({
                                'episodeTitle': episode.name,
                                'episodeUrl': f"https://open.spotify.com/episode/{episode.id}",
                                'publishDate': episode.release_date.strftime("%Y-%m-%d") if episode.release_date else '',
                                'transcript': transcript_text
                            })
                            print(f"✓ Extracted: {episode.name[:50]}")
                        else:
                            print(f"✗ No transcript: {episode.name[:50]}")
                    except Exception as e:
                        print(f"✗ Error ({episode.name[:30]}): {str(e)[:50]}")
            else:
                episode_id = extract_episode_id(url)
                episode = client.get_episode(episode_id)
                transcript = client.get_transcript(episode_id)
                
                if transcript and transcript.lines:
                    transcript_text = "\n".join([line.text for line in transcript.lines])
                    results.append({
                        'episodeTitle': episode.name,
                        'episodeUrl': episode.share_url or url,
                        'publishDate': episode.release_date.strftime("%Y-%m-%d") if episode.release_date else '',
                        'transcript': transcript_text
                    })
                    print(f"✓ Extracted: {episode.name}")
                else:
                    print(f"✗ No transcript: {episode.name}")
                    
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    return results


def save_transcripts(transcripts: list[dict]) -> None:
    """Save transcripts to individual files in the raw folder."""
    saved_count = 0
    
    for transcript in transcripts:
        title = transcript.get("episodeTitle", "unknown")
        episode_url = transcript.get("episodeUrl", "")
        pub_date = transcript.get("publishDate", "")
        
        safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()[:50]
        date_str = pub_date[:10] if pub_date else datetime.now().strftime("%Y-%m-%d")
        
        filename = f"{date_str} - {safe_title}.txt"
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Episode: {title}\n")
            f.write(f"URL: {episode_url}\n")
            f.write(f"Published: {pub_date}\n")
            f.write("=" * 80 + "\n\n")
            f.write(transcript.get("transcript", ""))
        
        print(f"Saved: {filename}")
        saved_count += 1
    
    print(f"\nTotal saved: {saved_count} transcript(s) to {OUTPUT_DIR}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract Spotify podcast transcripts to text files"
    )
    parser.add_argument(
        "--show", "-s",
        help="Spotify show URL (e.g., https://open.spotify.com/show/xxx)"
    )
    parser.add_argument(
        "--episodes", "-e",
        nargs="+",
        help="Specific episode URLs (optional, overrides --show)"
    )
    parser.add_argument(
        "--max-results", "-m",
        type=int,
        default=50,
        help="Maximum number of episodes to extract (default: 50)"
    )
    
    args = parser.parse_args()
    
    if args.episodes:
        urls = args.episodes
    elif args.show:
        urls = [args.show]
    else:
        parser.error("Either --show or --episodes is required")
    
    transcripts = extract_transcripts(urls, args.max_results)
    save_transcripts(transcripts)


if __name__ == "__main__":
    main()