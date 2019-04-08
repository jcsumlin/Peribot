from discord.ext import commands
from loguru import logger
import giphypop
import discord
import random



class CursedPearl:
    def __init__(self, bot):
        self.bot = bot


    def serverCheck(self, ctx):
        if ctx.message.server.id == '515370084538253333':
            return True
        else: return False

    @commands.command(pass_context=True, no_pm=True)
    async def levels(self, ctx):
        if self.serverCheck(ctx):
            await self.bot.send_file(ctx.message.channel, "data/card.png")

    @commands.command(pass_context=True, no_pm=True)
    async def rank(self, ctx):
        if self.serverCheck(ctx):
            await self.bot.send_file(ctx.message.channel, "data/card.png")

    @commands.command(pass_context=True, no_pm=True)
    async def peridot(self, ctx):
        if self.serverCheck(ctx):
            g = giphypop.Giphy("KZciiXBwyJ9RabyZyUHjQ8e4ZutZQ1Go")
            results = [x for x in g.search('Peridot')]
            embed = discord.Embed(color=0xe6e200)
            embed.set_image(url=random.choice(results).raw_data['images']['fixed_height_downsampled']['url'])
            embed.set_footer(text="This is a random gif from Giphy using the search term 'Peridot'")
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(CursedPearl(bot))
