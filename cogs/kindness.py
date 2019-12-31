import io
import json
import random

import aiohttp
import discord
import giphypop
from discord.ext import commands

from .utils.dataIO import dataIO
import os, os.path
import re


class Kindness(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx, victim: discord.Member = None):
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
        elif victim.name == kisser:
            await ctx.send(
                f"{kisser} starts making out with their image in a mirror... strange one this {kisser} is...")
        else:
            msg = random.choice(dataIO.load_json("data/lewd/kiss.json")['kiss']).format(kisser=str(kisser),
                                                                                        victim=str(victim.name))
            embed = discord.Embed(title=msg, color=0xFF69B4)
            embed.set_image(url=random.choice(results).raw_data['images']['fixed_height_downsampled']['url'])
            await ctx.send(embed=embed)

        # await ctx.send(msg)

    @commands.command("hug")
    async def hug(self, ctx, victim: discord.Member, number=None):
        """
        Hug a user with a cute gif
        :param victim: the user you are hugging
        :param number: The specific gif you want to return. If None picks a random gif.
        :return: The gif of your hug
        """
        if victim == ctx.author:
            return await ctx.channel.send(
                'https://tenor.com/view/steven-universe-su-stevenuniverse-diamonddays-gif-13326567')
        if number is None:
            DIR = 'data/lewd/hugs'
            number = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            file = str(random.randint(1, number)) + '.gif'
        else:
            file = str(number) + '.gif'
        await ctx.send(file=discord.File('data/lewd/hugs/' + file))

    @commands.command()
    async def hugadd(self, ctx, url):
        if '.gif' not in url:
            return await ctx.send("Please provide a Gif not an image!")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                DIR = 'data/lewd/hugs'
                number = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
                with open(f"{DIR}/{number}.gif", 'wb') as f:
                    f.write(data.read())
                await ctx.send(f"File Successfully saved as number {number}")

    @commands.command()
    async def pat(self, ctx, target=None, number=None):
        if number is None:
            DIR = 'data/lewd/headpats'
            number = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            file = str(random.randint(1, number)) + '.gif'
        await ctx.send(file=discord.File('data/lewd/headpats/' + file))

    @commands.command()
    async def addpat(self, ctx):
        dir = 'data/lewd/headpats'
        if ("https://" in ctx.message.content.lower() or "http://" in ctx.message.content.lower()):
            url = ctx.message.content[7:].lstrip(" ")
            await self.linkSubmit(ctx, url, dir)
        else:
            try:
                await self.normalSubmit(ctx, dir)
            except Exception as e:
                print(str(e))

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
        message = random.choice(messages).format(cuddler=ctx.author.name, victim=target.name)
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

    async def linkSubmit(self, ctx, url, dir):
        if '.gif' not in url:
            return await ctx.send("Please provide a Gif not an image!")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                number = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))]) + 1
                with open(f"{dir}/{number}.gif", 'wb') as f:
                    f.write(data.read())
                await ctx.send(f"File Successfully saved as number {number}")

    async def normalSubmit(self, ctx, dir):
        jsonstr = ctx.message.attachments[0]
        url = jsonstr.url
        await self.linkSubmit(ctx, url, dir)


def setup(bot):
    n = Kindness(bot)
    bot.add_cog(n)
