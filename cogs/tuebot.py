import discord
from discord.ext import commands
from BotMusic.BotMusic import Player

import ipdb
from typing import Optional


class TueBot(commands.Cog, Player):
    def __init__(self, client):
        super().__init__(client)
        self.context_dj = None
        self.logo = '🤖'

    @commands.command(name='song', brief='>song')
    async def song_now(self, ctx):
        try:
            song_now = self.data_current["data_song"]["title"]
            await ctx.send(f'**Now playing {song_now} :musical_note: ')
        except KeyError:
            await ctx.send('Queue Empty')

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='search')
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

    @commands.command(name='join', help='O bot entra na sala LUL')
    async def join(self, ctx):
        await ctx.message.delete()
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='play', aliases=['p', 'P', 'pl', 'ple', 'pley'], help='Comando para por musica ex: >play link')
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

    @commands.command(name='shuffle', help='randomizar a playlist')
    async def shuffle(self, ctx):
        self.shuffle_()
        await ctx.send('Shuffled :twisted_rightwards_arrows:')

    @commands.command(name='leave', help='Comando para o bot sair do canal')
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send('falÔo')
            await ctx.send('https://pbs.twimg.com/media/D63QUwcWkAEKd4a.jpg')

        except AttributeError:
            await ctx.send('Eu não to conectado sua putinha ')

    @commands.command(name='pause', help='Pausa a musica se estiver tocando *não me diga*')
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command(name='resume', help='Tira o pause do bot')
    async def resume(self, ctx):
        ctx.voice_client.resume()

    @commands.command(name='next')
    async def next(self, ctx):
        vc = ctx.voice_client
        vc.stop()

    @commands.command(name='repeat')
    async def reapeat(self, ctx):
        self.index -= 1
        await ctx.send('Song will repeat 🔁')

    @commands.command(name='previus')
    async def prev(self, ctx):
        self.index -= 2
        if self.index < 0:
            self.index = 0
        await self.next(ctx)

    @commands.command(name='stop')
    async def stop(self, ctx):
        self.index = 0
        self.queue.clear()

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='clear')
    async def clear_message(self, ctx, limit: Optional[int] = 1):
        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit)
                await ctx.send(f'Deleted {len(deleted)} messages', delete_after=5)
        else:
            await ctx.send('the limit provides is not within acceptable bounds.')

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('Pong! {0:.0f}'.format((self.client.latency * 1100)))

    @commands.command(name='help')
    async def too_command(self, ctx, *command: str):
        if command:
            command = command[0]
            comm = self.client.get_command(command)
            embed = discord.Embed(
                title=command,
                description=comm.help,
            )
            for arg in comm.__original_kwargs__:
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
    client.add_cog(TueBot(client))
