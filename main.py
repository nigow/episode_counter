import discord
from dotenv import load_dotenv
import os
import random

load_dotenv()
client = discord.Client()
SEARCH_LIMIT = 500

@client.event
async def on_message(cur_message):
    episode_channel = client.get_channel(int(os.environ.get('CHANNEL_ID')))
    messages = await episode_channel.history(limit=SEARCH_LIMIT).flatten()

    if cur_message.content == "count":
        counter = 0
        for message in messages:
            counter += message.content.count('\n・')
            if len(message.content) > 0:
                counter += 1 if message.content[0] == "・" else 0
        await cur_message.channel.send(f'現在のエピソードは{counter}話です。')

    elif cur_message.content == "random":
        all_episodes = []
        for message in messages:
            content = message.content
            if "・" in content:
                # a random episode should not contain "・" prefix
                if content[0] == "・":
                    content = content[1:]
                parsed_message = content.split('\n・')

                # make sure there are no empty strings
                parsed_message = list(filter(None, parsed_message))
                all_episodes.extend(parsed_message)
        random_episode = random.choice(all_episodes)
        await cur_message.channel.send(random_episode)

if __name__ == '__main__':
    discord_token = os.environ.get('DISCORD_TOKEN')
    client.run(discord_token)
