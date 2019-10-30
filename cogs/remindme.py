import time

import discord
from discord.ext import tasks, commands
from loguru import logger

from .utils.database import Database


class RemindMe(commands.Cog):
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()
        self.check_reminders.start()
        self.units = {"minute" : 60, "hour" : 3600, "day" : 86400, "week": 604800, "month": 2592000}

    def cog_unload(self):
        self.check_reminders.cancel()

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
        await self.database.post_reminder(user_id=author.id, future=future, text=text)
        await ctx.send("I will remind you that in {} {}.".format(str(quantity), time_unit + s))
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)


    @commands.command()
    async def forgetme(self, ctx):
        """Removes all your upcoming notifications"""
        author = ctx.author
        reminders = self.database.get_reminders()
        to_remove = []
        for reminder in reminders:
            if reminder.user_id == author.id:
                to_remove.append(reminder.id)

        if not to_remove == []:
            for reminder in to_remove:
                await self.database.delete_reminder(id=reminder)
            await ctx.send("All your notifications have been removed.")
        else:
            await ctx.send("You don't have any upcoming notification.")

    @tasks.loop(seconds=5.0)
    async def check_reminders(self):
        to_remove = []
        reminders = await self.database.get_reminders()
        for reminder in reminders:
            if reminder.future <= int(time.time()):
                try:
                    user = await self.bot.fetch_user(reminder.user_id)
                    if user is None:
                        logger.debug(f"Could not find user with id {reminder.user_id}, continuing")
                        return
                    embed = discord.Embed(title="You asked me to remind you this", description=reminder.text, color=discord.Color.blue())
                    await user.send(embed=embed)
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    to_remove.append(reminder)
                    logger.debug(f"User ID {reminder.id} could not be found, skipping")
                except discord.errors.HTTPException:
                    logger.debug(f"discord.errors.HTTPException on User ID {reminder.id}'s reminder")
                    pass
                else:
                    to_remove.append(reminder.id)
        for reminder in to_remove:
            await self.database.delete_reminder(id=reminder)

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

def setup(bot):
    n = RemindMe(bot)
    bot.add_cog(n)
