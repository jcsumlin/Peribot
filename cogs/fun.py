import random
from datetime import datetime
from random import choice

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Pong!
        """
        msg = await ctx.send("*Pinging...*")
        seconds = datetime.now() - self.bot.start_time
        server_latency = msg.created_at - ctx.message.created_at
        embed = discord.Embed(title="📶 Ping",
                              description=f"**Server**: `{server_latency}ms`\n" +
                                          f"**API**: `{round(self.bot.latency, 1)}ms`\n" +
                                          f"**Uptime**: `{seconds}`")

        await msg.edit(embed=embed, content=None)

    @commands.command()
    async def topic(self, ctx):
        """
        Gets a random chat topic to keep the chat going.
        """
        website = requests.get('https://www.conversationstarters.com/generator.php').content
        soup = BeautifulSoup(website, 'html.parser')
        topic = soup.find(id="random").text
        await ctx.send(topic)

    @commands.command(aliases=['r'])
    async def roll(self, ctx, upper_bound: str = None, modifier: str = None, number: int = None):
        if upper_bound is None and modifier is None and number is None:
            upper_bound = 20
            msg = random.randint(1, upper_bound)
        else:
            if 'd' in upper_bound.lower():
                upper_bound = upper_bound.lower()
                upper_bound = int(upper_bound.replace('d', ''))
            else:
                upper_bound = int(upper_bound)

            if upper_bound is not None and modifier is None and number is None:
                msg = random.randint(1, upper_bound)
            else:
                allowed_modifiers = ["+", "-", "*", "/"]
                if modifier not in allowed_modifiers:
                    await ctx.send("That is not a valid modifier! Allowed Modifiers include: " + str(allowed_modifiers))
                    return
                if upper_bound is not None and modifier is not None and number is None:
                    await ctx.send(
                        f"If you want to specify a modifier please make sure to give a number after it!\n\rExample: {ctx.prefix}roll 20 + 2")
                    return
                msg = random.randint(1, upper_bound)
                math = f"{msg} {modifier} {number}"
                msg = eval(math)

        if upper_bound == 1:
            msg = "***How do you even roll a one sided die?***"
        elif msg >= upper_bound:
            msg = "***Critical Hit!*** " + str(msg)
        elif msg == 1:
            msg = "***Critical Fail!*** " + str(msg)

        await ctx.send(f":game_die: You rolled a {msg}")

    @commands.command()
    @commands.is_owner()
    async def setgame(self, ctx, game):
        """
        Changes my displayed game. Only for privileged users!
        :param ctx: message context.
        :param game: a string of the game I am playing.
        :return: "Game Changed Successfully"
        """
        game = discord.Game(game)
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        embedMsg = discord.Embed(color=0x90ee90, title=":video_game: Game changed successfully!")
        await ctx.send(embed=embedMsg)

    @commands.command()
    async def flip(self, ctx, user: discord.Member = None):
        """
        Flips a coin ... or a user. But not me.
        :param user: the user you are flipping
        :return: either a flipped coin or user
        """
        if user != None:
            msg = ""
            if user.id == self.bot.user.id:
                user = ctx.author
                msg = "Nice try. You think this is funny? How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await ctx.send(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await ctx.send("*flips a coin and... " + choice(["HEADS!*", "TAILS!*"]))

    @commands.command()
    async def ded(self, ctx):
        # await ctx.send("https://giphy.com/gifs/bare-barren-Az1CJ2MEjmsp2")
        embed = discord.Embed()
        embed.set_image(url="https://i.imgur.com/X6pMtG4.gif")
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def uwu(self, ctx, *, message):
        uwus = ['UwU', 'Uwu', 'uwU', 'ÚwÚ', 'uwu', '☆w☆', '✧w✧', '♥w♥', '︠uw ︠u', '(uwu)', 'OwO', 'owo', 'Owo', 'owO']
        res = message.replace("r", "w").replace("l", "w").replace("L", "W").replace("R", "W")
        res = res.replace("the ", "da ").replace("The ", "Da ").replace("THE ", "DA ")
        res = res.replace("th", "d").replace("TH", "D")
        res = res.replace("\n", " " + random.choice(uwus) + "\n")
        await ctx.send(res + ' ' + random.choice(uwus))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "f":
            await message.add_reaction(u"\U0001F1EB")
        if message.content.lower() == "press x to doubt":
            await message.add_reaction(u"\U0001F1FD")


def setup(bot):
    bot.add_cog(Fun(bot))
