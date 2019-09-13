import random
from random import choice

import discord
from discord.ext import commands
import urllib.parse


class Memes:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def bill(self,ctx, *, text):
        """
        Pong!
        """
        base_url = "https://belikebill.ga/billgen-API.php?text=This%20is%20Bill%0D%0A" + urllib.parse.quote(text) + "%0D%0ABe%20Like%20Bill"
        embed = discord.Embed().set_image(url=base_url)
        await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    bot.add_cog(Memes(bot))
