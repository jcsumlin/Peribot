import discord
from discord.ext import commands

class Shipper:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ship(self, user1 : discord.Member, user2 : discord.Member):
        """Creates a ship name for two users"""
        name1 = user1.name
        name2 = user2.name
        name2 = name2[::-1]
        x = int(len(name1)/2)
        y = int(len(name2)/2)
        name1 = name1[:-x]
        name2 = name2[:-y]
        name2 = name2[::-1]
        message = "❤️ Your ship name is *{namex}{namey}* ❤️".format(namex=name1, namey=name2)
        await self.bot.say(message)

def setup(bot):
    bot.add_cog(Shipper(bot))