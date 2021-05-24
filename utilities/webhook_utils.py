import discord
import discord_webhook
import requests
from discord import Webhook, RequestsWebhookAdapter

async def sendWebhook(channel, name, pfp, message):
    webhook = await channel.create_webhook(name=name)
    await webhook.send(message, avatar_url=pfp)
    await webhook.delete()