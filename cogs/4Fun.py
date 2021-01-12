from discord.ext import commands
import discord
from random import choice, randint
from Memes import MemesScrapy
from PIL import Image
from io import BytesIO


class FourFun(commands.Cog, MemesScrapy.MemeWinTrade):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.logo = '🎉'

    @commands.command(name='wanted?', help='verify that you are wanted', usage='>wanted?')
    async def wanted(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        
        wanted = Image.open('wanted.jpg')

        asset = ctx.author.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((600, 600))

        wanted.paste(pfp, (340, 625))

        wanted.save('profile.jpg')

        await ctx.send(file=discord.File('profile.jpg'))

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='tag')
    async def reddit_tag(self, ctx, *tag):
        if tag:
            tag = tag[0]
        else:
            tag = 'meme'
        await ctx.send(self.get_random_meme(tag), delete_after=2)

    @commands.command(name='ÉOPAPI', help='Comando que consiste em mostrar a formatura do papi KEKW')
    async def papi(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/532609612420087828/784573727554666501/aham.png')

    @commands.command(name='eusou?', help='Digita ae pa tu ve')
    async def eusou(self, message):
        op = ['MANO, TU É 🤔?', 'AQUI É SUPER XANDÃO 🤠', 'EU SO PIKA BOTA NO ALTO 😎', 'É O PAAAPII AQUI PORRAA 🤓',
              'SEM PRESSÃO AQUI É XANDÃO 😎', 'UUuuuuuUuUUUUUUUUUUUUUUUUUUUUU', 'Abigo estoy aqui', 'Un Bandolero',
              'Tem CÁS tentro 🥤', 'Cás? 🥤', 'BUCETEIRO DE MERDA MESMO 🤮']
        await message.send(choice(op))

    @commands.command(name='rolladice', help='Rodar um dado :LUL:')
    async def roll(self, ctx):
        number = randint(0, 9)
        await ctx.send(f'Caiu no número {number}')

    @commands.command(name='rir', help='Commando que vai rir por você LUL')
    async def rir(self, ctx):
        risada = 100 * 'K'
        await ctx.send(risada)


def setup(client):
    client.add_cog(FourFun(client))
