import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import os
import asyncio
import time
from loguru import logger

class RemindMe:
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = fileIO("data/remindme/reminders.json", "load")
        self.remindeveryone = fileIO("data/remindme/remindeveryone.json", "load")
        self.units = {"minute" : 60, "hour" : 3600, "day" : 86400, "week": 604800, "month": 2592000}

    @commands.command(pass_context=True)
    async def remindme(self, ctx,  quantity : int, time_unit : str, *, text : str):
        """Sends you <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]remindme 3 days Have sushi with Asu and JennJenn"""
        time_unit = time_unit.lower()
        author = ctx.message.author
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await self.bot.say("Invalid time unit. Choose minutes/hours/days/weeks/month")
            return
        if quantity < 1:
            await self.bot.say("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await self.bot.say("Text is too long.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time()+seconds)
        self.reminders.append({"ID" : author.id, "FUTURE" : future, "TEXT" : text})
        logger.info("{} ({}) set a reminder.".format(author.name, author.id))
        await self.bot.say("I will remind you that in {} {}.".format(str(quantity), time_unit + s))
        fileIO("data/remindme/reminders.json", "save", self.reminders)

    @commands.has_role(name="RemindHere")
    @commands.command(pass_context=True, aliases=["re"])
    async def remindhere(self, ctx, quantity: int, time_unit: str, *, text: str):
        """Sends everyone <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]remindeveryone 3 days Have sushi with Asu and JennJenn"""
        logger.success("hello")
        time_unit = time_unit.lower()
        channel = ctx.message.channel
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await self.bot.say("Invalid time unit. Choose minutes/hours/days/weeks/month")
            return
        if quantity < 1:
            await self.bot.say("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await self.bot.say("Text is too long.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)
        self.remindeveryone.append({"ID": channel.id, "FUTURE": future, "TEXT": text})
        logger.info("{} ({}) set a reminder.".format(ctx.message.author.name, channel.id))
        await self.bot.say("I will remind everyone that in {} {}.".format(str(quantity), time_unit + s))
        fileIO("data/remindme/remindeveryone.json", "save", self.remindeveryone)


    @commands.command(pass_context=True)
    async def forgetme(self, ctx):
        """Removes all your upcoming notifications"""
        author = ctx.message.author
        to_remove = []
        for reminder in self.reminders:
            if reminder["ID"] == author.id:
                to_remove.append(reminder)

        if not to_remove == []:
            for reminder in to_remove:
                self.reminders.remove(reminder)
            fileIO("data/remindme/reminders.json", "save", self.reminders)
            await self.bot.say("All your notifications have been removed.")
        else:
            await self.bot.say("You don't have any upcoming notification.")

    async def check_reminders(self):
        while self is self.bot.get_cog("RemindMe"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        await self.bot.send_message(discord.User(id=reminder["ID"]),
                                                    "You asked me to remind you this:\n{}".format(reminder["TEXT"]))
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)
            for reminder in to_remove:
                self.reminders.remove(reminder)
            if to_remove:
                fileIO("data/remindme/reminders.json", "save", self.reminders)
            await asyncio.sleep(5)

    async def check_remindeveryone(self):
        while self is self.bot.get_cog("RemindMe"):
            to_remove = []
            for reminder in self.remindeveryone:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        channel = self.bot.get_channel(id=reminder['ID'])
                        await self.bot.send_message(self.bot.get_channel(id=reminder['ID']),"You asked me to remind @here this:\n{}".format(reminder["TEXT"]))
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
            await asyncio.sleep(5)

def check_folders():
    if not os.path.exists("data/remindme"):
        logger.info("Creating data/remindme folder...")
        os.makedirs("data/remindme")

def check_files():
    f = "data/remindme/reminders.json"
    if not fileIO(f, "check"):
        logger.info("Creating empty reminders.json...")
        fileIO(f, "save", [])
    f = "data/remindme/remindeveryone.json"
    if not fileIO(f, "check"):
        logger.info("Creating empty remindeveryone.json...")
        fileIO(f, "save", [])

def setup(bot):
    check_folders()
    check_files()
    n = RemindMe(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_reminders())
    loop.create_task(n.check_remindeveryone())
    bot.add_cog(n)
