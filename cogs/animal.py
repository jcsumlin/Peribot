import random

from discord.ext import commands

from .utils.easyembed import embed


class Animal:
    """Animal commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.http.session

    @commands.command()
    async def cats(self):
        """Shows a cat"""
        search = "https://nekos.life/api/v2/img/meow"
        try:
            async with self.session.get(search) as r:
                result = await r.json()
            await self.bot.say(embed=embed(image=result['url'], color=random.randint(0, 0xffffff)))
        except:
            await self.bot.say("Couldnt Get An Image")

    @commands.command()
    async def catsbomb(self, amount : int = 5):
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
                await self.bot.say(embed=embed(image=result, color=random.randint(0, 0xffffff)))
        except:
            await self.bot.say("Couldnt Get An Image")

    @commands.command()
    async def pugs(self):
        """Shows a pug"""
        search = "http://pugme.herokuapp.com/random"
        try:
            async with self.session.get(search) as r:
                result = await r.json()
            await self.bot.say(embed=embed(image=result['pug'], color=random.randint(0, 0xffffff)))
        except:
            await self.bot.say("Could Not Get An Image")

    @commands.command()
    async def pugsbomb(self, amount : int = 5):
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
                await self.bot.say(embed=embed(image=result, color=random.randint(0, 0xffffff)))
        except:
            await self.bot.say("Couldnt Get An Image")

def setup(bot):
    n = Animal(bot)
    bot.add_cog(n)