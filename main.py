import discord
from dotenv import load_dotenv
import os
from use_cases import UseCase

load_dotenv()
client = discord.Client()
SEARCH_LIMIT = 500

@client.event
async def on_message(cur_message):
    if cur_message.content in ["count", "random", "gatcha", "roulette"]:
        episode_channel = client.get_channel(int(os.environ.get('CHANNEL_ID')))
        messages = await episode_channel.history(limit=SEARCH_LIMIT).flatten()

        message = ""
        additional_message = ""

        if cur_message.content == "count":
            message = UseCase.message_counter(messages)

        elif cur_message.content == "random":
            message = UseCase.random_episode(messages)

        elif cur_message.content == "gatcha":
            username = cur_message.author.nick if cur_message.author.nick else cur_message.author.name
            message = UseCase.gatcha(messages, username)

        elif cur_message.content == "roulette":
            roulette_messages = UseCase.roulette()
            if roulette_messages:
                message, additional_message = roulette_messages

        if message:
            await cur_message.channel.send(message)

        if additional_message:
            await cur_message.channel.send(additional_message)

if __name__ == '__main__':
    discord_token = os.environ.get('DISCORD_TOKEN')
    client.run(discord_token)
