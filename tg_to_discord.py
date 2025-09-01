import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import discord
import asyncio

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = 'YOUR TELEGRAM BOT TOKEN'
TELEGRAM_CHAT_ID = 'YOUR CHAT ID'  # The chat/channel/group to listen to
DISCORD_BOT_TOKEN = 'YOUR DISCORD BOT TOKEN'
DISCORD_CHANNEL_ID = YOUR DISCORD CHANNEL ID  # Enter normally no need '' 

# --- Discord Setup ---
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

discord_ready = asyncio.Event()

def run_discord_bot():
    asyncio.run(client.start(DISCORD_BOT_TOKEN))

@client.event
async def on_ready():
    print(f'Discord bot logged in as {client.user}')
    for guild in client.guilds:
        print(f'Guild: {guild.name} (ID: {guild.id})')
        for channel in guild.text_channels:
            print(f'  Channel: {channel.name} (ID: {channel.id})')
    discord_ready.set()

async def send_to_discord(content=None, file_path=None, filename=None):
    await discord_ready.wait()
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        print('Discord channel not found!')
        return
    if file_path:
        with open(file_path, 'rb') as f:
            await channel.send(content, file=discord.File(f, filename=filename))
    else:
        await channel.send(content)

# --- Telegram Handlers ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        return
    text = update.effective_message.text or update.effective_message.caption

    # Handle photos
    if update.effective_message.photo:
        photo = update.effective_message.photo[-1]  # Best quality
        file = await context.bot.get_file(photo.file_id)
        file_path = f"temp_{photo.file_id}.jpg"
        await file.download_to_drive(file_path)
        await send_to_discord(content=text, file_path=file_path, filename=os.path.basename(file_path))
        os.remove(file_path)
        return

    # Handle videos
    if update.effective_message.video:
        video = update.effective_message.video
        file = await context.bot.get_file(video.file_id)
        file_path = f"temp_{video.file_id}.mp4"
        await file.download_to_drive(file_path)
        await send_to_discord(content=text, file_path=file_path, filename=os.path.basename(file_path))
        os.remove(file_path)
        return

    # Handle text only
    if text:
        await send_to_discord(content=text)

async def main():
    # Start Discord bot as a background task
    discord_task = asyncio.create_task(client.start(DISCORD_BOT_TOKEN))

    # Start Telegram bot using low-level API
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print('Telegram bot started.')

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    try:
        await discord_task  # Keep running until Discord bot stops
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) 
