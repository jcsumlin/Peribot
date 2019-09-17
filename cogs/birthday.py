import os
from datetime import datetime

import discord
from discord.ext import commands, tasks
from loguru import logger
from pytz import timezone

from .utils.dataIO import dataIO, fileIO


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()

    async def cog_before_invoke(self, ctx):
        if not os.path.exists("data/birthday"):
            logger.info("Creating data/birthday folder...")
            os.makedirs("data/birthday")

        f = "data/birthday/birthdays.json"
        if not fileIO(f, "check"):
            logger.info("Creating empty birthdays.json...")
            fileIO(f, "save", {})

    async def get_config(self):
        return dataIO.load_json('data/birthday/birthdays.json')

    async def save_config(self, data):
        return dataIO.save_json('data/birthday/birthdays.json', data)

    @commands.group()
    async def birthday(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @birthday.group()
    async def add(self, ctx, user: discord.User, birthday):
        birthday = birthday.split('/')
        birthdays = await self.get_config()
        if int(birthday[2]) >= datetime.now().year:
            await ctx.channel.send("That's not a valid year silly")
            return
        if str(ctx.guild.id) in birthdays.keys():
            birthday = datetime(year=int(birthday[2]), month=int(birthday[0]), day=int(birthday[1]))
            for birthday_user in birthdays[str(ctx.guild.id)]['users']:
                if birthday_user['user_id'] == user.id:
                    await ctx.channel.send("That User's birthday is already registered!")
                    return
            birthdays[str(ctx.guild.id)]['users'].append({'user_id': user.id, 'birthday': str(birthday), 'COMPLETE': False})
            await self.save_config(birthdays)
            await ctx.send("Done!")
        else:
            await ctx.send("Birthdays not setup!")

    @birthday.group()
    async def list(self, ctx):
        birthdays = await self.get_config()
        users = birthdays[str(ctx.guild.id)]['users']
        embed = discord.Embed(title=f"{ctx.guild.name}'s Birthday list for this month :birthday:")
        for user in users:
            birthday = datetime.strptime(user['birthday'], "%Y-%m-%d 00:00:00")
            now = datetime.now()
            if birthday.month == now.month:
                user_name = discord.utils.get(ctx.guild.members, id=user['user_id'])
                embed.add_field(name=user_name.name, value=birthday.strftime('%m/%d/%Y'))
        await ctx.channel.send(embed=embed)

    @birthday.group()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel):
        birthdays = await self.get_config()
        channel_id = channel.replace("#", "").replace("<", "").replace(">", "")
        if str(ctx.guild.id) not in birthdays.keys():
            birthdays[str(ctx.guild.id)] = {'channel': channel_id, 'users': []}
        else:
            birthdays[str(ctx.guild.id)]['channel'] = channel_id

        await self.save_config(birthdays)
        return await ctx.send("Birthday Channel Set! :birthday:")

    @birthday.group()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        birthdays = await self.get_config()
        if str(ctx.guild.id) in birthdays.keys():
            birthdays[str(ctx.guild.id)]['channel'] = ""
            await self.save_config(birthdays)
            return await ctx.channel.send(":x: Birthday Messages Disabled!")
        else:
            return await ctx.channel.send(":interrobang: Birthday Message Channel Not Set For This Server!")

    @birthday.group()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, role: discord.Role):
        birthdays = await self.get_config()
        birthdays[str(ctx.guild.id)]['role_id'] = role.id
        await self.save_config(birthdays)
        await ctx.channel.send("Birthday Role Set!")

    @tasks.loop(seconds=5.0)
    async def check_birthdays(self):
        birthdays = await self.get_config()
        for key, value in birthdays.items():
            if len(value['users']) == 0 or value['channel'] == '':
                continue
            for user in value['users']:
                birthday = datetime.strptime(user['birthday'], "%Y-%m-%d 00:00:00")
                eastern = timezone('US/Eastern')
                now = datetime.now(eastern)
                channel = self.bot.get_channel(int(value['channel']))
                if channel is None:
                    continue
                birthday_role = None
                if 'role_id' in value:
                    birthday_role = discord.utils.find(lambda r: r.id == value['role_id'],
                                                       channel.guild.roles)
                member = discord.utils.find(lambda m: m.id == user['user_id'], channel.guild.members)
                if member is None:
                    logger.error('Could not find user')
                    continue
                if birthday.month != now.month or birthday.day != now.day and user['COMPLETE']:
                    user['COMPLETE'] = False
                    if birthday_role:
                        try:
                            await self.bot.remove_roles(member, birthday_role)
                        except discord.Forbidden:
                            logger.error("Does Not have permissions to add roles to users!")
                        except Exception:
                            logger.error("Error removing role from user" + member.name)
                    await self.save_config(birthdays)
                if birthday.month == now.month and birthday.day == now.day and not user['COMPLETE']:
                    if birthday_role:
                        try:
                            await member.add_role( birthday_role)
                        except discord.Forbidden:
                            logger.error("Does Not have permissions to add roles to users!")
                    years = now.year - birthday.year
                    if 4 <= years <= 20 or 24 <= years <= 30:
                        suffix = "th"
                    else:
                        suffix = ["st", "nd", "rd"][years % 10 - 1]

                    await channel.send(f"Hey <@{user['user_id']}>! I just wanted to wish you the happiest of birthdays on your {years}{suffix} birthday! :birthday: :heart:")
                    user['COMPLETE'] = True
                    await self.save_config(birthdays)


def setup(bot):
    n = Birthdays(bot)
    bot.add_cog(n)
