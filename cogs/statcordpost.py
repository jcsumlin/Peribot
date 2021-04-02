import os

from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if "STATCORD_KEY" not in os.environ or os.environ.get('STATCORD_KEY') is None:
            return
        else:
            self.key = "statcord.com-" + os.environ.get('STATCORD_KEY')
            self.api = statcord.Client(self.bot,self.key)
            self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self,ctx):
        if "STATCORD_KEY" not in os.environ or os.environ.get('STATCORD_KEY') is None:
            return
        else:
            self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatcordPost(bot))
