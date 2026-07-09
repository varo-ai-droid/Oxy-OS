# Spotify Podcast Transcript Extractor

Extracts transcripts from Spotify podcast episodes using the spotify_scraper library.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your Spotify sp_dc Cookie

Transcripts require authentication. Follow these steps:

1. **Log into Spotify** in your web browser (https://open.spotify.com)
2. **Open Developer Tools** (F12 or right-click -> Inspect)
3. Go to **Application** tab -> **Cookies** -> `https://open.spotify.com`
4. Find **`sp_dc`** in the cookie list
5. Copy the entire value (it's a long string starting with `AQD...`)
6. Paste it in the **root `.env`** file after `SPOTIFY_DC_COOKIE=`

### 3. Configure Environment
Edit the root `.env` file and add your cookie:
```env
SPOTIFY_DC_COOKIE=your_sp_dc_cookie_value_here
APIFY_API_TOKEN=your_apify_token_here  # Optional, for Apify scraper
```

## Usage

**Extract all transcripts from a podcast show:**
```bash
python extract_transcripts.py --show "https://open.spotify.com/show/78sy8vFEPjOxGdG4IGslh5"
```

**Extract specific episodes:**
```bash
python extract_transcripts.py --episodes "https://open.spotify.com/episode/xxx" "https://open.spotify.com/episode/yyy"
```

**Limit number of episodes:**
```bash
python extract_transcripts.py --show "https://open.spotify.com/show/xxx" --max-results 10
```

**Using Apify scraper (alternative):**
```bash
python extract_transcripts_apify.py --show "https://open.spotify.com/show/xxx"
```

## Output

Transcripts are saved to `raw/` folder with filenames: `YYYY-MM-DD - Episode Title.txt`

Each file contains:
- Episode title
- Episode URL  
- Published date
- Full transcript with timestamps (start_time-end_time: text)

## Notes

- Not all podcasts have transcripts available (Spotify is still rolling this feature out)
- The script will skip episodes without transcripts and report them
- Transcript quality depends on Spotify's auto-generated or creator-uploaded content

## Centralized Configuration

All environment variables are stored in the **root `.env` file** at the project level:
- `.env` - All secrets and credentials
- `.env.example` - Template for documentation purposes