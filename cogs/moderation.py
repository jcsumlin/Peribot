import asyncio
import json
from datetime import datetime

import discord
from discord.ext import commands
from loguru import logger

from cogs.utils import checks
from cogs.utils.database import Database
from .utils.checks import mod_or_higher
from .utils.dataIO import DataIO
from .utils.easyembed import embed as easyembed
from .utils.time import get_datetime, get_time_string


class Moderation(commands.Cog):
    """Admin and Moderation Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()
        self.dataIO = DataIO()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        return await self.database.add_server_settings(guild)

    # !tempban [member] [time] [reason]
    # Bans a member for a specified time period
    @commands.has_permissions(ban_members=True)
    @commands.command(name='tempban')
    async def tempban(self, ctx, member: discord.Member = None, time=None, *, reason=None):
        if member is None:
            embed = discord.Embed(title='Command Error!',
                                  description='Please specify a member.',
                                  color=0xff0007)
            await ctx.send(embed=embed)
            return
        if time is None:
            embed = discord.Embed(title='Command Error!',
                                  description='Please specify a time.\n'
                                              '**Example: 1min**\n'
                                              'Most time abbreviations can be used (s, sec, m, min(s), etc.'
                                              ' See Documentation for more info.)',
                                  color=0xff0007)
            await ctx.send(embed=embed)
            return
        description = f"You have been temp banned from {ctx.guild.name} for {get_time_string(time)}"
        if reason:
            description += f"\nThis reason was provided by the staff:\n**{reason}**"
        embed = discord.Embed(title=f"Hey there {member.display_name}",
                              description=description)
        await member.send(embed=embed)
        await member.ban(reason=reason)
        self.bot.timer_manager.create_timer('tempban', get_datetime(time), args=(ctx, member))
        await ctx.send(embed=await self.gen_msg(ctx, 'banned', member, time, reason))

    async def gen_msg(self, ctx, verb, member, timer=None, reason=None):
        msg = f'{member} was successfully {verb}'
        if timer is not None:
            msg += f' for {get_time_string(timer)}'
        msg += '!'
        embed = discord.Embed(title=msg,
                              description=f'Reason: {reason}.',
                              color=discord.Color.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        return embed

    @commands.Cog.listener()
    async def on_tempban(self, ctx, member):
        await ctx.guild.unban(member)
        await ctx.send(embed=await self.gen_msg(ctx, 'unbanned', member))

    async def create_mute_role(self, ctx):
        role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(role,
                                          send_messages=False,
                                          add_reactions=False,
                                          send_tts_messages=False,
                                          embed_links=False,
                                          attach_files=False,
                                          speak=False,
                                          connect=False
                                          )
        e = discord.Embed(title="New 'Muted' role was created!",
                          description="Please move it to the top of your role hierarchy for it to work properly",
                          color=discord.Color.orange())
        await ctx.send(embed=e)
        return role

    # !tempmute [member] [time] [reason]
    # Mutes a member for a specified period of time
    @commands.has_permissions(manage_roles=True)
    @commands.command(name='tempmute')
    async def tempmute(self, ctx, member: discord.Member = None, time=None, *, reason=None):
        if member is None:
            embed = discord.Embed(title='Command Error!',
                                  description='Please specify a member.',
                                  color=0xff0007)
            await ctx.send(embed=embed)
            return
        if time is None:
            embed = discord.Embed(title='Command Error!',
                                  description='Please specify a time.\n'
                                              '**Example: 1min**\n'
                                              'Most time abbreviations can be used (s, sec, m, min(s), etc.'
                                              ' See Documentation for more info.)',
                                  color=0xff0007)
            await ctx.send(embed=embed)
            return
        try:
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            if role is None:
                role = await self.create_mute_role(ctx)

            await member.add_roles(role)
            await ctx.send(embed=await self.gen_msg(ctx, 'muted', member, time, reason))
            self.bot.timer_manager.create_timer('tempmute', get_datetime(time), args=(ctx, member))
        except Exception as error:
            embed = discord.Embed(title='Command Error!',
                                  description=f'{member} could not be muted.',
                                  color=0xff0007)
            await ctx.send(embed=embed)
            logger.exception(f'Error in the !tempmute command. [{error}]')

    @commands.Cog.listener()
    async def on_tempmute(self, ctx, member):
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name='Muted'))
        await ctx.send(embed=await self.gen_msg(ctx, 'unmuted', member))

    @commands.command('purge', no_pm=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int = 5):
        messages = []
        async for message in ctx.message.channel.history(limit=number + 1):
            messages.append(message)
        await ctx.message.channel.delete_messages(messages)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)

    @commands.command(name='mute')
    @mod_or_higher()
    async def mute(self, ctx, member: discord.Member, minutes: int = 5):
        for channel in member.guild.channels:
            await channel.set_permissions(member, send_messages=False, reason=f"{ctx.message.author} muted {member}")
        await ctx.send(f"<:check:677974494815584286> {member} has been muted for {minutes} minute(s)")
        await asyncio.sleep(minutes * 60)
        for channel in member.guild.channels:
            await channel.set_permissions(member, send_messages=None,
                                          reason=f"{member} has been un-muted after {minutes} minute(s)")
        await ctx.send(f"<:check:677974494815584286> {member} has been un-muted after {minutes} minute(s)")

    @commands.command(name='pin')
    @mod_or_higher()
    async def pin_message(self, ctx, *, message):
        """Copy your message in a stylish and modern frame, and then fix it!
        Arguments:
        `: message` - message
        __ __
        For example:
        ```
        !pin This text was written by the ancient Elves in the name of Discord!
        ```
        """
        embed = discord.Embed(color=ctx.message.author.top_role.color,
                              title='Pin it up!',
                              description=message)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        msg = await ctx.send(embed=embed)
        await ctx.message.delete()
        await msg.pin()
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = 'N/A'):
        """
        `:member` - The person you are kicking
        `:reason` - Reason for kick

        """
        try:
            await member.kick(reason=reason)
        except Exception as e:
            await ctx.send("error")
            return
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                              description=f'User {member.name} was kicked.\nReason: {reason}.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        await ctx.send(embed=embed)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = 'N/A', delete: int = 0):
        """
        `:member` - The person you are banning @ them
        `:reason` - Reason for kick

        """

        await member.ban(reason=reason, delete_message_days=delete)
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                              description=f'User {member.name} was banned.\n'
                                          f'Reason: {reason}.\n'
                                          f'Messages Deleted: {delete} days')

        await ctx.send(embed=embed)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: int, *, reason: str = 'N/A'):
        """
        `:member` - The person you are unbanning (their ID)
        `:reason` - Reason for kick

        """
        for banentry in await ctx.guild.bans():
            if member == banentry.user.id:
                try:
                    await ctx.guild.unban(banentry.user, reason=reason)
                except discord.Forbidden:
                    embed = discord.Embed(title="Command Error!", description=f"I do not have permissions to do that",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                except discord.HTTPException:
                    embed = discord.Embed(title="Command Error!", description=f"Unbanning failed. Try again",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                                      description=f'User {banentry.user.name} was unbanned.\nReason: {reason}.')
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
                await ctx.send(embed=embed)
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)

    # TODO: Fix user reports
    # @commands.command()
    # @commands.has_permissions(manage_messages=True)
    # async def setreport(self, ctx):
    #     """
    #     Sets the channel that reports come into.
    #     """
    #     try:
    #         channel = ctx.message.channel.id
    #         server_id = str(ctx.message.guild.id)
    #         # TODO: Setup database call
    #         await ctx.send("Report channel set! Any user reports will alert users here.")
    #         await self.database.audit_record(ctx.guild.id,
    #                                          ctx.guild.name,
    #                                          ctx.message.content,
    #                                          ctx.message.author.id)
    #     except Exception as e:
    #         logger.error(e)
    #         pass
    #
    # @commands.command()
    # @commands.dm_only()
    # async def report(self, ctx, server_id=None, *, message: str = None):
    #     """
    #     For users to report something going wrong.
    #     :param message: What you want included in the report
    #     """
    #     if server_id is None or message is None:
    #         await ctx.message.author(embed=easyembed(
    #             title="No Server ID Specified!",
    #             description=f"Usage: {ctx.prefix}report [server-id] [message]. [How to get server id](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)"))
    #     else:
    #         server_id = int(server_id)
    #         with open('data/report/info.json', 'r') as f:
    #             data = json.load(f)
    #             if server_id not in data.keys():
    #                 logger.debug(f"No channel ID set for reports! {server_id}")
    #                 await self.bot.say(easyembed(
    #                     title="Invalid Server ID!",
    #                     description="Either this server hasn't specified a channel to recieve reports or that ID you gave me is not a valid server ID"))
    #                 return
    #             channel = data[server_id]
    #         member = ctx.message.author
    #         em = discord.Embed(title="Report Case", description=message)
    #         em.add_field(name="author", value=member)
    #         em.set_footer(text=f"#{ctx.message.channel}")
    #         report_channel = self.bot.get_channel(id=int(channel))
    #         await report_channel.send(embed=em)
    #         await report_channel.send("@here")
    #         # await self.bot.send_message(self.bot.get_channel(id=channel), '@here')
    #         await ctx.send("Your report has been sent, the mods will look in to it as soon as possible.")
    #         await self.database.audit_record(int(server_id),
    #                                          report_channel.guild.name,
    #                                          ctx.message.content,
    #                                          ctx.message.author.id)
    #         # break

    @commands.group()
    @checks.mod_or_higher()
    async def warn(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=easyembed(title="Sorry that's not how this command works!",
                                           description=f"ex: {ctx.prefix}warn add [user id] Stop spamming please"))

    @warn.group(name="add", aliases=['user'])
    @checks.mod_or_higher()
    async def add(self, ctx, user_id=None, *, reason=None):
        if user_id is None and reason is None:
            await ctx.send(
                embed=easyembed(title="Sorry that's not how this command works!",
                                description=f"ex: {ctx.prefix}warn add [user id] Stop spamming please"))
        elif user_id is not None and reason is None:
            await ctx.send(
                embed=easyembed(title="Sorry that's not how this command works!",
                                description=f"ex: {ctx.prefix}warn add [user id] Stop spamming please"))
        elif user_id is not None and reason is not None:
            user = await self.bot.fetch_user(int(user_id))
            if not await self.database.add_warning(ctx.guild.id, user, ctx.message.author, reason):
                await ctx.send(
                    embed=easyembed(title="Error adding report to database!"))
            await user.send(embed=easyembed(
                title=f"Hey there {user.name} the mods from {ctx.message.guild.name} have sent you a warning!",
                description=f"Their reason is as follows: {reason}\n\nIf you have any questions please reach out to any of the staff members"))
            await ctx.send(embed=easyembed(
                title=":white_check_mark: User has been warned in the DM's",
                description=f"use **{ctx.prefix}warn list** : to see all your server's warns!",
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
            warns = ""
            for user, number_of_reports in users.items():
                warns += f"{user}: **{number_of_reports}**\n"
            embed1 = discord.Embed(
                title=f"Use **{ctx.prefix}warn reason [user id]** to see what they were warned for. ",
                description=warns, color=discord.Color.dark_red(), timestamp=datetime.now())
            embed1.set_author(name=f"{ctx.message.guild.name}'s Warned Users", icon_url=ctx.guild.icon_url)
            embed1.set_thumbnail(
                url="https://media.discordapp.net/attachments/564994079532908544/623917350454034479/New_Composition_2019-09-18_12-24-37.png")
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
                                   description=f"ex: {ctx.prefix}warn reason [user id]")
            await ctx.send(embed=easy_embed)
            return
        reports = await self.database.get_user_warns(ctx.guild.id, user_id)
        if len(reports) == 0:
            await ctx.send("That user has no warnings logged at this time.")
        else:
            user = await self.bot.fetch_user(int(user_id))
            embed1 = discord.Embed(
                title=f"Use **{ctx.prefix}warn list** to see all the warns for this server. ",
                description=f"You can use **{ctx.prefix}warn delete [ID]** to remove a warn from the database.",
                color=user.color,
                timestamp=datetime.now())
            embed1.set_author(name=f"Warnings for {user.name} are as follows:", icon_url=user.avatar_url)
            embed1.set_footer(text=f"{ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            for report in reports:
                embed1.add_field(
                    name=f"ID: {report.id} | {report.date.strftime('%m/%d/%Y %H:%M')} UTC by {report.mod_name}",
                    value=f"```\n{report.reason}\n```", inline=False)
            await ctx.send(embed=embed1)
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)

    @warn.group(name="delete")
    @checks.mod_or_higher()
    async def delete(self, ctx, warning_id: int = None):
        """
        Delete a single warning for a user based on that warnings id
        :param ctx:
        :param user_id:
        :return:
        """
        if warning_id == None:
            easy_embed = discord.Embed(title="Sorry that's not how this command works!",
                                       description=f"ex: {ctx.prefix}warn delete [warning id]\n*The warning id is found from {ctx.prefix}warn reason [user id]*")
            await ctx.send(embed=easy_embed)
            return
        reports = await self.database.get_warn(ctx.guild.id, warning_id)
        if reports is None:
            easy_embed = discord.Embed(title="Sorry that ID does not exist!",
                                       description=f"ex: {ctx.prefix}warn delete [warning id]\n*The warning id is found from {ctx.prefix}warn reason [user id]*")
            await ctx.send(embed=easy_embed)
        else:
            report = await self.database.delete_report(ctx.guild.id, warning_id)
            if report is not None:
                user = await self.bot.fetch_user(int(report.user_id))
                mod = await self.bot.fetch_user(int(report.mod_id))
                embed = discord.Embed(title=f"",
                                      description=f"Warning reason:\n```\n{report.reason}\n```\n"
                                                  f"Warning Date Time: {report.date.strftime('%m/%d/%Y %H:%M')} UTC\n"
                                                  f"Warned by: {mod.mention}",
                                      color=discord.Color.green(),
                                      timestamp=datetime.now())
                embed.set_author(name=f"Warning for {user.name} has been removed from the database!",
                                 icon_url=user.avatar_url)
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)


def setup(bot):
    bot.add_cog(Moderation(bot))
