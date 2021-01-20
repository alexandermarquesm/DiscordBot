import discord
from discord.ext import commands
from BotMusic.BotMusic import Player

import ipdb
from typing import Optional


class MusicianAgiota(commands.Cog, Player):
    def __init__(self, client):
        super().__init__(client)
        self.context_dj = None
        self.logo = '🤖'

    @commands.command(name='song', brief='show the song that is playing now', usage='>song')
    async def song_now(self, ctx):
        try:
            song_now = self.data_current["data_song"]["title"]
            await ctx.send(f'**Now playing {song_now} :musical_note: ')
        except KeyError:
            await ctx.send('Queue Empty')

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='search',
                      aliases=['s', 'srch', 'sarch'],
                      brief='shows the first 5 songs searched',
                      usage='>search [*song name or url]',
                      example='>search ghost bc\n>search https://www.youtube.com/watch?v=tMwmEcKVgtM'
                      )
    async def search_song(self, ctx, *, search):
        self.context_dj = ctx
        user_connected = ctx.author.voice
        if user_connected:
            five_songs = await self.search_api(search)
            mess_songs = await ctx.send(five_songs)
            reactions = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣')
            for react in reactions:
                await mess_songs.add_reaction(emoji=react)
        else:
            await ctx.send("You're not connected")

    @commands.command(name='join', brief='enter the voice chat that the user is connected to', usage='>join')
    async def join(self, ctx):
        await ctx.message.delete()
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='play', aliases=['p', 'P', 'pl', 'ple', 'pley'],
                      brief='command to play a song directly from youtube, get the first song if not url passed',
                      usage='>play [*song name or link]',
                      example='>play https://www.youtube.com/watch?v=gkBt7yLXyDk\n>play ghost bc year zero'
                              '\n>play https://www.youtube.com/watch?v=k5mX3NkA7jM&list=PLlCAnU1VQMzG9r-uKx'
                              'nFjYhi7z2gcjC89'
                      )
    async def play(self, ctx, *, link):

        if link not in 'youtube.com':
            link = self.get_song(link)

        channel = ctx.message.author.voice.channel
        bot_connection = ctx.voice_client
        if bot_connection:
            if bot_connection.is_playing():
                await self.add_links(link)
                await ctx.send(f':white_check_mark: Song {link} Added to playlist')
            else:
                await self.add_links(link)
                await ctx.send('Simbora')
                self.play_song(ctx)
        else:
            await channel.connect()
            await self.add_links(link)
            self.play_song(ctx)

    @commands.command(name='shuffle', brief='randomizes the playlist', usage='>shuffle')
    async def shuffle(self, ctx):
        self.shuffle_()
        await ctx.send('Shuffled :twisted_rightwards_arrows:')

    @commands.command(name='leave', brief='bot leave the voice channel', usage='>leave')
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send('falÔo')
            await ctx.send('https://pbs.twimg.com/media/D63QUwcWkAEKd4a.jpg')

        except AttributeError:
            await ctx.send('Eu não to conectado sua putinha ')

    @commands.command(name='pause', brief='pause the song if playing', usage='>pause')
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command(name='resume', brief='unpause the music', usage='>resume')
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command(name='next', brief='advances to the next song', usage='>next')
    async def next(self, ctx):
        vc = ctx.voice_client
        vc.stop()

    @commands.command(name='repeat', brief='repeat the current song', usage='>repeat')
    async def reapeat(self, ctx):
        self.index -= 1
        await ctx.send('Song will repeat 🔁')

    @commands.command(name='previous', brief='play the previous song', usage='>previous')
    async def prev(self, ctx):
        self.index -= 2
        if self.index < 0:
            self.index = 0
        await self.next(ctx)

    @commands.command(name='stop', brief='finish playing the playlist or the song if it is playing', usage='>stop')
    async def stop(self, ctx):
        self.index = 0
        self.queue.clear()

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='clear', brief='clears x amount of messages on the channel',
                      usage='>clear [amout] -> limit = 10',
                      example='>clear 20\n>clear 25\n>clear 50'
                      )
    async def clear_message(self, ctx, limit: Optional[int] = 1):
        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit)
                await ctx.send(f'Deleted {len(deleted)} messages', delete_after=5)
        else:
            await ctx.send('the limit provides is not within acceptable bounds.')

    @commands.command(name='help', usage='>help optional[command name]', example='>help\n>help wanted?\n>help play')
    async def too_command(self, ctx, *command: str):
        # ipdb.set_trace()
        if command:
            command = command[0]
            comm = self.client.get_command(command)
            embed = discord.Embed(
                title=command,
                description=comm.brief,
            )
            for arg in comm.__original_kwargs__:
                if arg in ['brief', 'name']:
                    continue
                embed.add_field(name=arg.capitalize(), value=f'`{comm.__original_kwargs__[arg]}`', inline=False)
            # fazer um for para adicionar os parametros das funçoes a cada laço
            # ex: aliases, brief, usage, help,
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Important link:',
                description='[TradingView](https://br.tradingview.com/symbols/BTCUSD/ "open TradingView Website")'
                            ' | [CoinMarketCap](https://coinmarketcap.com/ "open CoinMarketCap Website")'
                            ' | [ForDenise](https://www.youtube.com/watch?v=hH9M-m3WD0g)'
            )
            embed.set_author(name='📖 | Help Commands')

            for cog in self.client.cogs:
                if cog == 'CommandEvents':
                    continue
                comandos = ''
                for c in self.client.cogs[cog].walk_commands():
                    comandos += f'`{c}` | '
                embed.add_field(name=f'{self.client.get_cog(cog).logo} {cog}', value=comandos, inline=False)

            embed.set_footer(text='to get more info on commands >help [command]')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(MusicianAgiota(client))
