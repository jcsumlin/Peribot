from discord.ext import commands

class SendAsPeribot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def send(self,ctx,  channel, *, message: str):
        if ctx.author.id == 204792579881959424:
            channel2 = self.bot.get_channel(id=channel)
            await channel2.send(message)

def setup(bot):
    bot.add_cog(SendAsPeribot(bot))
