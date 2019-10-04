import csv
import json
import os
from datetime import datetime, timezone

import discord
from discord.ext import commands
from loguru import logger
# from create_databases import Base, Report

# declaration for User class is in here
from .utils.easyembed import embed as easyembed
from cogs.utils.database import Database
from cogs.utils import checks



class Moderation(commands.Cog):
    """Report system for admins"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        return await self.database.add_server_settings(guild)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def setreport(self, ctx):
        """
        Sets the channel that reports come into.
        """
        try:
            channel = ctx.message.channel.id
            server_id = str(ctx.message.guild.id)
            # TODO: Setup database call
            await ctx.send("Report channel set! Any user reports will alert users here.")
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)
        except Exception as e:
            logger.error(e)
            pass

    @commands.command()
    @commands.dm_only()
    async def report(self, ctx, server_id: int = None, *, message: str):
        """
        For users to report something going wrong.
        :param message: What you want included in the report
        """
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
            report_channel = self.bot.get_channel(id=int(channel))
            await report_channel.send(embed=em)
            await report_channel.send("@here")
            # await self.bot.send_message(self.bot.get_channel(id=channel), '@here')
            await ctx.send("Your report has been sent, the mods will look in to it as soon as possible.")
            await self.database.audit_record(int(server_id),
                                             report_channel.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)
            # break

    @commands.group()
    @checks.mod_or_higher()
    async def warn(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=easyembed(title="Sorry that's not how this command works!",
                                           description="ex: !warn add [user id] Stop spamming please"))

    @warn.group(name="add", aliases=['user'])
    @checks.mod_or_higher()
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
            user = await self.bot.fetch_user(int(user_id))
            if not await self.database.add_warning(ctx.guild.id, user, ctx.message.author, reason):
                await ctx.send(
                    embed=easyembed(title="Error adding report to database!"))
            await user.send(embed=easyembed(
                title=f"Hey there {user.name} the mods from {ctx.message.guild.name} have sent you a warning!",
                description=f"Their reason is as follows: {reason}\n\nIf you have any questions please reach out to any of the staff members"))
            await ctx.send(embed=easyembed(
                title="User has been warned in the DM's",
                color=discord.Color.green()))
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)

    @checks.mod_or_higher()
    @warn.group(name="list")
    async def list(self, ctx):
        reports = await self.database.get_all_reports(ctx.guild.id)
        users = {}
        if len(reports) == 0:
            await ctx.send("There have been no users warned on this server yet.")
        else:
            for report in reports:
                if f"{report.user_name} ({report.user_id})" not in users.keys():
                    users[f"{report.user_name} ({report.user_id})"] = 1
                else:
                    users[f"{report.user_name} ({report.user_id})"] = users[
                                                                          f"{report.user_name} ({report.user_id})"] + 1
            warns=""
            for user, number_of_reports in users.items():
                warns += f"{user}: **{number_of_reports}**\n"
            embed1 = discord.Embed(title=f"Use **{ctx.prefix}warn reason [user id]** to see what they were warned for. ", description=warns, color=discord.Color.dark_red(), timestamp=datetime.now())
            embed1.set_author(name=f"{ctx.message.guild.name}'s Warned Users", icon_url=ctx.guild.icon_url)
            embed1.set_thumbnail(url="https://media.discordapp.net/attachments/564994079532908544/623917350454034479/New_Composition_2019-09-18_12-24-37.png")
            embed1.set_footer(text=f"{ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed1)
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)

    @warn.group(name="reason")
    @checks.mod_or_higher()
    async def reason(self, ctx, user_id=None):
        if user_id == None:
            easy_embed = easyembed(title="Sorry that's not how this command works!",
                                   description="ex: !warn reason [user id]")
            await ctx.send(embed=easy_embed)
            return
        reports = await self.database.get_user_warns(ctx.guild.id, user_id)
        if len(reports) == 0:
            await ctx.send("That user has no warnings logged at this time.")
        else:
            user = await self.bot.fetch_user(int(user_id))
            embed1 = discord.Embed(
                title=f"Use **{ctx.prefix}warn list** to see all the warns for this server. ", color=user.color, timestamp=datetime.now())
            embed1.set_author(name=f"Warnings for {user.name} are as follows:", icon_url=user.avatar_url)
            embed1.set_footer(text=f"{ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            for report in reports:
                embed1.add_field(name=f"ID: {report.id} | {report.date.strftime('%m/%d/%Y %H:%M')} UTC by {report.mod_name}", value=f"```\n{report.reason}\n```")
            await ctx.send(embed=embed1)
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)

    @warn.group(name="delete")
    @checks.mod_or_higher()
    async def delete(self, ctx, warning_id: int=None):
        """
        Delete a single warning for a user based on that warnings id
        :param ctx:
        :param user_id:
        :return:
        """
        if warning_id == None:
            easy_embed = discord.Embed(title="Sorry that's not how this command works!",
                                   description=f"ex: !warn delete [warning id]\n*The warning id is found from {ctx.prefix}warn reason [user id]*")
            await ctx.send(embed=easy_embed)
            return
        reports = await self.database.get_warn(ctx.guild.id, warning_id)
        if reports is None:
            easy_embed = discord.Embed(title="Sorry that ID does not exist!",
                                       description=f"ex: !warn delete [warning id]\n*The warning id is found from {ctx.prefix}warn reason [user id]*")
            await ctx.send(embed=easy_embed)
        else:
            report = await self.database.delete_report(ctx.guild.id,warning_id)
            if report is not None:
                user = await self.bot.fetch_user(int(report.user_id))
                mod = await self.bot.fetch_user(int(report.mod_id))
                embed = discord.Embed(title=f"",
                                      description=f"Warning reason:\n```\n{report.reason}\n```\n"
                                                  f"Warning Date Time: {report.date.strftime('%m/%d/%Y %H:%M')} UTC\n"
                                                  f"Warned by: {mod.mention}",
                                      color=discord.Color.green(),
                                      timestamp=datetime.now())
                embed.set_author(name=f"Warning for {user.name} has been removed from the database!", icon_url=user.avatar_url)
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)


def setup(bot):
    bot.add_cog(Moderation(bot))
