import configparser
import os
import re

import discord
from discord.ext import commands
from loguru import logger

from .utils.chat_formatting import pagify, box
from .utils.dataIO import dataIO


class CustomCommands(commands.Cog):
    """Custom commands

    Creates commands used to display text"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/customcom/commands.json"
        self.c_commands = dataIO.load_json(self.file_path)
        self.config = configparser.ConfigParser()
        self.config.read('../auth.ini')

    async def cog_before_invoke(self, ctx):
        if not os.path.exists("data/customcom"):
            print("Creating data/customcom folder...")
            os.makedirs("data/customcom")

        f = "data/customcom/commands.json"
        if not dataIO.is_valid_json(f):
            print("Creating empty commands.json...")
            dataIO.save_json(f, {})

    @commands.group(aliases=["cc"], no_pm=True)
    async def customcom(self, ctx):
        """Custom commands management"""
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Error: That's not how you use this command!",
                              description="", color=discord.Color.red())
            e.add_field(name="!cc add [command] [result]", value="This will create a new custom command. Every time the [command] is invoked I will reply with the [result]")
            e.add_field(name="!cc edit [command] [result]", value="This will edit an existing custom command. Just incase you don't like my response any more")
            e.add_field(name="!cc delete [command]", value="This will completly delete a custom command from this server. I will no lover respond to it.")
            await ctx.send(embed=e)


    @customcom.command(name="add", )
    async def cc_add(self, ctx, command : str, *, text):
        """Adds a custom command

        Example:
        [p]customcom add yourcommand Text you want

        CCs can be enhanced with arguments:
        https://twentysix26.github.io/Red-Docs/red_guide_command_args/
        """
        guild = ctx.guild
        guild_id = str(guild.id)
        command = command.lower()
        if "!" in command:
            command = command.replace('!', '')
        if '!' in text:
            text = text.replace('!', '')
        if command in self.bot.commands:
            await ctx.send("That command is already a standard command.")
            return
        if guild_id not in self.c_commands:
            self.c_commands[guild_id] = {}
        cmdlist = self.c_commands[guild_id]
        if command not in cmdlist:
            cmdlist[command] = text
            self.c_commands[guild_id] = cmdlist
            dataIO.save_json(self.file_path, self.c_commands)
            await ctx.send("Custom command successfully added.")
        else:
            await ctx.send("This command already exists. Use "
                               "`{}customcom edit` to edit it."
                               "".format(ctx.prefix))

    @customcom.command(name="edit", )
    async def cc_edit(self, ctx, command : str, *, text):
        """Edits a custom command

        Example:
        [p]customcom edit yourcommand Text you want
        """
        guild = ctx.guild
        guild_id = str(guild.id)
        command = command.lower()
        if "!" in command:
            command = command.replace('!', '')
        if '!' in text:
            text = text.replace('!', '')
        if guild_id in self.c_commands:
            cmdlist = self.c_commands[guild_id]
            if command in cmdlist:
                cmdlist[command] = text
                self.c_commands[guild_id] = cmdlist
                dataIO.save_json(self.file_path, self.c_commands)
                await ctx.send("Custom command successfully edited.")
            else:
                await ctx.send("That command doesn't exist. Use "
                                   "`{}customcom add` to add it."
                                   "".format(ctx.prefix))
        else:
            await ctx.send("There are no custom commands in this server."
                               " Use `{}customcom add` to start adding some."
                               "".format(ctx.prefix))

    @customcom.command(name="delete", )
    async def cc_delete(self, ctx, command : str):
        """Deletes a custom command

        Example:
        [p]customcom delete yourcommand"""
        guild = ctx.guild
        guild_id = str(guild.id)

        command = command.lower()
        if guild_id in self.c_commands:
            cmdlist = self.c_commands[guild_id]
            if command in cmdlist:
                cmdlist.pop(command, None)
                self.c_commands[guild_id] = cmdlist
                dataIO.save_json(self.file_path, self.c_commands)
                await ctx.send("Custom command successfully deleted.")
            else:
                await ctx.send("That command doesn't exist.")
        else:
            await ctx.send("There are no custom commands in this guild."
                               " Use `{}customcom add` to start adding some."
                               "".format(ctx.prefix))

    @customcom.command(name="list", )
    async def cc_list(self, ctx):
        """Shows custom commands list"""
        guild = ctx.guild
        guild_id = str(guild.id)

        commands = self.c_commands.get(guild_id, {})

        if not commands:
            await ctx.send("There are no custom commands in this server."
                               " Use `{}customcom add` to start adding some."
                               "".format(ctx.prefix))
            return

        commands = ", ".join([ctx.prefix + c for c in sorted(commands)])
        commands = "Custom commands:\n\n" + commands

        if len(commands) < 1500:
            await ctx.send(box(commands))
        else:
            for page in pagify(commands, delims=[" ", "\n"]):
                await self.bot.whisper(box(page))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot is True:
            return
        if len(message.content) < 2 or isinstance(message.channel, discord.DMChannel):
            return

        guild = message.guild
        guild_id = str(guild.id)
        prefix = self.get_prefix(message)

        if not prefix:
            return

        if guild_id in self.c_commands:
            cmdlist = self.c_commands[guild_id]
            cmd = message.content[len(prefix):]
            if cmd in cmdlist:
                cmd = cmdlist[cmd]
                cmd = self.format_cc(cmd, message)
                await message.channel.send(cmd)
            elif cmd.lower() in cmdlist:
                cmd = cmdlist[cmd.lower()]
                cmd = self.format_cc(cmd, message)
                await message.channel.send(cmd)

    def get_prefix(self, message):
        try:
            p = self.config.get('discord', 'PREFIX')
            if message.content.startswith(p):
                return p
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
            "message" : message,
            "author"  : message.author,
            "channel" : message.channel,
            "guild"  : message.guild
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
