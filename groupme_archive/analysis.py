import csv
import logging
import os
import urllib.request
from pathlib import Path
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

def load_messages(csv_path: Path = Path('historic_messages.csv')) -> List[List[str]]:
    """Load messages from the historic_message csv file."""
    messages = []
    if not csv_path.exists():
        logger.error(f"File not found: {csv_path}")
        return []
        
    with open(csv_path, 'r', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for line in reader:
            messages.append(line)
    return messages

def extract_urls(messages: List[List[str]]) -> List[Tuple[str, str]]:
    """Given messages return all urls and their timestamps."""
    url_list = []
    for message in messages:
        # message[3] is the attachment URL string, message[4] is the timestamp
        if len(message) > 4 and message[3]:
            # Handle multiple URLs if present (comma separated)
            urls = message[3].split(',')
            for url in urls:
                url_list.append((url, message[4]))
    return url_list

def download_images(group_name: str, csv_path: Path = Path('historic_messages.csv'), output_dir: Optional[Path] = None):
    """Download symbols from archived messages."""
    messages = load_messages(csv_path)
    if not messages:
        return

    url_list = extract_urls(messages)
    
    if output_dir is None:
        output_dir = Path.cwd() / 'Images' / group_name
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Downloading {len(url_list)} images to {output_dir}")
    
    for i, (url, timestamp) in enumerate(url_list, 1):
        # Format filename: Frands MM-DD-YYYY@HH-MM-SS.gif
        safe_ts = timestamp.replace(':', '-').replace(' ', '@')
        filename = f"Frands {safe_ts}_{i}.gif"
        target_path = output_dir / filename
        
        if target_path.exists():
            continue
            
        try:
            urllib.request.urlretrieve(url, filename=target_path)
            if i % 10 == 0:
                logger.info(f"Downloaded {i}/{len(url_list)} images...")
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")

    logger.info("Image download complete.")
