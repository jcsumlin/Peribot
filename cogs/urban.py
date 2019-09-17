from urllib.parse import quote_plus

import requests
from discord.ext import commands


class Urban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_nsfw()
    @commands.command()
    async def urban(self,ctx, *, search_terms: str, definition_number: int = 1):
        """Urban Dictionary search
        Definition number must be between 1 and 10"""

        def encode(s):
            return quote_plus(s, encoding='utf-8', errors='replace')

        # definition_number is just there to show up in the help
        # all this mess is to avoid forcing double quotes on the user

        search_terms = search_terms.split(" ")
        try:
            if len(search_terms) > 1:
                pos = int(search_terms[-1]) - 1
                search_terms = search_terms[:-1]
            else:
                pos = 0
            if pos not in range(0, 11):  # API only provides the
                pos = 0  # top 10 definitions
        except ValueError:
            pos = 0

        search_terms = "+".join([encode(s) for s in search_terms])
        url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
        try:
            with requests.get(url) as r:
                result = r.json()
            if result["list"]:
                definition = result['list'][pos]['definition']
                example = result['list'][pos]['example']
                defs = len(result['list'])
                msg = ("**Definition #{} out of {}:\n**{}\n\n"
                       "**Example:\n**{}".format(pos + 1, defs, definition,
                                                 example))
                await ctx.send(msg)
            else:
                await ctx.send("Your search terms gave no results.")
        except IndexError:
            await ctx.send("There is no definition #{}".format(pos + 1))
        except:
            await ctx.send("Error.")



def setup(bot):
    n = Urban(bot)
    bot.add_cog(n)
