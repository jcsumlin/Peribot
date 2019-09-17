import csv
import json
import os
from datetime import datetime

import discord
from discord.ext import commands
from loguru import logger
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

# declaration for User class is in here
from create_databases import Base, Report
from .utils.easyembed import embed as easyembed


class Moderation(commands.Cog):
    """Report system for admins"""

    def __init__(self, bot):
        self.bot = bot
        engine = create_engine('sqlite:///warnings.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()  # session.commit() to store data, and session.rollback() to discard changes

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def setreport(self, ctx):
        """
        Sets the channel that reports come into.
        """
        try:
            channel = ctx.message.channel.id
            server_id = str(ctx.message.guild.id)
            with open('data/report/info.json', 'r+') as f:
                data = json.load(f)
                data[server_id] = str(channel)  # <--- add `id` value.
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
            await ctx.send("Report channel set! Any user reports will alert users here.")
        except Exception as e:
            logger.error(e)
            pass

    @commands.command()
    async def report(self, ctx, server_id: int = None, *, message: str):
        """
        For users to report something going wrong.
        :param message: What you want included in the report
        """
        if ctx.message.channel.is_private:
            if server_id is None:
                await self.bot.send_message(ctx.message.author,
                                            embed=easyembed(
                                                title="No Server ID Specified!",
                                                description="!report [server-id] [message]. You can get the server ID from right clicking on the Server icon and selecting 'Copy ID'"))
            else:
                server_id = str(server_id)
                with open('data/report/info.json', 'r') as f:
                    data = json.load(f)
                    if server_id not in data.keys():
                        logger.debug(f"No channel ID set for reports! {server_id}")
                        await self.bot.say(easyembed(
                            title="Invalid Server ID!",
                            description="Either this server hasn't specified a channel to recieve reports or that ID you gave me is not a valid server ID"))
                        return
                    channel = data[server_id]
                member = ctx.message.author
                em = discord.Embed(title="Report Case", description=message)
                em.add_field(name="author", value=member)
                em.set_footer(text=f"#{ctx.message.channel}")
                report_channel = await self.bot.get_channel(id=int(channel))
                await report_channel.send(embed=em)
                await report_channel.send("@here")
                # await self.bot.send_message(self.bot.get_channel(id=channel), '@here')
                await ctx.send("Your report has been sent, the mods will look in to it as soon as possible.")
                # break

    @commands.group()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=easyembed(title="Sorry that's not how this command works!",
                                           description="ex: !warn add [user id] Stop spamming please"))

    @warn.group(name="add", aliases=['user'])
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, user_id=None, *, reason=None):
        if user_id is None and reason is None:
            await ctx.send(
                embed=easyembed(title="Sorry that's not how this command works!",
                                description="ex: !warn add [user id] Stop spamming please"))
        elif user_id is not None and reason is None:
            await ctx.send(
                embed=easyembed(title="Sorry that's not how this command works!",
                                description="ex: !warn add [user id] Stop spamming please"))
        elif user_id is not None and reason is not None:
            user = await self.bot.get_user_info(user_id)
            try:
                new_report = Report(date=datetime.utcnow(), server_id=str(ctx.message.guild.id),
                                    user_name=user.name, user_id=str(user_id),
                                    mod_name=str(ctx.message.author.name),
                                    mod_id=str(ctx.message.author.id), reason=reason)
                self.session.add(new_report)
                self.session.commit()
            except:
                await ctx.send(
                    embed=easyembed(title="Error adding report to databse"))
            await user.send(embed=easyembed(
                title=f"Hey there {user.name} the mods from {ctx.message.guild.name} have warned you!",
                description=f"Their reason is as follows: {reason}"))
            await ctx.send(embed=easyembed(
                title="User has been warned in the DM's",
                color=discord.Color.green()))

    @warn.group(name="list")
    async def list(self, ctx):
        reports = self.session.query(Report).filter(Report.server_id == str(ctx.message.guild.id)).all()
        users = {}
        if len(reports) == 0:
            await ctx.send("There have been no users warned on this server yet.")
        else:
            for report in reports:
                if f"{report.user_name} | {report.user_id}" not in users.keys():
                    users[f"{report.user_name} | {report.user_id}"] = 1
                else:
                    users[f"{report.user_name} | {report.user_id}"] = users[
                                                                          f"{report.user_name} | {report.user_id}"] + 1
            embed1 = discord.Embed(title=f":warning: Warned Users from {ctx.message.guild.name} :warning: ")
            for user, number_of_reports in users.items():
                embed1.add_field(name=user, value=str(number_of_reports), inline=False)
            await ctx.send(embed=embed1)

    @warn.group(name="reason")
    async def reason(self, ctx, user_id=None):
        if user_id == None:
            easy_embed = easyembed(title="Sorry that's not how this command works!",
                                   description="ex: !warn reason [user id]")
            await ctx.send(embed=easy_embed)
            return
        reports = self.session.query(Report).filter(
            and_(Report.server_id == str(ctx.message.guild.id), Report.user_id == str(user_id))).all()
        if len(reports) == 0:
            await ctx.send(
                "That user has no warnings logged at this time.")
        else:
            user = await self.bot.get_user_info(user_id)
            embed1 = discord.Embed(title=f"Warnings for {user.name} are as follows:")
            for report in reports:
                embed1.add_field(name=f"{report.date} by {report.mod_name}", value=report.reason)
            await ctx.send(embed=embed1)

    @warn.group(name="delete")
    async def delete(self, ctx, user_id=None):
        if user_id == None:
            easy_embed = easyembed(title="Sorry that's not how this command works!",
                                   description="ex: !warn delete [user id]")
            await ctx.send(embed=easy_embed)
            return
        reports = self.session.query(Report).filter(
            and_(
                Report.server_id == str(ctx.message.guild.id),
                Report.user_id == str(user_id)
            )).all()
        if len(reports) == 0:
            await ctx.send(
                "That user has no warnings logged at this time.")
        else:
            user = await self.bot.get_user_info(user_id)
            try:
                num_rows_deleted = self.session.query(Report).filter(
                    and_(
                        Report.server_id == str(ctx.message.guild.id),
                        Report.user_id == str(user_id)
                    )).delete()
                self.session.commit()
            except:
                self.session.rollback()
                await ctx.send(
                    embed=easyembed(title="Error removing that user from the databsse!",
                                    color=discord.Color.red()))
                return
            user = await self.bot.get_user_info(user_id)
            await ctx.send(
                embed=easyembed(title=f"{user.name} has been removed from the database!",
                                description=f"{num_rows_deleted} warning records were removed!",
                                color=discord.Color.green()))

    @warn.group(name="backup")
    async def backup(self, ctx):
        outfile = open('mydump.csv', 'wb')
        outcsv = csv.writer(outfile)
        cursor = self.session.execute("select * from report")
        await ctx.send(f"{len(cursor)} Rows being exported")
        # dump column titles (optional)
        outcsv.writerow(x[0] for x in cursor.description)
        # dump rows
        outcsv.writerows(cursor.fetchall())
        await self.bot.send_file(ctx.message.channel, outfile)
        outfile.close()
        os.remove("mydump.csv")


def setup(bot):
    bot.add_cog(Moderation(bot))
