from discord.ext import commands


class CursedPearl:
    def __init__(self, bot):
        self.bot = bot


    async def serverCheck(self, ctx):
        if ctx.message.server == '515370084538253333':
            return True
        else: return False

    @commands.command(pass_context=True, no_pm=True)
    async def levels(self, ctx):
        if self.serverCheck(ctx):
            await self.bot.send_message(ctx.message.channel, "Sorry to be the one to tell you clods, but !rank and !levels have been disabled on here. But don’t worry, you’re all number one to me! :perismirk:")

    @commands.command(pass_context=True, no_pm=True)
    async def rank(self, ctx):
        if self.serverCheck(ctx):
            await self.bot.send_message(ctx.message.channel, "Sorry to be the one to tell you clods, but !rank and !levels have been disabled on here. But don’t worry, you’re all number one to me! :perismirk:")


def setup(bot):
    bot.add_cog(CursedPearl(bot))
