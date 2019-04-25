import re

import discord
from discord.ext import commands


def process_avatar(url):
    if ".gif" in url:
        new_url = re.sub("\?size\=\d+.*", "?size=2048", url)
        return new_url
    else:
        new_url = url.replace('.webp', '.png')
        return new_url

class Avatar:
    """Get user's avatar URL."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def avatar(self, ctx, *, user: discord.Member=None):
        """Returns user avatar URL."""
        author = ctx.message.author

        if not user:
            user = author

        u = await self.bot.get_user_info(str(user.id))
        url0 = u.avatar_url
        url = process_avatar(url0)
        embed = discord.Embed(title="{}'s Avatar".format(user.name))
        embed.set_image(url=url)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Avatar(bot))