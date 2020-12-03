import random
import discord
from discord.ext import commands
from .utils.SecretSanta import SecretSantaModel
from collections import deque
import jwt
from configparser import *

from .utils.checks import is_bot_owner_check


class SecretSanta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.secretsantamodel = SecretSantaModel()
        auth = ConfigParser()
        auth.read('../auth.ini')  # All my usernames and passwords for the api
        self.key = auth.get('JWTKey', 'Key')

    @commands.group()
    async def secretsanta(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="That's not how you use this command",
                                  description=f"{ctx.prefix}secretsanta enroll [Your address (it will be encrypted )]\n"
                                              f"{ctx.prefix}secretsanta assign\n")
            await ctx.send(embed=embed)

    @secretsanta.command()
    async def enroll(self, ctx, *, address):
        if ctx.message.channel.type.name != "private":
            return await ctx.send("This command can only be used in DMs please DM the bot.")
        try:
            if self.secretsantamodel.get_by_user_id(ctx.author.id) is None:
                return await ctx.send("You're already enrolled in the ACTA Secret Santa")
            address = {"address": address}
            address = jwt.encode(address, self.key, algorithm='HS256')
            await self.secretsantamodel.add(user_id=ctx.author.id, address=address, server_id=448695150135345152)
            await ctx.send("You have been enrolled in the ACTA Secret Santa")
        except Exception as e:
            await ctx.send(f"Failed to register you for the Secret Santa. Did you already register?\n```{e}```")

    @is_bot_owner_check()
    @secretsanta.command()
    async def list(self, ctx):
        all_users = await self.secretsantamodel.get_all(ctx.guild.id)
        members = []
        for user in all_users:
            user = await self.bot.fetch_user(user.user_id)
            if user is not None:
                members.append(user.mention)

        embed = discord.Embed(title="ACTA Secret Santa Participants",
                              description=f"Budget: **TBD**\nNumber of participants: {len(all_users)}\n\n {', '.join(members)}")
        await ctx.send(embed=embed)

    @is_bot_owner_check()
    @secretsanta.command()
    async def assign(self, ctx):
        all_users = await self.secretsantamodel.get_all(ctx.guild.id)
        if len(all_users) % 2 != 0:
            return await ctx.send("There are an odd number of participants. Cant assign pairs.")

        def pair_up(people):
            """ Given a list of people, assign each one a secret santa partner
            from the list and return the pairings as a dict. Implemented to always
            create a perfect cycle"""
            random.shuffle(people)
            partners = deque(people)
            partners.rotate()
            user_ids = [user.user_id for user in people]
            return dict(zip(user_ids, partners))
        pairs = pair_up(all_users)
        for key, value in pairs.items():
            user = await self.bot.fetch_user(key)
            if user.bot or user is None:
                continue
            partner = await self.bot.fetch_user(value.user_id)
            decoded = jwt.decode(value.address, self.key, algorithms='HS256')
            await user.send(f"You have been given {partner.mention} for secret santa. \nTheir address is {decoded['address']}\nIf there are issues with their address please contact JC.")

    @secretsanta.command()
    async def check(self, ctx, *, address):
        all_users = await self.secretsantamodel.get_all(448695150135345152)
        for user in all_users:
            decoded = jwt.decode(user.address, self.key, algorithms='HS256')
            if address == decoded:
                user = await self.bot.fetch_user(user.user_id)
                return await ctx.send(f"You have {user.name}")
        return await ctx.send("No user found. please make sure that you copied the address I sent you earlier "
                              "**exactly**")



def setup(bot):
    bot.add_cog(SecretSanta(bot))
