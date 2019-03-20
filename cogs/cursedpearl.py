from discord.ext import commands
from loguru import logger


class CursedPearl:
    def __init__(self, bot):
        self.bot = bot


    def serverCheck(self, ctx):
        if ctx.message.server.id == '515370084538253333':
            return True
        else:
            logger.debug(ctx.message.server.id)
            return False

    @commands.command(pass_context=True, no_pm=True)
    async def levels(self, ctx):
        if self.serverCheck(ctx):
            await self.bot.send_file(ctx.message.channel, "data/card.png")

    @commands.command(pass_context=True, no_pm=True)
    async def rank(self, ctx):
        if self.serverCheck(ctx):
            await self.bot.send_file(ctx.message.channel, "data/card.png")


def setup(bot):
    bot.add_cog(CursedPearl(bot))
