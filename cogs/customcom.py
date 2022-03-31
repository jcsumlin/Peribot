import re

import discord
from discord.ext import commands
from loguru import logger

from .utils.chat_formatting import pagify, box
from .utils.database import Database


class CustomCommands(commands.Cog):
    """Custom commands

    Creates commands used to display text"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.group(aliases=["cc"], no_pm=True)
    async def customcom(self, ctx):
        """Custom commands management"""
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Error: That's not how you use this command!",
                              description="", color=discord.Color.red())
            e.add_field(name=f"{ctx.prefix}cc add [command] [result]", value="This will create a new custom command. Every time the [command] is invoked I will reply with the [result]")
            e.add_field(name=f"{ctx.prefix}cc edit [command] [result]", value="This will edit an existing custom command. Just incase you don't like my response any more")
            e.add_field(name=f"{ctx.prefix}cc delete [command]", value="This will completly delete a custom command from this server. I will no lover respond to it.")
            await ctx.send(embed=e)


    @customcom.command(name="add")
    async def cc_add(self, ctx, command : str, *, text):
        """Adds a custom command

        Example:
        [p]customcom add yourcommand Text you want

        CCs can be enhanced with arguments:
        https://twentysix26.github.io/Red-Docs/red_guide_command_args/
        """
        command = command.lower()
        if ctx.prefix in command:
            command = command.replace(ctx.prefix, '')
        if ctx.prefix in text:
            text = text.replace(ctx.prefix, '')
        if command in self.bot.commands:
            await ctx.send("That command is already a standard command.")
            return
        try:
            await self.database.add_custom_command(ctx.guild.id,
                                                   command,
                                                   text,
                                                   ctx.message.author.id)
            await ctx.send("Custom command successfully added.")
        except ValueError:
            await ctx.send("This command already exists. Use "
                           f"`{ctx.prefix}customcom edit` to edit it.")
        finally:
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)

    @customcom.command(name="edit")
    async def cc_edit(self, ctx, command: str, *, text):
        """Edits a custom command

        Example:
        [p]customcom edit yourcommand Text you want
        """
        command = command.lower()
        if ctx.prefix in command:
            command = command.replace(ctx.prefix, '')
        if ctx.prefix in text:
            text = text.replace(ctx.prefix, '')
        edit = await self.database.edit_custom_command(ctx.guild.id, command, text)
        if edit:
                await ctx.send("Custom command successfully edited.")
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)
        else:
            await ctx.send("That command doesn't exist. Use "
                               f"`{ctx.prefix}customcom add` to add it.")

    @customcom.command(name="delete")
    async def cc_delete(self, ctx, command: str):
        """Deletes a custom command

        Example:
        [p]customcom delete yourcommand"""
        guild = ctx.guild
        guild_id = guild.id
        cc = await self.database.get_custom_command(guild_id, command)
        if cc is not None:
            if await self.database.delete_custom_command(guild_id, command):
                await ctx.send("Custom command successfully deleted.")
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)
            else:
                await ctx.send(f"Failed to delete custom command `${command}`.")
        else:
            await ctx.send("That command doesn't exist.")

    @customcom.command(name="list")
    async def cc_list(self, ctx):
        """Shows custom commands list"""
        guild = ctx.guild
        guild_id = guild.id
        commands = await self.database.get_custom_commands(guild_id)
        if not commands:
            await ctx.send("There are no custom commands in this server."
                               f" Use `{ctx.prefix}customcom add` to start adding some.")
            return

        commands = ", ".join([ctx.prefix + c.command for c in commands])
        commands = "Custom commands:\n\n" + commands

        if len(commands) < 1500:
            await ctx.send(box(commands))
        else:
            for page in pagify(commands, delims=[" ", "\n"]):
                await ctx.send(box(page))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is True:
            return
        if len(message.content) < 2 or isinstance(message.channel, discord.DMChannel):
            return
        prefix = await self.get_prefix(message)
        if not prefix:
            return
        if prefix not in message.content:
            return

        cmd = message.content[len(prefix):]
        cmd = await self.database.get_custom_command(message.guild.id, cmd)
        if cmd is None:
            return
        cmd = self.format_cc(cmd, message)
        await message.channel.send(cmd)

    async def get_prefix(self, message):
        try:
            server = await self.database.get_server_settings(message.guild.id)
            if server is None:
                return '!'
            return server.prefix
        except Exception as error:
            logger.exception(error)
        return False

    def format_cc(self, command, message):
        results = re.findall("\{([^}]+)\}", command)
        for result in results:
            param = self.transform_parameter(result, message)
            command = command.replace("{" + result + "}", param)
        return command

    def transform_parameter(self, result, message):
        """
        For security reasons only specific objects are allowed
        Internals are ignored
        """
        raw_result = "{" + result + "}"
        objects = {
            "message": message,
            "author": message.author,
            "channel": message.channel,
            "guild": message.guild
        }
        if result in objects:
            return str(objects[result])
        try:
            first, second = result.split(".")
        except ValueError:
            return raw_result
        if first in objects and not second.startswith("_"):
            first = objects[first]
        else:
            return raw_result
        return str(getattr(first, second, raw_result))


def setup(bot):
    bot.add_cog(CustomCommands(bot))
