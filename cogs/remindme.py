import os
import time

import discord
from discord.ext import tasks, commands
from loguru import logger

from .utils.dataIO import fileIO


class RemindMe(commands.Cog):
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()
        self.check_remindeveryone.start()
        self.reminders = fileIO("data/remindme/reminders.json", "load")
        self.remindeveryone = fileIO("data/remindme/remindeveryone.json", "load")
        self.units = {"minute" : 60, "hour" : 3600, "day" : 86400, "week": 604800, "month": 2592000}

    def cog_unload(self):
        self.check_reminders.cancel()
        self.check_remindeveryone.cancel()

    async def cog_before_invoke(self, ctx):
        if not os.path.exists("data/remindme"):
            logger.info("Creating data/remindme folder...")
            os.makedirs("data/remindme")

        f = "data/remindme/reminders.json"
        if not fileIO(f, "check"):
            logger.info("Creating empty reminders.json...")
            fileIO(f, "save", [])
        f = "data/remindme/remindeveryone.json"
        if not fileIO(f, "check"):
            logger.info("Creating empty remindeveryone.json...")
            fileIO(f, "save", [])

    @commands.command()
    async def remindme(self, ctx,  quantity : int, time_unit : str, *, text : str):
        """Sends you <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]remindme 3 days Have sushi with Asu and JennJenn"""
        time_unit = time_unit.lower()
        author = ctx.author
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await ctx.send("Invalid time unit. Choose minutes/hours/days/weeks/month")
            return
        if quantity < 1:
            await ctx.send("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await ctx.send("Text is too long.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time()+seconds)
        self.reminders.append({"ID" : author.id, "FUTURE" : future, "TEXT" : text})
        logger.info("{} ({}) set a reminder.".format(author.name, author.id))
        await ctx.send("I will remind you that in {} {}.".format(str(quantity), time_unit + s))
        fileIO("data/remindme/reminders.json", "save", self.reminders)

    @commands.has_role("RemindHere")
    @commands.command(aliases=["re"])
    async def remindhere(self, ctx, quantity: int, time_unit: str, *, text: str):
        """Sends everyone <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]remindeveryone 3 days Have sushi with Asu and JennJenn"""
        time_unit = time_unit.lower()
        channel = ctx.channel
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await ctx.send("Invalid time unit. Choose minutes/hours/days/weeks/month")
            return
        if quantity < 1:
            await ctx.send("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await ctx.send("Text is too long.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)
        self.remindeveryone.append({"ID": channel.id, "FUTURE": future, "TEXT": text, 'AUTHOR': ctx.author.id})
        await ctx.send("I will remind everyone here of that in {} {}.".format(str(quantity), time_unit + s))
        fileIO("data/remindme/remindeveryone.json", "save", self.remindeveryone)

    @commands.command()
    async def forgetme(self, ctx):
        """Removes all your upcoming notifications"""
        author = ctx.author
        to_remove = []
        for reminder in self.reminders:
            if reminder["ID"] == author.id:
                to_remove.append(reminder)

        if not to_remove == []:
            for reminder in to_remove:
                self.reminders.remove(reminder)
            fileIO("data/remindme/reminders.json", "save", self.reminders)
            await ctx.send("All your notifications have been removed.")
        else:
            await ctx.send("You don't have any upcoming notification.")

    @tasks.loop(seconds=5.0)
    async def check_reminders(self):
        await self.bot.wait_until_ready()
        to_remove = []
        for reminder in self.reminders:
            if reminder["FUTURE"] <= int(time.time()):
                try:
                    user = self.bot.get_user(int(reminder["ID"]))
                    await user.send("You asked me to remind you this:\n{}".format(reminder["TEXT"]))
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    to_remove.append(reminder)
                    logger.debug(f"User ID {reminder['ID']} could not be found, skipping")
                except discord.errors.HTTPException:
                    logger.debug(f"discord.errors.HTTPException on User ID {reminder['ID']}'s reminder")
                    pass
                else:
                    to_remove.append(reminder)
        for reminder in to_remove:
            self.reminders.remove(reminder)
        if to_remove:
            fileIO("data/remindme/reminders.json", "save", self.reminders)

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=5.0)
    async def check_remindeveryone(self):
        await self.bot.wait_until_ready()
        to_remove = []
        for reminder in self.remindeveryone:
            if reminder["FUTURE"] <= int(time.time()):
                try:
                    channel = self.bot.get_channel(int(reminder['ID']))
                    user = self.bot.get_user(int(reminder["AUTHOR"]))
                    e = discord.Embed(title=f":reminder_ribbon: {user.name} asked me to remind everyone here of this:", description=reminder["TEXT"])
                    await channel.send("@here", embed=e)
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    to_remove.append(reminder)
                except discord.errors.HTTPException:
                    pass
                else:
                    to_remove.append(reminder)
        for reminder in to_remove:
            self.remindeveryone.remove(reminder)
        if to_remove:
            fileIO("data/remindme/remindeveryone.json", "save", self.remindeveryone)

    @check_remindeveryone.before_loop
    async def before_check_remindeveryone(self):
        await self.bot.wait_until_ready()

def setup(bot):
    n = RemindMe(bot)
    bot.add_cog(n)
