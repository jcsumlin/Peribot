import random

from discord.ext import commands


class Chikadance:
    def __init__(self, bot):
        self.bot = bot
        self.dance = ['https://cdn.discordapp.com/attachments/486899116299911178/543612168172601344/image0.gif',
                      'https://cdn.discordapp.com/attachments/486899116299911178/543613000033239070/image0.gif',
                      'https://cdn.discordapp.com/attachments/486899116299911178/543613202177720320/image0.gif',
                      'https://cdn.discordapp.com/attachments/517546603473797141/540644284106276864/k757zzgurid21.gif']

    @commands.command(name='chika')
    async def chikadance(self):
       choice = random.choice(self.dance)
       await self.bot.say(choice)


def setup(bot):
    n = Chikadance(bot)
    bot.add_cog(n)