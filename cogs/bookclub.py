import random

import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from cogs.utils.BookClub import BookClubModel
from .utils.checks import is_bot_owner_check


class BookClub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = BookClubModel()
        self.scheduler = AsyncIOScheduler(timezone='America/New_York')
        self.scheduler.add_job(self.update_chapters, trigger='cron', hour=23, minute=1, second=1, replace_existing=True,
                               coalesce=True, id='update_chapters_id')
        self.scheduler.start()

    async def update_chapters(self):
        bc = await self.model.get_all()
        for club in bc:
            club.start = club.end + 1
            club.end = (club.start + club.interval) - 1
            try:
                channel = self.bot.get_channel(club.channel_id)
                await channel.edit(topic=f"{club.title} Chapters {club.start} - {club.end}",
                                   reason="Daily job to update book club channels")
                await channel.send(f"Chapters updated to {club.start} - {club.end}")
            except Exception as e:
                logger.error(e)

        await self.model.save()

    async def cog_unload(self):
        self.scheduler.remove_job('update_chapters_id')
        self.scheduler.shutdown()

    @commands.group()
    async def bookclub(self, ctx):
        pass

    @is_bot_owner_check()
    @bookclub.command()
    async def forceupdate(self, ctx):
        await self.update_chapters()
        await ctx.send("Done")

    @bookclub.command()
    async def create(self, ctx, title: str, start: int = 1, interval: int = 1):
        try:
            bookclub = await self.model.add(
                server_id=ctx.guild.id,
                channel_id=ctx.channel.id,
                title=title,
                interval=interval,
                start=start
            )
        except Exception as e:
            return await ctx.send(f"Error creating new book club. Please try again\n```\n{e}\n```")
        e = discord.Embed(title=f"Book club **{bookclub.title}** was created successfully",
                          description=f"**Interval**: {bookclub.interval}"
                                      f"\n**Start**: {bookclub.start}"
                                      f"\n**End**: {bookclub.end}",
                          color=random.randint(0, 0xffffff))
        return await ctx.send(embed=e)

    @bookclub.command()
    async def end(self, ctx):
        bc = await self.model.get_by_channel_id(ctx.channel.id)
        if bc is not None:
            await self.model.delete(bc)
            await ctx.send("Book club has been ended!")
        else:
            await ctx.send("No book club was found")

    @commands.group()
    async def chapter(self, ctx):
        if ctx.invoked_subcommand is None:
            channel_id = ctx.channel.id
            bc = await self.model.get_by_channel_id(channel_id)
            if bc is None:
                await ctx.send("No book club found, maybe you should start one.")
            e = discord.Embed(title=f"{bc.title} Book club",
                              description=f"Chapters today: {bc.start} - {bc.end}",
                              color=random.randint(0, 0xffffff))
            return await ctx.send(embed=e)

    @chapter.command()
    async def interval(self, ctx, interval: int = 1):
        bc = await self.model.get_by_channel_id(ctx.channel.id)
        bc.interval = interval
        bc.end = (bc.start + bc.interval) - 1
        await self.model.save()
        await ctx.send(f"Interval updated! Set to {bc.interval}")

    @chapter.command()
    async def add(self, ctx, number: int = 1):
        bc = await self.model.get_by_channel_id(ctx.channel.id)
        bc.end = bc.end + number
        await self.model.save()
        await ctx.send(f"Chapters updated! Chapters today are {bc.start} - {bc.end}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Error!",
                                  description=f"Command is on cool down (discord rate limits and such). Try again in {exception.retry_after} seconds.",
                                  color=discord.Color.red())
            message = await ctx.send(embed=embed)
            message_sent = True

def setup(bot):
    bot.add_cog(BookClub(bot))
