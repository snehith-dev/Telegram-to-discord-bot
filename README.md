# 🤖 Telegram to Discord Forwarder Bot

This bot automatically forwards **messages**, **photos**, and **videos** from a specified **Telegram channel or group** to a **Discord channel**.

## ✨ Features

- 📩 Forwards **text messages**
- 🖼️ Sends **photos** with captions (if available)
- 🎥 Shares **videos** to Discord
- 🔒 Option to filter messages by keywords (optional)
- 🔁 Real-time message forwarding
- 🛠️ Easy to configure and deploy

## 📦 Requirements

- Python 3.8+
- Telegram Bot Token
- Telegram Chat ID (group/channel)
- Discord Bot Token
- Discord Channel ID

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/snehith-dev/Telegram-to-discord-bot.git

## Install dependencies
pip install -r requirements.txt

## Set up configuration
Create a .env file or edit config.py with the following:
- TELEGRAM_BOT_TOKEN=your_telegram_bot_token
- TELEGRAM_CHAT_ID=your_telegram_chat_id
- DISCORD_BOT_TOKEN=your_discord_bot_token
- DISCORD_CHANNEL_ID=your_discord_channel_id

## 🧠 How It Works
The bot listens for new messages in a Telegram chat using the Telegram Bot API and forwards them to a specified Discord channel using Discord Webhooks or the Discord API.
### It handles:
- Message parsing
- Media downloading from Telegram
- Uploading to Discord

## 🛡️ Permissions
### Make sure:
- Your Telegram bot is an admin in the group or channel you're monitoring.
- Your Discord bot has permissions to send messages and upload files to the target channel.

## How To Run 
```bash
python tg_to_discord.py
