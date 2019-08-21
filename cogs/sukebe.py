import datetime
import random

import discord
from discord.ext import commands


class Sukebe(commands.Cog):
    """Paruru sensei can detect your Sukebe-ness."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sukebe(self, ctx, user: discord.Member = None):
        """Detects user's Sukebe-ness.
        157% accurate!"""
        if user is None:
            user = ctx.author
        a = ctx.message.created_at
        b = a.strftime("%Y-%m-%d %H:%M:%S.%f0")
        c = datetime.datetime.strptime(b[:7], '%Y-%m')
        d = c.timestamp()

        random.seed(int(user.id) % int(d))
        x = ":fire:" * random.randint(1, 10)
        await ctx.send("{}'s Sukebe-ness is : ".format(user.display_name) + x)


def setup(bot):
    bot.add_cog(Sukebe(bot))
