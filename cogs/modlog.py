import datetime
import os

import discord
from discord.ext import commands
from loguru import logger

from cogs.utils.dataIO import dataIO
from .utils import checks


class Modlog(commands.Cog):
    """Logs moderation stuff."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/modlog/settings.json")

    @commands.group(no_pm=True)
    @checks.mod_or_permissions()
    async def modlogset(self, ctx):
        """Set the settings for the moderation logs."""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(title="Command Error!", description="That's not how you use this command!")
            await ctx.send(embed=embed)
        if str(ctx.message.guild.id) not in self.settings:
            self.settings[str(ctx.message.guild.id)] = {'channel': None, 'disabled': False, 'join': True, 'leave': True,
                                                        'voicechat': True, 'msgedit': True, 'msgdelete': True,
                                                        'roleedit': True, 'ban': True, 'reactions': True,
                                                        'channels': True,
                                                        'nicknames': True}
            self.save_settings()

    @modlogset.command(no_pm=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel the bot should log to."""
        self.settings[str(ctx.message.guild.id)]['channel'] = channel.id
        self.save_settings()
        await ctx.send("Channel set, I will now log to {}.".format(channel.mention))

    @modlogset.command(no_pm=True)
    async def disable(self, ctx):
        """Disable the logging system completely."""
        if not self.settings[str(ctx.message.guild.id)]['disabled']:
            self.settings[str(ctx.message.guild.id)]['disabled'] = True
            self.save_settings()
            await ctx.send("Logging system has been disabled.")
        else:
            self.settings[str(ctx.message.guild.id)]['disabled'] = False
            self.save_settings()
            await ctx.send("Logging system has been enabled.")

    @modlogset.command(no_pm=True)
    async def toggle(self, ctx, module=None):
        """Toggle what the bot should and what the bot shouldn't log."""
        server = ctx.message.guild
        modules = ['join', 'leave', 'ban', 'voicechat', 'msgedit', 'msgdelete', 'roleedit', 'channels', 'nicknames']
        if module == None:
            msg = "```py"
            try:
                msg += "\nChannel: " + str(self.settings[str(server.id)]['channel'])
                msg += "\nDisabled: " + str(self.settings[str(server.id)]['disabled'])
                msg += "\nJoin: " + str(self.settings[str(server.id)]['join'])
                msg += "\nLeave: " + str(self.settings[str(server.id)]['leave'])
                msg += "\nBan: " + str(self.settings[str(server.id)]['ban'])
                msg += "\nVoicechat: " + str(self.settings[str(server.id)]['voicechat'])
                msg += "\nMessage edit: " + str(self.settings[str(server.id)]['msgedit'])
                msg += "\nMessage delete: " + str(self.settings[str(server.id)]['msgdelete'])
                msg += "\nRole edit: " + str(self.settings[str(server.id)]['roleedit'])
                msg += "\nChannels: " + str(self.settings[str(server.id)]['channels'])
                msg += "\nNicknames: " + str(self.settings[str(server.id)]['nicknames'])
            except KeyError:
                pass
            msg += "\n\nFalse = not being logged.\nTrue = being logged."
            msg += "```"
            await ctx.send(msg + "You can toggle\n{}.".format(", ".join(modules)))

        elif module.lower() == 'join':
            if self.settings[str(server.id)]['join']:
                self.settings[str(server.id)]['join'] = False
                self.save_settings()
                await ctx.send("Join logging has been disabled.")
            else:
                self.settings[str(server.id)]['join'] = True
                self.save_settings()
                await ctx.send("Join logging has been enabled.")

        elif module.lower() == 'leave':
            if self.settings[str(server.id)]['leave']:
                self.settings[str(server.id)]['leave'] = False
                self.save_settings()
                await ctx.send("Leave (and kick) logging has been disabled.")
            else:
                self.settings[str(server.id)]['leave'] = True
                self.save_settings()
                await ctx.send("Leave (and kick) logging has been enabled.")

        elif module.lower() == 'ban':
            if self.settings[str(server.id)]['ban']:
                self.settings[str(server.id)]['ban'] = False
                self.save_settings()
                await ctx.send("Ban logging has been disabled.")
            else:
                self.settings[str(server.id)]['ban'] = True
                self.save_settings()
                await ctx.send("Ban logging has been enabled.")

        elif module.lower() == 'voicechat':
            if self.settings[str(server.id)]['voicechat']:
                self.settings[str(server.id)]['voicechat'] = False
                self.save_settings()
                await ctx.send("Voicechat logging has been disabled.")
            else:
                self.settings[str(server.id)]['voicechat'] = True
                self.save_settings()
                await ctx.send("Voicechat logging has been enabled.")

        elif module.lower() == 'msgedit':
            if self.settings[str(server.id)]['msgedit']:
                self.settings[str(server.id)]['msgedit'] = False
                self.save_settings()
                await ctx.send("Message edit has been disabled.")
            else:
                self.settings[str(server.id)]['msgedit'] = True
                self.save_settings()
                await ctx.send("Message edit has been enabled.")

        elif module.lower() == 'msgdelete':
            if self.settings[str(server.id)]['msgdelete']:
                self.settings[str(server.id)]['msgdelete'] = False
                self.save_settings()
                await ctx.send("Message delete has been disabled.")
            else:
                self.settings[str(server.id)]['msgdelete'] = True
                self.save_settings()
                await ctx.send("Message delete has been enabled.")

        elif module.lower() == 'roleedit':
            if self.settings[str(server.id)]['roleedit']:
                self.settings[str(server.id)]['roleedit'] = False
                self.save_settings()
                await ctx.send("Role edit has been disabled.")
            else:
                self.settings[str(server.id)]['roleedit'] = True
                self.save_settings()
                await ctx.send("Role edit has been enabled.")

        elif module.lower() == 'channels':
            if 'channels' not in self.settings[str(server.id)]:
                self.settings[str(server.id)]['channels'] = True
                self.save_settings()
                return
            elif self.settings[str(server.id)]['channels']:
                self.settings[str(server.id)]['channels'] = False
                self.save_settings()
                await ctx.send("Channels have been disabled.")
            else:
                self.settings[str(server.id)]['channels'] = True
                self.save_settings()
                await ctx.send("Channels have been enabled.")

        elif module.lower() == 'nicknames':
            if 'nicknames' not in self.settings[str(server.id)]:
                self.settings[str(server.id)]['nicknames'] = True
                self.save_settings()
                await ctx.send("Nicknames have been enabled.")
            elif self.settings[str(server.id)]['nicknames']:
                self.settings[str(server.id)]['nicknames'] = False
                self.save_settings()
                await ctx.send("Nicknames have been disabled.")
            else:
                self.settings[str(server.id)]['nicknames'] = True
                self.save_settings()
                await ctx.send("Nicknames have been enabled.")

        else:
            await ctx.send("That module cannot be toggled, you can toggle\n{}.".format(", ".join(modules)))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.is_module(member.guild, 'join'):
            await self.log(member.guild, "`[{}]` :inbox_tray: **Member Join Log**\n"
                                         "```Member Joined: {}```".format(self.get_time(), str(member)))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.is_module(member.guild, 'leave'):
            await self.log(member.guild, "`[{}]` :outbox_tray: **Member Leave/Kick Log**\n"
                                         "```Member Left/Kicked: {}```".format(self.get_time(), str(member)))

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if self.is_module(member.guild, 'ban'):
            await self.log(member.guild, "`[{}]` :hammer: **Member Ban Log**\n"
                                         "```Member Banned: {}```".format(self.get_time(), str(member)))

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        await self.log(member.guild, "`[{}]` :hammer: **Member Un-Ban Log**\n"
                                     "```Member Un-Banned: {}```".format(self.get_time(), str(member)))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None or after.channel is None:
            return
        if self.is_module(before.channel.guild, 'voicechat'):
            await self.log(before.channel.guild, "`[{}]` :bangbang: **Voicechat Log**\n"
                                                 "```User: {}"
                                                 "\nBefore: {}".format(self.get_time(),
                                                                       str(member),
                                                                       str(before.channel)) +
                           f"\n\tServer Muted: {before.mute}" +
                           f"\n\tServer Deafened: {before.deaf}" +
                           "\nAfter: {}".format(str(after.channel)) +
                           f"\n\tServer Muted: {after.mute}" +
                           f"\n\tServer Deafened: {after.deaf}```")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if (before.guild != None) and (before.author == before.guild.me):
            return
        if self.is_module(before.guild, 'msgedit'):
            if before.content != after.content:
                await self.log(before.guild, "`[{}]` :pencil2: **Message Edit Log**\n"
                                             "```User: {}"
                                             "\nChannel: {}"
                                             "\nBefore: {}".format(self.get_time(), before.author.name,
                                                                   before.channel.name, before.content) +
                               "\nAfter: {}```".format(after.content))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == message.guild.me:
            return
        if self.is_module(message.guild, 'msgdelete'):
            await self.log(message.guild, "`[{}]` :wastebasket: **Message Delete Log**\n"
                                          "```User: {}\n"
                                          "Channel: {}\n"
                                          "Message: {}\n```".format(self.get_time(), str(message.author),
                                                                    str(message.channel), message.content))

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if self.is_module(role.guild, 'roleedit'):
            perms = role.permissions
            await self.log(role.guild, "`[{}]` :game_die: **Role Create Log**\n"
                                       "```py\nRole: {}"
                                       "\nColour: {}"
                                       "\nPermissions:"
                                       "\n\tMentionable: {}"
                                       "\n\tDisplay Separatly: {}"
                                       "\n\tAdministrator: {}"
                                       "\n\tCan ban members: {}"
                                       "\n\tCan kick members: {}"
                                       "\n\tCan change nickname: {}"
                                       "\n\tCan connect to voice channels: {}"
                                       "\n\tCan create instant invites: {}"
                                       "\n\tCan deafen members: {}"
                                       "\n\tCan embed links: {}"
                                       "\n\tCan manage channels: {}"
                                       "\n\tCan manage emojis: {}"
                                       "\n\tCan manage messages: {}"
                                       "\n\tCan manage nicknames: {}"
                                       "\n\tCan manage roles: {}"
                                       "\n\tCan manage server: {}"
                                       "\n\tCan mention everyone: {}"
                                       "\n\tCan move members: {}"
                                       "\n\tCan mute members: {}"
                                       "\n\tPriority speaker: {}"
                                       "\n\tCan Stream: {}"
                                       "\n\tCan read message history: {}```".format(self.get_time(), str(role.name),
                                                                                    str(role.colour),
                                                                                    str(role.mentionable),
                                                                                    str(role.hoist),
                                                                                    str(perms.administrator),
                                                                                    str(perms.ban_members),
                                                                                    str(perms.kick_members),
                                                                                    str(perms.change_nickname),
                                                                                    str(perms.connect),
                                                                                    str(perms.create_instant_invite),
                                                                                    str(perms.deafen_members),
                                                                                    str(perms.embed_links),
                                                                                    str(perms.manage_channels),
                                                                                    str(perms.manage_emojis),
                                                                                    str(perms.manage_messages),
                                                                                    str(perms.manage_nicknames),
                                                                                    str(perms.manage_roles),
                                                                                    str(perms.manage_guild),
                                                                                    str(perms.mention_everyone),
                                                                                    str(perms.move_members),
                                                                                    str(perms.mute_members),
                                                                                    str(perms.read_message_history),
                                                                                    str(perms.send_messages),
                                                                                    str(perms.speak),
                                                                                    str(perms.use_voice_activation),
                                                                                    str(perms.manage_webhooks),
                                                                                    str(perms.priority_speaker),
                                                                                    str(perms.stream),
                                                                                    str(perms.add_reactions)))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if self.is_module(role.guild, 'roleedit'):
            await self.log(role.guild, "`[{}]` :game_die: **Role Delete Log**\n"
                                       "```Role: {}```".format(self.get_time(), role.name))

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if self.is_module(before.guild, 'roleedit'):
            if not (before.permissions == after.permissions) or not (before.color == after.color):
                perms = before.permissions
                perms2 = after.permissions
                await self.log(before.guild, "`[{}]` :game_die: **Role Edit Log**\n"
                                             "```py\nBefore:\nRole: {}"
                                             "\nColor: {}"
                                             "\nPermissions:"
                                             "\n\tMentionable: {}"
                                             "\n\tDisplay Separately: {}"
                                             "\n\tAdministrator: {}"
                                             "\n\tCan ban members: {}"
                                             "\n\tCan kick members: {}"
                                             "\n\tCan change nickname: {}"
                                             "\n\tCan connect to voice channels: {}"
                                             "\n\tCan create instant invites: {}"
                                             "\n\tCan deafen members: {}"
                                             "\n\tCan embed links: {}"
                                             "\n\tCan manage channels: {}"
                                             "\n\tCan manage emojis: {}"
                                             "\n\tCan manage messages: {}"
                                             "\n\tCan manage nicknames: {}"
                                             "\n\tCan manage roles: {}"
                                             "\n\tCan manage server: {}"
                                             "\n\tCan mention everyone: {}"
                                             "\n\tCan move members: {}"
                                             "\n\tCan mute members: {}"
                                             "\n\tPriority speaker: {}"
                                             "\n\tCan Stream: {}"
                                             "\n\tCan read message history: {}".format(self.get_time(),
                                                                                       str(before.name),
                                                                                       str(before.colour),
                                                                                       str(before.mentionable),
                                                                                       str(before.hoist),
                                                                                       str(perms.administrator),
                                                                                       str(perms.ban_members),
                                                                                       str(perms.kick_members),
                                                                                       str(perms.change_nickname),
                                                                                       str(perms.connect),
                                                                                       str(perms.create_instant_invite),
                                                                                       str(perms.deafen_members),
                                                                                       str(perms.embed_links),
                                                                                       str(perms.manage_channels),
                                                                                       str(perms.manage_emojis),
                                                                                       str(perms.manage_messages),
                                                                                       str(perms.manage_nicknames),
                                                                                       str(perms.manage_roles),
                                                                                       str(perms.manage_guild),
                                                                                       str(perms.mention_everyone),
                                                                                       str(perms.move_members),
                                                                                       str(perms.mute_members),
                                                                                       str(perms.priority_speaker),
                                                                                       str(perms.stream),
                                                                                       str(perms.read_message_history),
                                                                                       str(perms.send_messages),
                                                                                       str(perms.speak),
                                                                                       str(perms.use_voice_activation),
                                                                                       str(perms.manage_webhooks),
                                                                                       str(perms.add_reactions)) +
                               "\n\nAfter:\nRole: {}"
                               "\nColor: {}"
                               "\nPermissions:"
                               "\n\tMentionable: {}"
                               "\n\tDisplay Separatly: {}"
                               "\n\tAdministrator: {}"
                               "\n\tCan ban members: {}"
                               "\n\tCan kick members: {}"
                               "\n\tCan change nickname: {}"
                               "\n\tCan connect to voice channels: {}"
                               "\n\tCan create instant invites: {}"
                               "\n\tCan deafen members: {}"
                               "\n\tCan embed links: {}"
                               "\n\tCan manage channels: {}"
                               "\n\tCan manage emojis: {}"
                               "\n\tCan manage messages: {}"
                               "\n\tCan manage nicknames: {}"
                               "\n\tCan manage roles: {}"
                               "\n\tCan manage server: {}"
                               "\n\tCan mention everyone: {}"
                               "\n\tCan move members: {}"
                               "\n\tCan mute members: {}"
                               "\n\tPriority speaker: {}"
                               "\n\tCan Stream: {}"
                               "\n\tCan read message history: {}```".format(str(after.name), str(after.colour),
                                                                            str(after.mentionable), str(after.hoist),
                                                                            str(perms2.administrator),
                                                                            str(perms2.ban_members),
                                                                            str(perms2.kick_members),
                                                                            str(perms2.change_nickname),
                                                                            str(perms2.connect),
                                                                            str(perms2.create_instant_invite),
                                                                            str(perms2.deafen_members),
                                                                            str(perms2.embed_links),
                                                                            str(perms2.manage_channels),
                                                                            str(perms2.manage_emojis),
                                                                            str(perms2.manage_messages),
                                                                            str(perms2.manage_nicknames),
                                                                            str(perms2.manage_roles),
                                                                            str(perms2.manage_guild),
                                                                            str(perms2.mention_everyone),
                                                                            str(perms2.move_members),
                                                                            str(perms2.mute_members),
                                                                            str(perms2.priority_speaker),
                                                                            str(perms2.stream),
                                                                            str(perms2.read_message_history),
                                                                            str(perms2.send_messages),
                                                                            str(perms2.speak),
                                                                            str(perms2.use_voice_activation),
                                                                            str(perms2.manage_webhooks),
                                                                            str(perms2.add_reactions)))

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if self.is_module(channel.guild, 'channels'):
            await self.log(channel.guild, "`[{}]` :pick: **Channel Create Log**\n"
                                          "```Channel: {}```".format(self.get_time(), channel.name))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if self.is_module(channel.guild, 'channels'):
            await self.log(channel.guild, "`[{}]` :pick: **Channel Delete Log**\n"
                                          "```Channel: {}```".format(self.get_time(), channel.name))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if self.is_module(before.guild, 'channels'):
            if not before.name == after.name:
                await self.log(before.guild, "`[{}]` :pick: **Channel Edit Log**\n"
                                             "```Before: {}\nAfter: {}```".format(self.get_time(), before.name,
                                                                                  after.name))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if self.is_module(before.guild, 'nicknames'):
            if not before.nick == after.nick:
                await self.log(before.guild, "`[{}]` :warning: **Nickname Change Log**\n"
                                             "```User: {}\nBefore: {}\nAfter: {}```".format(self.get_time(),
                                                                                            str(before), before.nick,
                                                                                            after.nick))

    async def log(self, server, message):
        channel = discord.utils.get(server.channels, id=self.settings[str(server.id)]['channel'])
        try:
            await channel.send(message)
        except:
            pass

    def get_time(self):
        return datetime.datetime.now().strftime("%X")

    def is_module(self, server, module):
        if server == None:
            return False
        elif str(server.id) not in self.settings:
            return False
        elif not self.settings[str(server.id)]['disabled']:
            if (self.settings[str(server.id)]['channel'] != None) and (module in self.settings[str(server.id)]) and (
                    self.settings[str(server.id)][module]):
                return True
            else:
                return False
        else:
            return False

    def save_settings(self):
        dataIO.save_json("data/modlog/settings.json", self.settings)


def check_folders():
    if not os.path.exists("data/modlog"):
        logger.debug("Creating data/modlog folder...")
        os.makedirs("data/modlog")


def check_files():
    if not os.path.exists("data/modlog/settings.json"):
        logger.debug("Creating data/modlog/settings.json file...")
        dataIO.save_json("data/modlog/settings.json", {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Modlog(bot))
