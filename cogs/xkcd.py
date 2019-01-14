from discord.ext import commands
import discord
import json
import urllib.request


class XKCD:
    def __init__(self, bot):
        self.bot = bot
        self.apiurl = "http://xkcd.com/{x}/info.0.json"
        self.current = "http://xkcd.com/info.0.json"

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, number: int = None):
        if number is None:
            with urllib.request.urlopen(self.current) as url:
                data = json.loads(url.read().decode())
                embed = discord.Embed(title=data["title"], description=f"Alt: {data['alt']}")
                embed.set_image(url=data["img"])
                embed.set_footer(text=f"XKCD nr.{data['num']}")
                await self.bot.say(embed=embed)
        else:
            try:
                with urllib.request.urlopen(self.apiurl.format(x=number)) as url:
                    data = json.loads(url.read().decode())
                    em = discord.Embed(title=data["title"],
                                       description=f"Alt: {data['alt']}")
                    em.set_image(url=data["img"])
                    em.set_footer(text=f"XKCD nr.{data['num']}")
                    await self.bot.say(embed=em)
            except:
                await self.bot.say("Could not find an XKCD with this ID!")

    # @xkcd.command(pass_context=True)
    # async def id(self, ctx, number: int):
    #    with urllib.request.urlopen(self.apiurl.format(x = number)) as url:
    #        data = json.loads(url.read().decode())
    #        em = discord.Embed(title=data["title"], description="Alt: {x}".format(x = data["alt"], color=discord.Color.red()))
    #        em.set_image(url=data["img"])
    #        await self.bot.say(embed = em)


def setup(bot):
    bot.add_cog(XKCD(bot))