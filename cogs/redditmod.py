from discord.ext import commands
import discord
from loguru import logger


class Reddit:
    """Custom commands

    Creates commands used to display text"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["sr"], pass_context=True, no_pm=True)
    async def subreport(self, ctx, link):
        if ctx.message.channel == '486883481843138560':
            if 'reddit.com' in ctx.message.content:
                embed = discord.Embed(title="Should this post be removed?",
                                      url=link)
                embed.set_thumbnail(
                    url="https://b.thumbs.redditmedia.com/-WOirRBZXE7LaTFTkD3X7zSp3rK3mkbxFtrxtEt7WDY.png")
                message = await self.bot.send_message(ctx.message.channel, embed=embed)
                await self.bot.add_reaction(message, u"\u2705")
                await self.bot.add_reaction(message, u"\u274C")