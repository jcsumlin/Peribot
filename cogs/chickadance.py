import random

import discord
from discord.ext import commands


class Chikadance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dance = ['https://cdn.discordapp.com/attachments/486899116299911178/543612168172601344/image0.gif',
                      'https://cdn.discordapp.com/attachments/486899116299911178/543613000033239070/image0.gif',
                      'https://cdn.discordapp.com/attachments/486899116299911178/543613202177720320/image0.gif',
                      'https://cdn.discordapp.com/attachments/517546603473797141/540644284106276864/k757zzgurid21.gif']

    @commands.command(name='chikadance', aliases=['chika'])
    async def chikadance(self, ctx):
       choice = random.choice(self.dance)
       em = discord.Embed().set_image(url=choice)
       await ctx.send(embed=em)


def setup(bot):
    n = Chikadance(bot)
    bot.add_cog(n)
