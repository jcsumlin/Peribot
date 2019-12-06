import os
from datetime import datetime

import discord
from discord.ext import commands, tasks
from loguru import logger
from pytz import timezone
from .utils.genericResponseBuilder import commandSuccess, commandError
from .utils.database import Database


from .utils.dataIO import dataIO, fileIO


class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()
        self.database = Database()

    def cog_unload(self):
        self.check_birthdays.cancel()

    @commands.group()
    async def birthday(self, ctx):
        if ctx.invoked_subcommand is None:
            await commandError(ctx, f"Thats not how this command is used!\n\n"
                                    f"**{ctx.prefix}birthday add [birthday]**\n\tThis will add your birthday. Please add it in MM/DD/YYYY format!\n"
                                    f"**{ctx.prefix}birthday list**\n\tThis will list all the birthdays for this month.\n"
                                    f"**{ctx.prefix}birthday clear**\n\tThis will purge your birthday from my database.\n"
                                    f"**{ctx.prefix}birthday channel [channel]**\n\t(Admins only) This will set the channel where Peribot wishes everyone a happy birthday!\n"
                                    f"**{ctx.prefix}birthday disable**\n\t(Admins only) This will disable the birthday functionality in your server.\n"
                                    f"**{ctx.prefix}birthday role @[role]**\n\t(Admins only | Optional) This will give a user a role of your choosing on their special day.")
            return

    @birthday.group()
    async def add(self, ctx, birthday):
        settings = await self.database.get_birthday_settings(ctx.guild.id)
        if settings is None:
            await commandError(ctx, f"This feature has not been enabled by your admins! Please have them do {ctx.prefix}birthday to see how to set this up!")
        birthday = birthday.split('/')
        birthdays = await self.database.birthday_exists(ctx)
        if birthdays is not False:
            await commandError(ctx, "Your birthday is already registered! Peribot will ping you on your special day.")
            return
        user = ctx.author
        if int(birthday[2]) >= datetime.now().year:
            await ctx.channel.send("That's not a valid year silly")
            return
        birthday = datetime(year=int(birthday[2]), month=int(birthday[0]), day=int(birthday[1]))
        await self.database.add_birthday(server_id=ctx.guild.id, user_id=user.id, birthday=birthday)
        await commandSuccess(ctx, "Your birthday has been added!")

    @birthday.group()
    async def clear(self, ctx):
        try:
            await self.database.delete_birthday(user_id=ctx.author.id)
            await commandSuccess(ctx, "Your birthday data was successfully removed from my database!")
        except ValueError:
            await commandError(ctx, "Coundn't find your birthday record in my database, are you sure you registered it with me?")

    @birthday.group()
    async def list(self, ctx):
        birthdays = await self.database.get_months_bdays()
        settings = await self.database.get_birthday_settings(ctx.guild.id)
        embed = discord.Embed(title=f"{ctx.guild.name}'s Birthday list for this month :birthday:",
                              description=f"Users will be pinged on their birthday in <#{settings.channel_id}>.\n You can use **{ctx.prefix}birthday clear** to remove your birthday from my records")
        for user in birthdays:
            member = discord.utils.find(lambda m: m.id == user.user_id, ctx.guild.members)
            embed.add_field(name=member.name, value=user.birthday.strftime('%m/%d/%Y'))
        await ctx.channel.send(embed=embed)

    @birthday.group()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """

        :param ctx:
        :param channel:
        :return:
        """
        settings = await self.database.get_birthday_settings(ctx.guild.id)
        if settings is None:
            default_message = "Hey [user]! I just wanted to wish you the happiest of birthdays on your [years][suffix] birthday! :birthday: :heart:"
            await self.database.add_birthday_settings(ctx.guild.id, True, channel.id, default_message)
        else:
            settings.channel_id = channel.id
        return await ctx.send("Birthday Channel Set! :birthday:")

    @birthday.group()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        settings = await self.database.get_birthday_settings(ctx.guild.id)
        if settings is not None:
            new_settings = await self.database.update_birthday_settings(ctx.guild.id, enabled=False)
            if new_settings.enabled is False:
                return await commandSuccess(ctx, ":white_check_mark: Birthday Messages Disabled!")
            else:
                return await commandError(ctx, ":x: Failed to update Birthday Settings!")

        else:
            return await commandError(ctx, ":interrobang: Birthday Message Channel Not Set For This Server!")

    # TODO: Add this as a migration later to the settings table
    # @birthday.group()
    # @commands.has_permissions(administrator=True)
    # async def role(self, ctx, role: discord.Role):
    #     birthdays = await self.get_config()
    #     birthdays[str(ctx.guild.id)]['role_id'] = role.id
    #     await self.save_config(birthdays)
    #     await ctx.channel.send("Birthday Role Set!")

    @tasks.loop(seconds=30.0)
    async def check_birthdays(self):
        await self.bot.wait_until_ready()
        birthdays = await self.database.get_todays_birthdays()
        if len(birthdays) == 0:
            return
        for birthday in birthdays:
            settings = await self.database.get_birthday_settings(birthday.server_id)
            if settings.enabled is False:
                return
            channel = self.bot.get_channel(settings.channel_id)
            member = discord.utils.find(lambda m: m.id == birthday.user_id, channel.guild.members)
            if member is None:
                logger.error(f'Could not find user {birthday.user_id}')
                continue
            years = datetime.now().year - birthday.birthday.year
            if 4 <= years <= 20 or 24 <= years <= 30:
                suffix = "th"
            else:
                suffix = ["th", "st", "nd", "rd","th", "th", "th", "th", "th", "th"][years % 10]
            await channel.send(f"Hey <@{birthday.user_id}>! I just wanted to wish you the happiest of birthdays on your {years}{suffix} birthday! :birthday: :heart:")
            await self.database.update_birthday(birthday.id, completed=True)


def setup(bot):
    bot.add_cog(Birthdays(bot))
