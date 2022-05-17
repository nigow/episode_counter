import csv

from discord import Message
from typing import List, Union, Tuple
import random
from entity import EpisodeDeck, Roulette
from utility import divide_by_delimiter
import os

# set up constants

# every number emoji has the following unicode as its suffix
NUMBER_EMOJI_SUFFIX = '\ufe0f\u20e3'

# SSR should be more than 4 reactions
SSR_THRESHOLD = 4

# SR should be more than 1 reaction
SR_THRESHOLD = 1

# Setting file for roulette config
ROULETTE_PATH = 'roulette.csv'


class UseCase:
    @staticmethod
    def message_counter(messages: List[Message]) -> str:
        """
        Helper function to count the number of messages
        """
        counter = 0
        for message in messages:
            counter += message.content.count('\n・')
            if len(message.content) > 0:
                counter += 1 if message.content[0] == "・" else 0
        message = f'現在のエピソードは{counter}話です。'
        return message

    @staticmethod
    def random_episode(messages: List[Message]) -> str:
        """
        Helper function to get a random episode
        """
        all_episodes = []
        for message in messages:
            if "・" in message.content:
                parsed_message = divide_by_delimiter(message.content)
                all_episodes.extend(parsed_message)
        random_episode = random.choice(all_episodes)
        return random_episode

    @staticmethod
    def gatcha(messages: List[Message], username) -> str:
        """
        Helper function to roll a gatcha
        """
        all_episodes = EpisodeDeck()

        def __add_episode(episode: str, count: int):
            if count >= SSR_THRESHOLD:
                all_episodes.add_episode(episode, 'SSR')
            elif count >= SR_THRESHOLD:
                all_episodes.add_episode(episode, 'SR')
            else:
                all_episodes.add_episode(episode, 'R')

        for message in messages:
            if message.content:
                parsed_message = divide_by_delimiter(message.content)
                if message.reactions:
                    # check if someone reacted with a number emoji
                    if any(reaction.emoji and NUMBER_EMOJI_SUFFIX in reaction.emoji for reaction in message.reactions):
                        # multiple entries may be elected for higher classes
                        reacted_indecies = []
                        for reaction in message.reactions:
                            if NUMBER_EMOJI_SUFFIX in reaction.emoji:
                                index = int(reaction.emoji[0]) - 1
                                try:
                                    __add_episode(parsed_message[index], int(reaction.count))
                                # skip error handling for now
                                except IndexError:
                                    pass
                                reacted_indecies.append(index)
                        # remove the reacted indecies from the message
                        for index in reacted_indecies:
                            # TODO: fix this: popping multiple elements by addressing the contents instead of index
                            parsed_message.pop(index)

                    else:
                        # if no number emoji is found, the highest count would attribute to the first episode
                        max_reaction_counts = max(reaction.count for reaction in message.reactions)
                        __add_episode(parsed_message[0], max_reaction_counts)
                        parsed_message.pop(0)

                # all the remaining episodes are added as R
                [all_episodes.add_episode(m, 'R') for m in parsed_message]

        result = all_episodes.roll_ten_gatchas(username)
        return result

    @staticmethod
    def roulette() -> Union[Tuple[str, str], None]:
        setting_exists = os.path.exists(ROULETTE_PATH)
        if setting_exists:
            with open(ROULETTE_PATH) as f:
                roulette_settings = list(csv.reader(f))
                roulette = Roulette(roulette_settings)
                emoji_string, score_string = roulette.roll()
                return emoji_string, score_string
