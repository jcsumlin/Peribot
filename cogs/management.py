import asyncio
import subprocess
import sys

import discord
import git
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.errors import BadArgument

from .utils.checks import admin_or_permissions, is_bot_owner_check
from .utils.database import Database
from loguru import logger


class Management(commands.Cog):
    """
    Set of commands for Administration.
    """

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is True:
            return
        if message.type == discord.MessageType.default:
            if message.guild is not None:
                server = await self.database.get_server_settings(message.guild.id)
                if server is None:
                    await self.database.add_server_settings(message.guild)

    @commands.Cog.listener()
    async def on_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        message_sent = False
        if isinstance(exception, BadArgument):
            embed = discord.Embed(title=f"Error: {exception}", color=discord.Color.red())
            message = await ctx.send(embed=embed)
            message_sent = True

        if isinstance(exception, discord.Forbidden):
            embed = discord.Embed(title="Command Error!",
                                  description="I do not have permissions to do that",
                                  color=discord.Color.red())
            message = await ctx.send(embed=embed)
            message_sent = True

        if isinstance(exception, discord.HTTPException):
            embed = discord.Embed(title="Command Error!",
                                  description="Failed to preform that action, there was a Discord API error. "
                                              "Try again in a second",
                                  color=discord.Color.red())
            message = await ctx.send(embed=embed)
            message_sent = True

        if message_sent:
            await asyncio.sleep(5)
            await message.delete()

    @commands.command(name="announce")
    @commands.is_owner()
    async def announce(self, ctx, *, message):
        servers = self.bot.guilds
        user_ids = []
        users = []
        for server in servers:
            if server.owner.id not in user_ids:
                embed = discord.Embed(color=ctx.message.author.top_role.color,
                                      title='Announcement From Peribot\'s creator',
                                      description=message)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                try:
                    await server.owner.send(embed=embed)
                    user_ids.append(server.owner.id)
                    users.append(server.owner.name)
                except Exception as e:
                    logger.exception(str(e))
        await ctx.send(f"Announcement successfully sent to {', '.join(users)}")

    @commands.command(name="pipinstall")
    @commands.is_owner()
    async def pipinstall(self, ctx):
        results = subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])
        embed = discord.Embed(title=":white_check_mark: Successfully ran pip install",
                              description=f"```{results}```",
                              color=0x00df00)
        await ctx.channel.send(embed=embed)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)

    @commands.command()
    @commands.is_owner()
    async def send(self,ctx,  channel, *, message: str):
        if ctx.author.id == 204792579881959424:
            channel2 = self.bot.get_channel(int(channel))
            await channel2.send(message)

    @commands.command(name='setcolor', no_pm=True, aliases=["rolecolor", "color"])
    @commands.has_permissions(manage_roles=True)
    async def set_role_color(self, ctx, role: discord.Role, color: discord.Color):
        """
        Color the nickname of the participant. * Let there be bright colors and colors! *
        [!] In development.
        Arguments:
        color in HEX

        For example:
        !setcolor #FF0000
        """
        try:
            if not role.is_default():
                await role.edit(color=color)
                embed = discord.Embed(title=f"Changed the role color for {role.name} to {color}", color=color)
                await ctx.send(embed=embed)
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)
            else:
                embed = discord.Embed(title="Peribot cannot affect the default roles.")
                await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title="Peribot does not have permissions to change roles.")
            await ctx.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(title=f"Peribot failed to update {role.name}'s color")
            await ctx.send(embed=embed)
        except discord.InvalidArgument:
            embed = discord.Embed(title=f"Invalid Arguments!",
                                  description=f"{ctx.prefix}setcolor @Role [Hex Code or Generic Name]")
            await ctx.send(embed=embed)
        except discord.ext.commands.errors.BadArgument:
            embed = discord.Embed(title=f"Invalid Arguments!",
                                  description=f"{ctx.prefix}setcolor @Role [Hex Code or Generic Name]")
            await ctx.send(embed=embed)

    @commands.command('prefix', no_pm=True)
    @admin_or_permissions()
    async def prefix(self, ctx, prefix):
        if await self.database.update_server_settings(ctx.guild.id, prefix=prefix):
            await ctx.send("Preibot's command prefix has been updated!")
        else:
            await ctx.send("Preibot's command prefix failed to update!")


    @commands.command(name='nick', aliases=["setnick"])
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def nick(self, ctx, user: discord.Member, *, nick):
        if ctx.author.id == 309089769663496194 or ctx.author.id == 204792579881959424:
            await user.edit(nick=nick, reason="Jeep made me do it")
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)

    @commands.command(name='gitpull')
    async def git_pull(self, ctx):
        if ctx.author.id == 204792579881959424:
            git_dir = "./"
            try:
                g = git.cmd.Git(git_dir)
                updates = g.pull()
                embed = discord.Embed(title=":white_check_mark: Successfully pulled from repository",
                                      description=f"```{updates}```",
                                      color=0x00df00)
                await ctx.channel.send(embed=embed)
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)
            except Exception as e:
                errno, strerror = e.args
                embed = discord.Embed(title="Command Error!",
                                      description=f"Git Pull Error: {errno} - {strerror}",
                                      color=0xff0007)
                await ctx.channel.send(embed=embed)
        else:
            await ctx.send("You don't have access to this command!")



    @commands.command(name='servers')
    @is_bot_owner_check()
    async def servers(self, ctx):
        servers = self.bot.guilds
        serverNames = []
        member_count = 0
        for server in servers:
            serverNames.append(server.name)
            member_count += len(server.members)
        e = discord.Embed(title="Servers Peribot is apart of", description=", ".join(serverNames))
        e.add_field(name="Number of Servers", value=str(len(serverNames)))
        e.add_field(name="Number of Users", value=str(member_count))
        await ctx.send(embed=e)



def setup(bot):
    bot.add_cog(Management(bot))
