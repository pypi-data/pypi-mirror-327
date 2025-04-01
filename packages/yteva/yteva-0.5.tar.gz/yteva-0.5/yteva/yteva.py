import aiohttp
import asyncio
from pyrogram import Client

class YTeva:
    def __init__(self, api_key: str, bot_app, max_retries=5, retry_delay=2):
        self.api_key = api_key
        self.bot_app = bot_app
        self.channel = "datdtst44"
        self.session = aiohttp.ClientSession()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def fetch_audio_link(self, video_id: str):
        url = f"http://127.0.0.1:8000/get_audio/{video_id}?api_key={self.api_key}"
        for attempt in range(self.max_retries):
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    telegram_link = data.get("telegram_link")
                    if telegram_link:
                        return telegram_link
            print(f"Retry {attempt + 1}/{self.max_retries}: Retrying in {self.retry_delay} seconds...")
            await asyncio.sleep(self.retry_delay)
        raise Exception("Failed to fetch audio link after multiple retries")

    async def download_audio(self, video_id: str):
        telegram_link = await self.fetch_audio_link(video_id)
        message_id = int(telegram_link.split("/")[-1])
        msg = await self.bot_app.get_messages(self.channel, message_id)
        downloaded_file = await msg.download(file_name=f"downloads/{video_id}.m4a")
        return [downloaded_file, False]

    async def close(self):
        await self.session.close()
