import discord
import discord.errors
from GoogleAPIs import crypt
from discord.ext import commands, tasks


class CommandEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        cr = crypt.Crpyo()
        status = await cr.get_cryptocurrency()
        await self.client.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game(status['Bitcoin'])
        )
        print('O pai ta on 😎')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == 238859922274648084 or user.id == 320654747633844226 or user.id == 233781462485172224:
            tuebot = self.client.get_cog('TueBot')
            ctx = await self.client.get_context(reaction.message)
            if reaction.emoji == '⏸':
                await reaction.message.remove_reaction('⏸', user)
                await tuebot.pause(ctx)
            elif reaction.emoji == '⏮':
                await reaction.message.clear_reactions()
                await tuebot.prev(ctx)
            elif reaction.emoji == '⏹':
                await reaction.message.clear_reactions()
                await tuebot.stop(ctx)
                await tuebot.next(ctx)
            elif reaction.emoji == '▶':
                await reaction.message.remove_reaction('▶', user)
                await tuebot.resume(ctx)
            elif reaction.emoji == '⏭':
                await reaction.message.clear_reactions()
                await tuebot.next(ctx)
            elif reaction.emoji == '🔁':
                await reaction.message.remove_reaction('🔁', user)
                await tuebot.reapeat(ctx)
            elif reaction.emoji == '1️⃣':
                await reaction.message.clear_reactions()
                link = tuebot.five_songs_ids[0]["link"]
                await tuebot.play(tuebot.context_dj, link=link)
                tuebot.five_songs_ids.clear()
            elif reaction.emoji == '2️⃣':
                await reaction.message.clear_reactions()
                link = tuebot.five_songs_ids[1]["link"]
                await tuebot.play(tuebot.context_dj, link=link)
                tuebot.five_songs_ids.clear()
            elif reaction.emoji == '3️⃣':
                await reaction.message.clear_reactions()
                link = tuebot.five_songs_ids[2]["link"]
                await tuebot.play(tuebot.context_dj, link=link)
                tuebot.five_songs_ids.clear()
            elif reaction.emoji == '4️⃣':
                await reaction.message.clear_reactions()
                link = tuebot.five_songs_ids[3]["link"]
                await tuebot.play(tuebot.context_dj, link=link)
                tuebot.five_songs_ids.clear()
            elif reaction.emoji == '5️⃣':
                await reaction.message.clear_reactions()
                link = tuebot.five_songs_ids[4]["link"]
                await tuebot.play(tuebot.context_dj, link=link)
                tuebot.five_songs_ids.clear()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have the permission to do that")

        if isinstance(error, commands.CommandNotFound):
            await ctx.send('This is not a command')
            await ctx.send('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/80c977ea-f882-4329-8151-3f7670a390e0/ddyz5ku-aedf592f-f732-4e70-9111-f218dc5ea207.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvODBjOTc3ZWEtZjg4Mi00MzI5LTgxNTEtM2Y3NjcwYTM5MGUwXC9kZHl6NWt1LWFlZGY1OTJmLWY3MzItNGU3MC05MTExLWYyMThkYzVlYTIwNy5qcGcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.aVDczqHMaQk8smkj9oaRajGWLlltfi-xaglST5m1zgw')

        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.__context__.__class__(), discord.errors.ClientException):
                await ctx.send('Already connected to a voice channel')
            if isinstance(error.__context__.__class__(), AttributeError):
                await ctx.send("You're not connected")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Required argument')

        raise error


def setup(client):
    client.add_cog(CommandEvents(client))
