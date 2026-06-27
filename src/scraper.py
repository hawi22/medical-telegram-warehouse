import os
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from datetime import datetime
from datalake import get_partition_path, write_to_json, write_manifest, ensure_dir

# Load config
load_dotenv()
API_ID = os.getenv("TG_API_ID")
API_HASH = os.getenv("TG_API_HASH")

# Best Practice: Throttling constants
MSG_DELAY = 1.0  # Seconds between messages
CH_DELAY = 3.0   # Seconds between channels

# Setup Logging
ensure_dir("logs")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"logs/scrape_{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def scrape_channel(client, channel_username, base_path, date_str, limit=100):
    entity = await client.get_entity(channel_username)
    channel_name = channel_username.strip('@')
    
    # Image directory: data/raw/images/{channel_name}/
    img_dir = os.path.join(base_path, "raw", "images", channel_name)
    ensure_dir(img_dir)

    messages = []
    logger.info(f"Starting scrape for {channel_username}...")

    async for message in client.iter_messages(entity, limit=limit):
        img_path = None
        
        # Check for media (Photos only as per task)
        if message.media and isinstance(message.media, MessageMediaPhoto):
            img_path = os.path.join(img_dir, f"{message.id}.jpg")
            if not os.path.exists(img_path):
                await client.download_media(message, img_path)
        
        # Structured Data Collection
        msg_data = {
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": message.date.isoformat(),
            "message_text": message.text or "",
            "has_media": message.media is not None,
            "image_path": img_path,
            "views": message.views or 0,
            "forwards": message.forwards or 0
        }
        messages.append(msg_data)
        await asyncio.sleep(MSG_DELAY) # Polite Throttling

    # Save JSON partition
    file_path = os.path.join(get_partition_path(base_path, date_str), f"{channel_name}.json")
    write_to_json(file_path, messages)
    
    return len(messages)

async def main():
    channels = ['@CheMed123', '@LobeliaCosmetics', '@TikvahPharma'] # Add more from TGStat
    base_data_path = "data"
    today = datetime.now().strftime("%Y-%m-%d")
    
    async with TelegramClient('scraper_session', API_ID, API_HASH) as client:
        stats = {}
        for channel in channels:
            try:
                count = await scrape_channel(client, channel, base_data_path, today)
                stats[channel] = count
                await asyncio.sleep(CH_DELAY) # Inter-channel Throttling
            except FloodWaitError as e:
                logger.warning(f"Rate limit hit. Waiting {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"Error scraping {channel}: {e}")

        # Best Practice: Write manifest to finalize the ingestion
        write_manifest(base_data_path, today, stats)
        logger.info("Scraping Job Complete.")

if __name__ == "__main__":
    asyncio.run(main())