from configparser import ConfigParser

from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
    def __init__(self, bot):
        auth = ConfigParser()
        auth.read('auth.ini')  # All my usernames and passwords for the api
        self.bot = bot
        self.key = auth.get('STATCORD', 'KEY')
        self.api = statcord.Client(self.bot,self.key)
        self.api.start_loop()


    @commands.Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatcordPost(bot))
