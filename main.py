from telethon import TelegramClient
import os
import json
import asyncio
from datetime import datetime

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

api_id = config["api_id"]
api_hash = config["api_hash"]
messages = config["messages"]
start_time = datetime.strptime(config["start_time"], "%H:%M").time()
end_time = datetime.strptime(config["end_time"], "%H:%M").time()
interval_minutes = config["interval_minutes"]

client = TelegramClient("session_name", api_id, api_hash)

async def send_scheduled_messages():
    while True:
        now = datetime.now()
        if start_time <= now.time() <= end_time:
            print(f"[{now}] Sending messages to all groups...")
            for dialog in await client.get_dialogs():
                if dialog.is_group:
                    for message in messages:
                        await client.send_message(dialog.id, message)
            await asyncio.sleep(interval_minutes * 60)
        else:
            await asyncio.sleep(60)

async def main():
    # First time login if session not found
    if not os.path.exists("session_name.session"):
        print("First time login. Please enter your phone number and login code below.")
        await client.start()
    await send_scheduled_messages()

with client:
    client.loop.run_until_complete(main())
