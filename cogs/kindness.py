from discord.ext import commands
import random
import discord
from .utils.dataIO import dataIO
import json
import os, os.path
import giphypop

class Kindness:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def kiss(self, ctx, victim:discord.Member = None):
        g = giphypop.Giphy("KZciiXBwyJ9RabyZyUHjQ8e4ZutZQ1Go")
        results = [x for x in g.search('kiss')]
        kisses = ['https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif',
                  "https://i.imgur.com/PIyPCfZ.gif",
                  "https://thumbs.gfycat.com/FondEvergreenIcterinewarbler-max-1mb.gif"]
        kisser = ctx.message.author.name
        if victim == None:
            await self.bot.say(str(ctx.message.author.name) + " puckers their lips, but no one is there... sad.")
        elif victim.name ==kisser:
            await self.bot.say(f"{kisser} starts making out with their image in a mirror... strange one this {kisser} is...")
        else:
            msg = random.choice(dataIO.load_json("data/lewd/kiss.json")['kiss']).format(kisser=str(kisser),victim=str(victim.name))
            embed = discord.Embed(title=msg, color=0xFF69B4)
            embed.set_image(url=random.choice(results).raw_data['images']['fixed_height_downsampled']['url'])
            await self.bot.say(embed=embed)

        # await self.bot.say(msg)

    @commands.command("hug", pass_context=True)
    async def hug(self, ctx, victim: discord.Member, number=None):
        count = sum([len(files) for r, d, files in os.walk("cogs/data/lewd/hugs")])
        if number is None:
            file = str(random.randint(1,30)) + '.gif'
        else:
            file = str(number) + '.gif'
        area = ctx.message.channel
        author = ctx.message.author.mention
        # embed = discord.Embed(title=author+'hugs'+victim.mention)
        # embed.set_image(url=)
        with open('data/lewd/hugs/'+file, 'rb') as file:
            await self.bot.send_file(area, file)

    @commands.command(pass_context=True)
    async def compliment(self, ctx, target):
        msg = random.choice(dataIO.load_json("data/compliment/compliments.json")['compliments'])
        await self.bot.say(str(target) + ' ' + msg)


def setup(bot):
    n = Kindness(bot)
    bot.add_cog(n)