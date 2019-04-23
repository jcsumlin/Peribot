import discord
from discord.ext import commands

class SendAsPeribot:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def send(self,ctx,  channel, *, message: str):
        """Creates a ship name for two users"""
        if ctx.message.author.id == "204792579881959424":
            channel2 = self.bot.get_channel(id=channel)
            await self.bot.send_message(channel2, message)

def setup(bot):
    bot.add_cog(SendAsPeribot(bot))
