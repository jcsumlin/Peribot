import json
import random
import re

import discord
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils.dataIO import fileIO


class Trap:

    def __init__(self, bot):
        self.bot = bot
        self.trap_gifs = fileIO("data/lewd/traps/traps.json", "load")

    @commands.group(pass_context=True)
    async def trap(self, ctx):
        '''
        Returns either a gif of Star Wars Trap or Anime Trap... Are you a gambling man?
        :return: What kind of trap is it?
        '''
        if ctx.invoked_subcommand is None:
            type = random.randint(1, 2)
            if type == 1:
                embed = discord.Embed(title="Now ***that's*** a trap!", color=0xffd2e8)
                embed.set_image(url=random.choice(self.trap_gifs))
                await self.bot.say(embed=embed)
            elif type == 2:
                embed = discord.Embed(title="ITS A TRAP!", color=0x381010)
                embed.set_image(url='https://media.giphy.com/media/8McNH1aXZnVyE/giphy.gif')
                await self.bot.say(embed=embed)

    @trap.group(pass_context=True)
    async def add(self, ctx):
        if ("https://" in ctx.message.content.lower() or "http://" in ctx.message.content.lower()):
            url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
            url = re.search(url_pattern, ctx.message.content.lower()).group(0)
            try:
                self.trap_gifs.append(url)
                dataIO.save_json('data/lewd/traps/traps.json', self.trap_gifs)
                await self.bot.say("Trap added successfully!")
            except:
                await self.bot.say("Trap failed to add!")
        else:
            try:
                # normal submit.
                comment = ctx.message.content[7:].lstrip(" ")
                jsonstr = json.dumps(ctx.message.attachments[0])
                jsondict = json.loads(jsonstr)
                url = jsondict['url']
                self.trap_gifs.append(url)
                dataIO.save_json('data/lewd/traps/traps.json', self.trap_gifs)
                await self.bot.say("Trap added successfully!")
            except:
                await self.bot.say("Trap failed to add!")

    @trap.group()
    async def list(self):
        embed = discord.Embed(title="Current List of trap Gifs/Images")
        increment = 1
        for link in self.trap_gifs:
            embed.add_field(value=link, name=str(increment))
            increment += 1
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Trap(bot))