ztnet-webhook-telegram-bot

This repository contains a Python-based webhook listener designed for the ztnet app. 
It listens for incoming webhook events from ztnet and forwards them to a specified Telegram chat using a Telegram bot.

Features

Listens for incoming webhook events from ztnet.
Formats and sends event data as a message to a specified Telegram chat.
Configurable with environment variables for the Telegram bot token and chat IDs.



Docker Setup

To run the webhook listener inside a Docker container, you can use the provided Dockerfile:

docker build -t ztnet-webhook-telegram-bot .
docker run -p 5000:5000 --env TELEGRAM_BOT_TOKEN="your-bot-token" --env TELEGRAM_CHAT_IDS="your-chat-id" ztnet-webhook-telegram-bot
