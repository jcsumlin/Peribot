import discord
from discord.ext import commands


class Avatar(commands.Cog):
    """Get user's avatar URL."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
        """Returns user avatar URL."""
        author = ctx.author
        if user is None:
            user = author
        user_name = user.name.replace('_', '\_').replace('~', '\~').replace('|', '\|').replace('*', '\*')
        embed = discord.Embed(title=f"{user_name}'s Avatar", color=user.color)
        if user.is_avatar_animated():
            embed.set_image(url=user.avatar_url_as(format='gif', size=1024))
        else:
            embed.set_image(url=user.avatar_url_as(format='png', size=1024))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Avatar(bot))
