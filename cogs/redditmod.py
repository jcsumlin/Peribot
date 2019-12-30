import discord
from discord.ext import commands


class Reddit(commands.Cog):
    """Custom commands

    Creates commands used to display text"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["sr"], no_pm=True)
    async def subreport(self, ctx, link):
        if ctx.channel.id == 486883481843138560:
                embed = discord.Embed(title="Should this post be removed?",
                                      url=link)
                embed.set_thumbnail(
                    url="https://b.thumbs.redditmedia.com/-WOirRBZXE7LaTFTkD3X7zSp3rK3mkbxFtrxtEt7WDY.png")
                message = await ctx.channel.send(embed=embed)
                await message.add_reaction(message, u"\u2705")
                await message.add_reaction(message, u"\u274C")
                await ctx.message.delete()

def setup(bot):
    bot.add_cog(Reddit(bot))
