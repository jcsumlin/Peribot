import random

import aiohttp
from discord.ext import commands

from .utils.easyembed import embed


class Animal(commands.Cog):
    """Animal commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def cats(self, ctx):
        """Shows a cat"""
        search = "https://nekos.life/api/v2/img/meow"
        try:
            async with self.session.get(search) as r:
                result = await r.json()
            await ctx.send(embed=embed(image=result['url'], color=random.randint(0, 0xffffff)))
        except:
            await ctx.send("Couldnt Get An Image")

    @commands.command()
    async def catsbomb(self, ctx, amount : int = 5):
        """Throws a cat bomb!
        Defaults to 5"""
        search = "https://nekos.life/api/v2/img/meow"
        results = []
        if amount > 10 or amount < 1:
            amount = 5
        try:
            for x in range(0,amount):
                async with self.session.get(search) as r:
                    api_result = await r.json()
                    results.append(api_result['url'])
            for result in results:
                await ctx.send(embed=embed(image=result, color=random.randint(0, 0xffffff)))
        except:
            await ctx.send("Couldn't Get An Image")

    @commands.command()
    async def pugs(self, ctx):
        """Shows a pug"""
        search = "http://pugme.herokuapp.com/random"
        try:
            async with self.session.get(search) as r:
                result = await r.json()
            await ctx.send(embed=embed(image=result['pug'], color=random.randint(0, 0xffffff)))
        except:
            await ctx.send("Could Not Get An Image")

    @commands.command()
    async def pugsbomb(self, ctx, amount : int = 5):
        """Throws a pugs bomb!
        Defaults to 5"""
        search = "http://pugme.herokuapp.com/random"
        results = []
        if amount > 10 or amount < 1:
            amount = 5
        try:
            for x in range(0,amount):
                async with self.session.get(search) as r:
                    api_result = await r.json()
                    results.append(api_result['pug'])
            for result in results:
                await ctx.send(embed=embed(image=result, color=random.randint(0, 0xffffff)))
        except:
            await ctx.send("Couldnt Get An Image")

def setup(bot):
    n = Animal(bot)
    bot.add_cog(n)
