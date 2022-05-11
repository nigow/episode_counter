import discord
from dotenv import load_dotenv
import os
import random
from use_cases import UseCase

load_dotenv()
client = discord.Client()
SEARCH_LIMIT = 500

@client.event
async def on_message(cur_message):
    if cur_message.content in ["count", "random", "gatcha"]:
        episode_channel = client.get_channel(int(os.environ.get('CHANNEL_ID')))
        messages = await episode_channel.history(limit=SEARCH_LIMIT).flatten()

        message = ""

        if cur_message.content == "count":
            message = UseCase.message_counter(messages)

        elif cur_message.content == "random":
            message = UseCase.random_episode(messages)

        elif cur_message.content == "gatcha":
            username = cur_message.author.nick if cur_message.author.nick else cur_message.author.name
            message = UseCase.gatcha(messages, username)

        if message:
            await cur_message.channel.send(message)

if __name__ == '__main__':
    discord_token = os.environ.get('DISCORD_TOKEN')
    client.run(discord_token)
