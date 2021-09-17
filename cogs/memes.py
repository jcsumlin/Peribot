import urllib.parse

import discord
from discord.ext import commands

from .utils.genericResponseBuilder import commandError
from .utils.memegenerator import make_meme


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bill(self, ctx, *, text):
        """
        Pong!
        """
        base_url = "https://belikebill.ga/billgen-API.php?text=This%20is%20Bill%0D%0A" + urllib.parse.quote(text) + "%0D%0ABe%20Like%20Bill"
        embed = discord.Embed().set_image(url=base_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def kobayashi(self, ctx, *, text):
        try:
            img = await self.make_meme_from_template("data/memes/zvlmhl1iw77412.jpeg", text)
        except ValueError as e:
            return await commandError(ctx, str(e))
        await ctx.send(file=img)

    @commands.command()
    async def lapis(self, ctx, *, text):
        try:
            img = await self.make_meme_from_template("data/memes/lapis.png", text)
        except ValueError as e:
            return await commandError(ctx, str(e))
        await ctx.send(file=img)


    async def make_meme_from_template(self, template, text):
        newText = [x.strip() for x in text.split(',')]
        if len(newText) > 2:
            raise ValueError(f'You gave too many strings!\r'
                             f'Remember memes have a top text and a bottom text delineated by a comma!\r You can also just have a bottom text by formatting your parameter like this: **[command] , bottom text only**')
        if len(newText) == 1:
            await make_meme(topString=newText[0], filename=template)
        else:
            await make_meme(topString=newText[0], bottomString=newText[1], filename=template)

        img = discord.File('data/memes/temp.png')
        return img

def setup(bot):
    bot.add_cog(Memes(bot))
