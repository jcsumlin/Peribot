import aiohttp
import discord
from discord.ext import commands
from loguru import logger

from cogs.utils.database import Database
import urllib.parse


class Nookazon(commands.Cog):
    """
    """

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def nookazon(self, ctx, *, name):
        base_url = f"https://nookazon.com/api/items?variants=&search={urllib.parse.quote(name)}"
        async with self.session.get(base_url) as r:
            if r.status != 200:
                return ctx.send("API Error please try again later! :(")
            result = await r.json()

        if len(result["items"]) == 0:
            return await ctx.send(f"No items were found for {name}")
        first_item = result["items"][0]
        embed = discord.Embed(title="**Item**: {}".format(first_item["name"]), description="**Item Type**: {item_type} \n**Is DIY?**: {diy}\n**Buy Price**: {buy}\n**Sell Price**: {sell}\n**Average Price**: {avgprice}".format(
            item_type=first_item['type'],
            diy='yes' if first_item['diy'] is True else 'No',
            buy=first_item['buy_price'],
            sell=first_item['sell_price'],
            avgprice=first_item['price']),
                              url=f"https://nookazon.com/product/{first_item['id']}")
        embed.set_thumbnail(url=first_item["img"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nookazon(bot))
