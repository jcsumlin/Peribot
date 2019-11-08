import random

import discord
import giphypop
from discord.ext import commands

from .utils.dataIO import dataIO


class Kindness(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx, victim:discord.Member = None):
        """
        Kisses a user with a random gif from Giphy
        :param ctx:
        :param victim: Who are you kissing? (optional)
        :return: The kiss you sent off :)
        """
        g = giphypop.Giphy("KZciiXBwyJ9RabyZyUHjQ8e4ZutZQ1Go")
        results = [x for x in g.search('kiss')]
        kisser = ctx.author.name
        if victim == None:
            await ctx.send(str(ctx.author.name) + " puckers their lips, but no one is there... sad.")
        elif victim.name ==kisser:
            await ctx.send(f"{kisser} starts making out with their image in a mirror... strange one this {kisser} is...")
        else:
            msg = random.choice(dataIO.load_json("data/lewd/kiss.json")['kiss']).format(kisser=str(kisser),victim=str(victim.name))
            embed = discord.Embed(title=msg, color=0xFF69B4)
            embed.set_image(url=random.choice(results).raw_data['images']['fixed_height_downsampled']['url'])
            await ctx.send(embed=embed)

        # await ctx.send(msg)

    @commands.command("hug", )
    async def hug(self, ctx, victim: discord.Member, number=None):
        """
        Hug a user with a cute gif
        :param victim: the user you are hugging
        :param number: The specific gif you want to return. If None picks a random gif.
        :return: The gif of your hug
        """
        if victim == ctx.author:
            await ctx.channel.send('https://tenor.com/view/steven-universe-su-stevenuniverse-diamonddays-gif-13326567')
            return
        if number is None:
            file = str(random.randint(1,58)) + '.gif'
        else:
            file = str(number) + '.gif'
        area = ctx.channel
        author = ctx.author.mention
        # embed = discord.Embed(title=author+'hugs'+victim.mention)
        # embed.set_image(url=)
        await ctx.send(file=discord.File('data/lewd/hugs/'+file))

    @commands.command()
    async def cuddle(self, ctx, target: discord.Member):
        if target == ctx.author:
            await ctx.channel.send('https://tenor.com/view/steven-universe-su-stevenuniverse-diamonddays-gif-13326567')
            return
        cuddles = ['https://i.imgur.com/d7gjIVu.gif',
                   'https://media.giphy.com/media/xR9FIxmoAPCMw/giphy.gif',
                   'https://i.imgur.com/fgPMy3v.gif',
                   'https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fmedia.giphy.com%2Fmedia%2F3bqtLDeiDtwhq%2Fgiphy.gif',
                   'https://i.imgur.com/TVT4K9d.gif',
                   'https://i.imgur.com/65ZrxPf.gif',
                   'https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Faf%2F6a%2Ff9%2Faf6af9f078d34217d49287514b2d24d5.gif',
                   'https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fmedia.giphy.com%2Fmedia%2Flrr9rHuoJOE0w%2Fgiphy.gif'
                   ]
        messages = dataIO.load_json('data/lewd/cuddles.json')
        message = random.choice(messages).format(cuddler=ctx.author.name,victim=target.name)
        embed = discord.Embed(title=message, color=discord.Color.purple())
        embed.set_image(url=random.choice(cuddles))
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def compliment(self, ctx, target):
        """
        Compliment a user!
        :param target: Who you are coplimenting
        :return:
        """
        msg = random.choice(dataIO.load_json("data/compliment/compliments.json")['compliments'])
        await ctx.send(str(target) + ' ' + msg)

    @commands.command(name="relax")
    async def relax(self, ctx):
        g = giphypop.Giphy("KZciiXBwyJ9RabyZyUHjQ8e4ZutZQ1Go")
        results = [x for x in g.search('calming loop')]
        embedrelax = discord.Embed(color=discord.Color.blue())
        embedrelax.set_image(url=random.choice(results).raw_data['images']['fixed_height_downsampled']['url'])
        await ctx.send(embed=embedrelax)


def setup(bot):
    n = Kindness(bot)
    bot.add_cog(n)
