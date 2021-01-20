from lolchamps.fetch import Analize
from discord.ext import commands
from discord import Embed


class LOLRune(commands.Cog, Analize):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.logo = ':rainbow:'

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='att db')
    async def atualizar_database(self, ctx):
        from lolchamps.spider import MainSpider
        from scrapy.crawler import CrawlerProcess
        spiderlol = CrawlerProcess()
        spiderlol.crawl(MainSpider)
        spiderlol.start()
        await ctx.send('DATABASE HAS BEEN UPDATED')

    @commands.command(name='rune',
                      aliases=['runa'],
                      brief='shows the current runes of the champion',
                      usage='>rune [name champ]',
                      example='>rune lee sin\n>rune lux\n>rune gangplank'
                      )
    async def rune(self, ctx, *,
                   name: str):
        champs = self.choose_champ(name)[0]
        embed = Embed()
        runes = ''

        for champ in champs.items():
            if champ[0] == 'name':
                embed.title = f'RUNE {champ[1][0].upper()}'
                continue
            for champ1 in champ[1]:
                runes += f' | `{champ1}`'

            embed.add_field(name=champ[0].upper(), value=runes, inline=False)
            runes = ''

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(LOLRune(client))
