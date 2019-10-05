import random

import discord
import giphypop
from discord.ext import commands

from .utils.dataIO import fileIO, dataIO
from loguru import logger
from ftplib import FTP, all_errors
import os
import requests


class CursedPearl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = fileIO("data/cp/quotes/quotes.json", "load")
        self.author = fileIO("data/cp/quotes/author.json", "load")


    def guildCheck(self, ctx):
        if ctx.guild.id == 515370084538253333:
            return True
        else: return False

    @commands.command(no_pm=True)
    async def whitelist(self, ctx, username):
        logger.warn(f"{username} being added to whitelist by {ctx.message.author.id}")
        with FTP('107.172.93.98')  as ftp:# connect to host, default port
            ftp.login(user="J_C.736421", passwd="johnsummy")  # user anonymous, passwd anonymous@
            file_copy = "whitelist.json"
            file_orig = '/whitelist.json'
            with open(file_copy, 'w') as fp:
                res = ftp.retrlines('RETR ' + file_orig, fp.write)

                if not res.startswith("226-File successfully transferred"):
                    print('Download failed')
                    if os.path.isfile(file_copy):
                        os.remove(file_copy)
        if os.path.isfile(file_copy):
            whitelist = dataIO.load_json('whitelist.json')
            username = "awefawefaoiwenfaoiwenf"
            uuid = requests.get(f"http://tools.glowingmines.eu/convertor/nick/{username}").json()
            if "error" in uuid:
                return ctx.send("Invalid username please try again")
            new_user = {'uuid': uuid, 'name': username}
            whitelist.append(new_user)
            os.remove(file_copy)

    @commands.command(no_pm=True)
    async def levels(self, ctx):
        if self.guildCheck(ctx):
            await ctx.send(file=discord.File("./data/cp/card.png"))

    @commands.command(no_pm=True)
    async def rank(self, ctx):
        if self.guildCheck(ctx):
            await ctx.send(file=discord.File("./data/cp/card.png"))

    @commands.command(no_pm=True)
    async def peridot(self, ctx):
        if self.guildCheck(ctx):
            g = giphypop.Giphy("KZciiXBwyJ9RabyZyUHjQ8e4ZutZQ1Go")
            results = [x for x in g.search('Peridot')]
            embed = discord.Embed(color=0xe6e200)
            embed.set_image(url=random.choice(results).raw_data['images']['fixed_height_downsampled']['url'])
            embed.set_footer(text="This is a random gif from Giphy using the search term 'Peridot'")
            await ctx.send(embed=embed)

    @commands.command()
    async def quote(self,ctx):
        index = random.randint(0,len(self.quotes) - 1)
        quote = self.quotes[index]
        author = self.author[index]
        if 'Pearl' in author:
            thumbnail = 'https://i.lensdump.com/i/Agxrvq.png'
            color = 0xf7ceb2
        elif 'Garnet' in author:
            thumbnail = 'https://i.lensdump.com/i/AgxEca.png'
            color = 0x7a032d
        elif 'Amethyst' in author:
            thumbnail = 'https://i.lensdump.com/i/AgxtGA.png'
            color = 0xad8dbe
        elif 'Steven' in author:
            thumbnail = 'https://i.lensdump.com/i/AgxREM.png'
            color = 0xffc954
        elif 'Lapis' in author:
            thumbnail = 'https://i.lensdump.com/i/AgxTHQ.png'
            color = 0x66b9fb
        elif 'Peridot' in author:
            thumbnail = 'https://i.lensdump.com/i/AgxC3k.png'
            color = 0x3c796a
        embed = discord.Embed(title=quote, description=author, color=color)
        embed.set_thumbnail(url=thumbnail)
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(CursedPearl(bot))
