from discord.ext import commands


class Riot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def riot(self, ctx, *, text: str):
        '''
        Riot in the street!
        :param text: What you are rioting about
        :return: RIOT!!
        '''
        await ctx.send('ヽ༼ຈل͜ຈ༽ﾉ **' + str(text) + '** ヽ༼ຈل͜ຈ༽ﾉ')


def setup(bot):
    bot.add_cog(Riot(bot))
