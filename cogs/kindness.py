from discord.ext import commands
import random
import discord
from .utils.dataIO import dataIO
import json
import os, os.path


class Kindness:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def kiss(self, ctx, victim):
        kisser = ctx.message.author.mention
        msg = random.choice(dataIO.load_json("data/lewd/kiss.json")['kiss'])
        await self.bot.say(msg.format(kisser=kisser,victim=victim))

    @commands.command("hug", pass_context=True)
    async def hug(self, ctx, victim: discord.Member, number=None):
        count = sum([len(files) for r, d, files in os.walk("cogs/data/lewd/hugs")])
        if number is None:
            file = str(random.randint(1,30)) + '.gif'
        else:
            file = str(number) + '.gif'
        area = ctx.message.channel
        author = ctx.message.author.mention
        # embed = discord.Embed(title=author+'hugs'+victim.mention)
        # embed.set_image(url=)
        with open('data/lewd/hugs/'+file, 'rb') as file:
            await self.bot.send_file(area, file)

    @commands.command(pass_context=True)
    async def compliment(self, ctx, target):
        msg = random.choice(dataIO.load_json("data/compliment/compliments.json")['compliments'])
        await self.bot.say(str(target) + ' ' + msg)


def setup(bot):
    n = Kindness(bot)
    bot.add_cog(n)