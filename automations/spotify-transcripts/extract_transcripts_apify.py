#!/usr/bin/env python3
"""
Spotify Podcast Transcript Extractor (Apify version)
Uses Apify Podcast Transcript Scraper to extract transcripts.
"""

import os
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from root .env
load_dotenv(Path(__file__).parent.parent / '.env')

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
OUTPUT_DIR = Path(__file__).parent / "raw"
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_transcripts_apify(urls: list[str], max_results: int = 50) -> list[dict]:
    """Extract transcripts using Apify Podcast Transcript Scraper."""
    if not APIFY_TOKEN:
        raise ValueError(
            "APIFY_API_TOKEN not found in .env file. "
            "Please add your Apify API token to run the Apify scraper."
        )
    
    from apify_client import ApifyClient
    
    client = ApifyClient(APIFY_TOKEN)
    
    # Try the main podcast transcript scraper actor
    run_input = {
        "urls": urls,
        "maxResults": max_results
    }
    
    print(f"Starting Apify actor run...")
    
    try:
        run = client.actor("consummate_mandala/podcast-transcript-scraper").call(
            run_input=run_input
        )
    except Exception as e:
        print(f"Error with consummate_mandala actor: {e}")
        print("Trying alternative: taroyamada/spotify-podcast-intelligence")
        run_input = {"url": urls[0]}
        run = client.actor("taroyamada/spotify-podcast-intelligence").call(
            run_input=run_input
        )
    
    print(f"Actor run completed with ID: {run['id']}")
    
    results = []
    dataset = client.dataset(run["defaultDatasetId"])
    
    for item in dataset.iterate_items():
        results.append(item)
    
    return results


def save_transcripts(transcripts: list[dict]) -> None:
    """Save transcripts to individual files in the raw folder."""
    saved_count = 0
    
    for transcript in transcripts:
        title = transcript.get("episodeTitle", transcript.get("name", "unknown"))
        episode_url = transcript.get("episodeUrl", transcript.get("url", ""))
        
        safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()[:50]
        pub_date = transcript.get("publishDate", transcript.get("publish_date", ""))
        date_str = pub_date[:10] if pub_date else datetime.now().strftime("%Y-%m-%d")
        
        filename = f"{date_str} - {safe_title}.txt"
        filepath = OUTPUT_DIR / filename
        
        transcript_text = transcript.get("transcript", transcript.get("text", ""))
        
        if transcript_text:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Episode: {title}\n")
                f.write(f"URL: {episode_url}\n")
                f.write(f"Published: {pub_date}\n")
                f.write("=" * 80 + "\n\n")
                f.write(transcript_text)
            
            print(f"Saved: {filename}")
            saved_count += 1
    
    print(f"\nSaved {saved_count} transcript(s) to {OUTPUT_DIR}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract Spotify podcast transcripts using Apify"
    )
    parser.add_argument(
        "--show", "-s",
        required=True,
        help="Spotify show URL (e.g., https://open.spotify.com/show/xxx)"
    )
    parser.add_argument(
        "--max-results", "-m",
        type=int,
        default=50,
        help="Maximum number of episodes to extract (default: 50)"
    )
    
    args = parser.parse_args()
    
    print(f"Extracting transcripts for: {args.show}")
    
    try:
        transcripts = extract_transcripts_apify([args.show], args.max_results)
        save_transcripts(transcripts)
    except ValueError as e:
        print(f"Error: {e}")
        print("Make sure APIFY_API_TOKEN is set in .env file")


if __name__ == "__main__":
    main()