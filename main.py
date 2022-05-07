import discord
from dotenv import load_dotenv
import os

load_dotenv()
client = discord.Client()


@client.event
async def on_message(cur_message):
    if cur_message.content == "count":
        episode_channel = client.get_channel(int(os.environ.get('CHANNEL_ID')))
        messages = await episode_channel.history(limit=500).flatten()
        counter = 0
        for message in messages:
            counter += message.content.count('\n・')
            counter += 1 if message.content[0] == "・" else 0
        await cur_message.channel.send(f'現在のエピソードは{counter}話です。')


if __name__ == '__main__':
    discord_token = os.environ.get('DISCORD_TOKEN')
    client.run(discord_token)
