from random import randint, shuffle
from typing import List


class Episode:
    def __init__(self, episode: str, rank: str):
        self.episode = episode
        self.rank = rank

    def __str__(self):
        return f"{self.rank} - {self.episode}"


class EpisodeDeck:
    def __init__(self):
        self.r = []
        self.sr = []
        self.ssr = []

    def add_episode(self, episode: str, rank: str):
        possible_ranks = ['R', 'SR', 'SSR']
        if rank in possible_ranks:
            if rank == 'R':
                self.r.append(episode)
            elif rank == 'SR':
                self.sr.append(episode)
            elif rank == 'SSR':
                self.ssr.append(episode)

    def roll_ten_gatchas(self, username: str) -> str:
        episodes = []  # type: List[Episode]
        for _ in range(9):
            current_episode = self._roll_gatcha()
            episodes.append(current_episode)

        # if all episodes are R, add a random SR
        if all(e.rank == 'R' for e in episodes):
            random_episode_content = self.sr[randint(0, len(self.sr) - 1)]
            random_episode_rank = "SR"
            random_episode = Episode(random_episode_content, random_episode_rank)
            episodes.append(random_episode)

        # if at least one episode is SR or SSR, just roll a random episode
        else:
            last_episode = self._roll_gatcha()
            episodes.append(last_episode)
        shuffle(episodes)

        # generate the message with gatcha results
        message = f"エピソードアーカイブガシャ1日1回10連無料キャンペーン中!!\n{username}さんの本日の結果はこちら!!\n\n"
        for e in episodes:
            message += f"{e.rank} - {e.episode}\n"
        return message

    def _roll_gatcha(self) -> Episode:
        random_number = randint(1, 100)
        # SSR
        if random_number <= 3:
            random_episode_content = self.ssr[randint(0, len(self.ssr) - 1)]
            random_episode_rank = "SSR"

        # SR
        elif random_number <= 12:
            random_episode_content = self.sr[randint(0, len(self.sr) - 1)]
            random_episode_rank = "SR"

        # R
        else:
            random_episode_content = self.r[randint(0, len(self.r) - 1)]
            random_episode_rank = "R"

        return Episode(random_episode_content, random_episode_rank)
