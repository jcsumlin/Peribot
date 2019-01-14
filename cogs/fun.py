import discord
from discord.ext import commands
import random
from random import choice
import datetime

class Fun:
    def __init__(self, bot):
        self.bot = bot


    def fetch_joined_at(self, user, server):
        """Just a special case for someone special :^)"""
        if user.id == "96130341705637888" and server.id == "133049272517001216":
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at

    @commands.command()
    async def ping(self):
        await self.bot.say("Pong!")

    @commands.command(aliases=['r'])
    async def roll(self, upper_bound=20 #type: int
                   ):
        msg = random.randint(1,int(upper_bound))
        if msg == upper_bound:
            msg = "***Critical Hit!*** " + str(msg)
        elif msg == 1:
            msg = "***Critical Fail!*** " + str(msg)

        await self.bot.say(f":game_die: You rolled a {msg}")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def changegame(self, ctx, game):
        """
        Changes my displayed game. Only for privileged users!
        :param ctx: message context.
        :param game: a string of the game I am playing.
        :return: "Game Changed Successfully"
        """
        await self.bot.change_presence(game=discord.Game(name=game))
        embedMsg = discord.Embed(color=0x90ee90, title=":video_game: Game changed successfully!")
        await self.bot.say(embed=embedMsg)

    @commands.command(pass_context=True)
    async def flip(self, ctx, user : discord.Member=None):
        """Flips a coin... or a user.
        Defaults to coin.
        """
        if user != None:
            msg = ""
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Nice try. You think this is funny? How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await self.bot.say(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await self.bot.say("*flips a coin and... " + choice(["HEADS!*", "TAILS!*"]))


def setup(bot):
    bot.add_cog(Fun(bot))