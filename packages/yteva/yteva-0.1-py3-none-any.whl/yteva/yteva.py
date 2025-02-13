import requests
import asyncio
from pyrogram import Client

class YTeva:
    def __init__(self, api_key: str, bot_app: Client):
        self.api_key = api_key
        self.bot_app = bot_app
        self.channel = "datdtst44"

    async def download_audio(self, video_id: str):
        url = f"http://127.0.0.1:8000/get_audio/{video_id}?api_key={self.api_key}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception("Failed to fetch audio link from API")
        
        telegram_link = response.json().get("telegram_link")
        if not telegram_link:
            raise Exception("Invalid response from API")
        
        message_id = int(telegram_link.split("/")[-1])
        msg = await self.bot_app.get_messages(self.channel, message_id)
        downloaded_file = await msg.download(file_name=f"downloads/{video_id}.m4a")
        
        return [downloaded_file, False]
    