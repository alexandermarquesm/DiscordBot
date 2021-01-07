import praw
from random import choice
import json
from discord.ext import commands


class MemeWinTrade:
    user_values = {'client_id': 'SNdADgMxCYfgWw',
                   'client_secret': 'pQd8F0DoikGh1WmOxPFoiBaWWH0HCw',
                   'user_agent': 'Memes scrape',
                   'user_name': 'Gangplank_Gaucho',
                   'user_password': 'desktop3348'}

    def __init__(self):
        self.tag_list = []
        self.reddit = praw.Reddit(client_id=self.user_values['client_id'],
                                  client_secret=self.user_values['client_secret'],
                                  user_agent=self.user_values['user_agent'],
                                  user_name=self.user_values['user_name'],
                                  user_password=self.user_values['user_password'])

    def get_meme_reddit(self, tag):
        self.tag_list.clear()
        for meme in self.reddit.subreddit(tag).hot(limit=10):
            if 'jpg' in meme.url.lower() or 'png' in meme.url.lower():
                self.tag_list.append(meme.url)

    def get_random_meme(self, tag):
        self.get_meme_reddit(tag)
        return choice(self.tag_list)
