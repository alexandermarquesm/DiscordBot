import asyncio
from pytube import Playlist, YouTube
import ipdb
from datetime import timedelta
import discord
from random import shuffle
from GoogleAPIs.YoutubeApi import YoutubeSearch
import isodate


class Queue:
    ffmpeg_options = {
        'options': '-vn'
    }

    def __init__(self):
        self.queue = []
        self.index = 0

    def put(self, item):
        self.queue.extend(item)

    def get(self):
        try:
            return self.queue[self.index]
        except IndexError as e:
            raise e

    def shuffle_(self):
        shuffle(self.queue)

    def peek(self):
        return self.queue


class Player(Queue, YoutubeSearch):
    def __init__(self, client):
        super().__init__()
        self.client = client

        self.data_current = {}
        self.five_songs_ids = []

    async def markdown_queue(self, data):
        five_songs = ''
        for n, v in enumerate(data):
            five_songs += f"{v['number']:>2})  {v['title'][:61]:61}  {v['duration']:7}\n"
            self.five_songs_ids.append({"number": data[n]["number"], "link": self.youtube_query + data[n]["id"]})
        five_songs = f'```py\n{five_songs}```'
        return five_songs

    async def search_api(self, string):
        data_search = self.search(string)
        return await self.markdown_queue(data_search)

    async def add_links(self, url):
        try:
            playlist = Playlist(url)
            self.queue.extend(playlist)
        except KeyError:
            self.queue.append(url)

    @staticmethod
    async def add_reaction_player(message):
        emojis = ('⏮', '⏹', '▶', '⏸', '⏭', '🔁')
        for reaction in emojis:
            await message.add_reaction(emoji=reaction)

    def data_song(self, url):
        song = YouTube(url)
        self.data_current['data_song'] = {
            'player': song.streams.get_by_itag(251).default_filename,
            'title': song.title,
            'thumb': song.thumbnail_url,
            'author': song.author,
            'time': timedelta(seconds=song.length),
            'url': song.watch_url,
            'views': song.views
        }
        song.streams.get_by_itag(251).download()

    async def embed_song(self, bot):
        embedsong = discord.Embed(title=f':musical_note: `{self.data_current.get("data_song")["title"]}`',
                                  color=0xf5dc00, url=self.data_current.get("data_song")["url"])
        embedsong.set_thumbnail(url=self.data_current.get("data_song")['thumb'])
        embedsong.set_author(name=f'{self.data_current.get("data_song")["author"]}')
        embedsong.add_field(name=':watch:Time', value=f'`{self.data_current.get("data_song")["time"]}`')
        embedsong.add_field(name=':face_with_monocle: Views', value=f'`{self.data_current.get("data_song")["views"]}`')
        embedsong.set_footer(icon_url=bot.author.avatar_url, text=f'Requested by {bot.author.name}')
        message = await bot.send(embed=embedsong)
        await self.add_reaction_player(message)

    def next_song(self):
        self.data_song(self.get())
        self.index += 1

    def play_song(self, ctx):
        try:
            self.next_song()
            asyncio.run_coroutine_threadsafe(self.embed_song(ctx), self.client.loop)
            source = discord.FFmpegPCMAudio(self.data_current.get('data_song')['player'], **self.ffmpeg_options)
            ctx.voice_client.play(source, after=lambda x: self.play_song(ctx))
        except IndexError:
            asyncio.run_coroutine_threadsafe(ctx.send('Fim da Playlist <:ResidentSleeper:442472326303580161>',
                                                      delete_after=5),
                                             self.client.loop)
