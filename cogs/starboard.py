import discord
import asyncio
from .utils.dataIO import dataIO
from discord.ext import commands
from cogs.utils import checks
import os
import re


class Star:
    """Quote board"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/star/settings.json")

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def starboard(self, ctx):
        """Commands for managing the starboard"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Thats not how you use this command. Use !help starboard for more info")

    @starboard.group(pass_context=True, name="role", aliases=["roles"])
    async def _roles(self, ctx):
        """Add or remove roles allowed to add to the starboard"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Thats not how you use this command. Use !help roles for more info")

    async def get_everyone_role(self, server):
        for role in server.roles:
            if role.is_everyone:
                return role

    async def check_server_emojis(self, server, emoji):
        server_emoji = None
        for emojis in server.emojis:
            if emojis.id in emoji:
                server_emoji = emojis
        return server_emoji

    @starboard.command(pass_context=True, name="setup", aliases=["set"])
    async def setup_starboard(self, ctx, channel: discord.Channel = None, emoji="⭐",
                              role: discord.Role = None):
        """Sets the starboard channel, emoji and role"""
        server = ctx.message.server
        if channel is None:
            channel = ctx.message.channel
        if "<" in emoji and ">" in emoji:
            emoji = await self.check_server_emojis(server, emoji)
            if emoji is None:
                await self.bot.send_message(ctx.message.channel,
                                            "That emoji is not on this server!")
                return
            else:
                emoji = ":" + emoji.name + ":" + emoji.id

        if role is None:
            role = await self.get_everyone_role(server)
        self.settings[server.id] = {"emoji": emoji,
                                    "channel": channel.id,
                                    "role": [role.id],
                                    "threshold": 0,
                                    "messages": [],
                                    "ignore": []}
        dataIO.save_json("data/star/settings.json", self.settings)
        await self.bot.say("Starboard set to {}".format(channel.mention))

    @starboard.command(pass_context=True, name="clear")
    async def clear_post_history(self, ctx):
        """Clears the database of previous starred messages"""
        self.settings[ctx.message.server.id]["messages"] = []
        dataIO.save_json("data/star/settings.json", self.settings)
        await self.bot.send_message(ctx.message.channel,
                                    "Done! I will no longer track starred messages older than right now.")

    @starboard.command(pass_context=True, name="ignore")
    async def toggle_channel_ignore(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel
        if channel.id in self.settings[ctx.message.server.id]["ignore"]:
            self.settings[ctx.message.server.id]["ignore"].remove(channel.id)
            await self.bot.send_message(ctx.message.channel,
                                        "{} removed from the ignored channel list!".format(
                                            channel.mention))
        else:
            self.settings[ctx.message.server.id]["ignore"].append(channel.id)
            await self.bot.send_message(ctx.message.channel,
                                        "{} added to the ignored channel list!".format(
                                            channel.mention))
        dataIO.save_json("data/star/settings.json", self.settings)

    @starboard.command(pass_context=True, name="emoji")
    async def set_emoji(self, ctx, emoji="⭐"):
        """Set the emoji for the starboard defaults to ⭐"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self.bot.send_message(ctx.message.channel,
                                        "I am not setup for the starboard on this server!\
                                         \nuse starboard set to set it up.")
            return
        is_server_emoji = False
        if "<" in emoji and ">" in emoji:
            emoji = await self.check_server_emojis(server, emoji)
            if emoji is None:
                await self.bot.send_message(ctx.message.channel,
                                            "That emoji is not on this server!")
                return
            else:
                is_server_emoji = True
                emoji = ":" + emoji.name + ":" + emoji.id
        self.settings[server.id]["emoji"] = emoji
        dataIO.save_json("data/star/settings.json", self.settings)
        if is_server_emoji:
            await self.bot.send_message(ctx.message.channel,
                                        "Starboard emoji set to <{}>.".format(emoji))
        else:
            await self.bot.send_message(ctx.message.channel,
                                        "Starboard emoji set to {}.".format(emoji))

    @starboard.command(pass_context=True, name="channel")
    async def set_channel(self, ctx, channel: discord.Channel = None):
        """Set the channel for the starboard"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self.bot.send_message(ctx.message.channel,
                                        "I am not setup for the starboard on this server!\
                                         \nuse starboard set to set it up.")
            return
        if channel is None:
            channel = ctx.message.channel
        self.settings[server.id]["channel"] = channel.id
        dataIO.save_json("data/star/settings.json", self.settings)
        await self.bot.send_message(ctx.message.channel,
                                    "Starboard channel set to {}.".format(channel.mention))

    @starboard.command(pass_context=True, name="threshold")
    async def set_threshold(self, ctx, threshold: int = 0):
        """Set the threshold before posting to the starboard"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self.bot.send_message(ctx.message.channel,
                                        "I am not setup for the starboard on this server!\
                                         \nuse starboard set to set it up.")
            return
        self.settings[server.id]["threshold"] = threshold
        dataIO.save_json("data/star/settings.json", self.settings)
        await self.bot.send_message(ctx.message.channel,
                                    "Starboard threshold set to {}.".format(threshold))

    @_roles.command(pass_context=True, name="add")
    async def add_role(self, ctx, role: discord.Role = None):
        """Add a role allowed to add messages to the starboard defaults to @everyone"""
        server = ctx.message.server
        if server.id not in self.settings:
            await self.bot.send_message(ctx.message.channel,
                                        "I am not setup for the starboard on this server!\
                                         \nuse starboard set to set it up.")
            return
        everyone_role = await self.get_everyone_role(server)
        if role is None:
            role = everyone_role
        if role.id in self.settings[server.id]["role"]:
            await self.bot.send_message(ctx.message.channel,
                                        "{} can already add to the starboard!".format(role.name))
            return
        if everyone_role.id in self.settings[server.id]["role"] and role != everyone_role:
            self.settings[server.id]["role"].remove(everyone_role.id)
        self.settings[server.id]["role"].append(role.id)
        dataIO.save_json("data/star/settings.json", self.settings)
        await self.bot.send_message(ctx.message.channel,
                                    "Starboard role set to {}.".format(role.name))

    @_roles.command(pass_context=True, name="remove", aliases=["del", "rem"])
    async def remove_role(self, ctx, role: discord.Role):
        """Remove a role allowed to add messages to the starboard"""
        server = ctx.message.server
        everyone_role = await self.get_everyone_role(server)
        if role.id in self.settings[server.id]["role"]:
            self.settings[server.id]["role"].remove(role.id)
        if self.settings[server.id]["role"] == []:
            self.settings[server.id]["role"].append(everyone_role.id)
        dataIO.save_json("data/star/settings.json", self.settings)
        await self.bot.send_message(ctx.message.channel,
                                    "{} removed from starboard.".format(role.name))

    async def check_roles(self, user, author, server):
        """Checks if the user is allowed to add to the starboard
           Allows bot owner to always add messages for testing
           disallows users from adding their own messages"""
        has_role = False
        for role in user.roles:
            if role.id in self.settings[server.id]["role"]:
                has_role = True
        if user is author:
            has_role = False
        if user.id == '204792579881959424':
            has_role = True
        return has_role

    async def check_is_posted(self, server, message):
        is_posted = False
        for past_message in self.settings[server.id]["messages"]:
            if message.id == past_message["original_message"]:
                is_posted = True
        return is_posted

    async def check_is_added(self, server, message):
        is_posted = False
        for past_message in self.settings[server.id]["messages"]:
            if message.id == past_message["new_message"]:
                is_posted = True
        return is_posted

    async def get_count(self, server, message):
        count = 0
        for past_message in list(self.settings[server.id]["messages"]):
            if message.id == past_message["original_message"]:
                count = past_message["count"]
        return count

    async def get_posted_message(self, server, message):
        msg_list = self.settings[server.id]["messages"]
        for past_message in msg_list:
            if message.id == past_message["original_message"]:
                msg = past_message
        msg_list.remove(msg)
        msg["count"] += 1
        msg_list.append(msg)
        self.settings[server.id]["messages"] = msg_list
        dataIO.save_json("data/star/settings.json", self.settings)
        return msg["new_message"], msg["count"]

    async def on_reaction_add(self, reaction, user):
        server = reaction.message.server
        msg = reaction.message
        if server.id not in self.settings:
            return
        if msg.channel.id in self.settings[server.id]["ignore"]:
            return
        if not await self.check_roles(user, msg.author, server):
            return
        react = self.settings[server.id]["emoji"]
        if react in str(reaction.emoji):
            threshold = self.settings[server.id]["threshold"]
            count = await self.get_count(server, msg)
            if await self.check_is_posted(server, msg):
                channel = self.bot.get_channel(self.settings[server.id]["channel"])
                msg_id, count = await self.get_posted_message(server, msg)
                if msg_id is not None:
                    msg_edit = await self.bot.get_message(channel, msg_id)
                    await self.bot.edit_message(msg_edit,
                                                new_content="{} **#{}**".format(reaction.emoji,
                                                                                count - 1))
                    return
            if count < threshold and threshold != 0:
                store = {"original_message": msg.id, "new_message": None, "count": count + 1}
                has_message = None
                for message in self.settings[server.id]["messages"]:
                    if msg.id == message["original_message"]:
                        has_message = message
                if has_message is not None:
                    self.settings[server.id]["messages"].remove(has_message)
                    self.settings[server.id]["messages"].append(store)
                    dataIO.save_json("data/star/settings.json", self.settings)
                else:
                    self.settings[server.id]["messages"].append(store)
                    dataIO.save_json("data/star/settings.json", self.settings)
                return
            if threshold == 0:
                count = 2
            # else:
            author = reaction.message.author
            channel = reaction.message.channel
            channel2 = self.bot.get_channel(id=self.settings[server.id]["channel"])
            if reaction.message.embeds != []:
                embed = reaction.message.embeds[0]  # .to_dict()
                # print(embed)
                em = discord.Embed(timestamp=reaction.message.timestamp)
                if "title" in embed:
                    em.title = embed["title"]
                if "thumbnail" in embed:
                    em.set_thumbnail(url=embed["thumbnail"]["url"])
                if "description" in embed:
                    em.description = msg.clean_content + "\n\n" + embed["description"]
                if "description" not in embed:
                    em.description = msg.clean_content
                if "url" in embed:
                    em.url = embed["url"]
                if "footer" in embed:
                    em.set_footer(text=embed["footer"]["text"])
                if "author" in embed:
                    postauthor = embed["author"]
                    if "icon_url" in postauthor:
                        if author.nick != None:
                            em.set_author(name=author.nick, icon_url=author.avatar_url)
                        else:
                            em.set_author(name=author.name, icon_url=author.avatar_url)
                    else:
                        if author.nick != None:
                            em.set_author(name=author.nick)
                        else:
                            em.set_author(name=author.name)
                if "author" not in embed:
                    if author.nick != None:
                        em.set_author(name=author.nick, icon_url=author.avatar_url)
                    else:
                        em.set_author(name=author.name, icon_url=author.avatar_url)
                if "color" in embed:
                    em.color = embed["color"]
                if "color" not in embed:
                    em.color = author.top_role.color
                if "image" in embed:
                    em.set_image(url=embed["image"]["url"])
                if embed["type"] == "image":
                    em.type = "image"
                    if ".png" in embed["url"] or ".jpg" in embed["url"]:
                        em.set_thumbnail(url="")
                        em.set_image(url=embed["url"])
                    else:
                        em.set_thumbnail(url=embed["url"])
                        em.set_image(
                            url=embed["url"] + "." + embed["thumbnail"]["url"].rsplit(".")[-1])
                if embed["type"] == "gifv":
                    em.type = "gifv"
                    em.set_thumbnail(url=embed["url"])
                    em.set_image(url=embed["url"] + ".gif")

            else:
                em = discord.Embed(timestamp=reaction.message.timestamp)
                em.color = author.top_role.color
                em.description = msg.content
                if author.nick != None:
                    em.set_author(name=author.nick, icon_url=author.avatar_url)
                else:
                    em.set_author(name=author.name, icon_url=author.avatar_url)
                if reaction.message.attachments != []:
                    em.set_image(url=reaction.message.attachments[0]["url"])
            em.set_footer(text='{} | {}'.format(channel.server.name, channel.name))
            post_msg = await self.bot.send_message(channel2,
                                                   "{} **#{}**".format(reaction.emoji, count - 1),
                                                   embed=em)
            past_message_list = self.settings[server.id]["messages"]
            past_message_list.append(
                {"original_message": msg.id, "new_message": post_msg.id, "count": count})
            dataIO.save_json("data/star/settings.json", self.settings)

        else:
            return


def check_folder():
    if not os.path.exists('data/star'):
        os.mkdir('data/star')


def check_files():
    data = {}
    f = 'data/star/settings.json'
    if not os.path.exists(f):
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(Star(bot))