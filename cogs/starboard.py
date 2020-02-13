import discord
from discord.ext import commands

from .utils.database import Database
from .utils.genericResponseBuilder import commandSuccess, commandError


class Star(commands.Cog):
    """Quote board"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.group()
    @commands.has_permissions(manage_channels=True)
    async def starboard(self, ctx):
        """Commands for managing the starboard"""
        if ctx.invoked_subcommand is None:
            await commandError(ctx, "Thats not how you use this command.\n"
                                    f"**{ctx.prefix}starboard setup [channel] [emoji | :star:] [allowed role | @everyone]**\nSets up Starboard. Optional parameters with defaults are displayed with a pipe \"|\" character\n"
                                    f"**{ctx.prefix}starboard ignore [channel]**\nTells the Starboard to ignore a specific channel\n"
                                    f"**{ctx.prefix}starboard emoji [emoji]**\nSets the emoji that the Starboard tracks\n"
                                    f"**{ctx.prefix}starboard channel [channel]**\nSets the channel where the starboard is housed\n"
                                    f"**{ctx.prefix}starboard threshold [integer]**\nSets the threshold of reactions needed to be posted on the starboard\n"
                                    f"**{ctx.prefix}starboard add [role]**\nAdd a role that's allowed to make it on the starboard\n"
                                    f"**{ctx.prefix}starboard remove [role]**\nRemoves a role from the allowed roles list\n")

    @starboard.group(name="role", aliases=["roles"])
    async def _roles(self, ctx):
        """Add or remove roles allowed to add to the starboard"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Thats not how you use this command. Use !help roles for more info")

    async def get_everyone_role(self, guild):
        for role in guild.roles:
            if role.is_default():
                return role

    async def check_guild_emojis(self, guild, emoji):
        guild_emoji = None
        for emojis in guild.emojis:
            if str(emojis.id) in emoji:
                guild_emoji = emojis
        return guild_emoji

    @starboard.command(name="setup", aliases=["set"])
    async def setup_starboard(self, ctx, channel: discord.TextChannel = None, emoji="⭐",
                              role: discord.Role = None):
        """Sets the starboard channel, emoji and role"""
        guild = ctx.guild
        if channel is None:
            channel = ctx.channel
        if "<" in emoji and ">" in emoji:
            emoji = await self.check_guild_emojis(guild, emoji)
            if emoji is None:
                return await commandError(ctx, "That emoji is not on this server!")
            else:
                emoji = ":" + emoji.name + ":" + emoji.id

        if role is None:
            role = await self.get_everyone_role(guild)
        if await self.database.get_starboard_settings(ctx.guild.id) is not None:
            return await commandError(ctx, f'Starboard already setup!\nUse **{ctx.prefix}starboard channel #[channel]** to reassign the channel for the starboard.')
        await self.database.post_starboard_settings(ctx.guild.id,
                                              True,
                                              channel.id,
                                              emoji,
                                              0)
        await self.database.post_starboard_role(ctx.guild.id, role_id=role.id)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)
        await commandSuccess(ctx, f"Starboard set to {channel.mention}")

    @starboard.command(name="clear")
    async def clear_post_history(self, ctx):
        """Clears the database of previous starred messages"""

        if await self.database.clear_starboard(ctx.guild.id):
            await self.database.audit_record(ctx.guild.id,
                                             ctx.guild.name,
                                             ctx.message.content,
                                             ctx.message.author.id)
            await commandSuccess(ctx, "Done! I will no longer track starred messages older than right now.")
        else:
            await commandError(ctx, "Could not clear starboard!")

    @starboard.command(name="ignore")
    async def toggle_channel_ignore(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        channels = await self.database.get_ignored_starboard_channels(ctx.guild.id)
        if channel.id in channels:
            if await self.database.delete_starboard_ignored_channel(ctx.guild.id, channel.id):
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)
                await commandSuccess(ctx, f"{channel.mention} removed from the ignored channel list!")
        else:
            if await self.database.add_starboard_ignored_channel(ctx.guild.id, channel.id):
                await self.database.audit_record(ctx.guild.id,
                                                 ctx.guild.name,
                                                 ctx.message.content,
                                                 ctx.message.author.id)
                await commandSuccess(ctx, f"{channel.mention} added to the ignored channel list!")

    @starboard.command(name="emoji")
    async def set_emoji(self, ctx, emoji="⭐"):
        """Set the emoji for the starboard defaults to ⭐"""
        guild = ctx.guild
        starboard_settings = await self.database.get_starboard_settings(ctx.guild.id)
        if starboard_settings is None:
            return await commandError(ctx, f"I am not setup for the starboard on this server!\
                                         \nuse **{ctx.prefix}starboard set** to set it up.")
        is_guild_emoji = False
        if "<" in emoji and ">" in emoji:
            emoji = await self.check_guild_emojis(guild, emoji)
            if emoji is None:
                await ctx.send("That emoji is not on this server!")
                return
            else:
                is_guild_emoji = True
                emoji = ":" + emoji.name + ":" + emoji.id
        await self.database.update_starboard_settings(server_id=guild.id, emoji=emoji)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)
        if is_guild_emoji:
            await commandSuccess(ctx, f"Starboard emoji set to <{emoji}>.")
        else:
            await commandSuccess(ctx, f"Starboard emoji set to {emoji}.")

    @starboard.command(name="channel")
    async def set_channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel for the starboard"""
        guild = ctx.guild
        settings = await self.database.get_starboard_settings(guild.id)
        if settings is None:
            return await commandError(ctx, f"I am not setup for the starboard on this server!\
                                                     \nuse **{ctx.prefix}starboard set** to set it up.")
        if channel is None:
            channel = ctx.channel
        await self.database.update_starboard_settings(ctx.guild.id, channel_id=channel.id)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)
        await ctx.send(f"Starboard channel set to {channel.mention}.")

    @starboard.command(name="threshold")
    async def set_threshold(self, ctx, threshold: int = 0):
        """Set the threshold before posting to the starboard"""
        guild = ctx.guild
        settings = await self.database.get_starboard_settings(guild.id)
        if settings is None:
            return await commandError(ctx, f"I am not setup for the starboard on this server!\
                                                            \nuse **{ctx.prefix}starboard set** to set it up.")
        await self.database.update_starboard_settings(guild.id, threshold=threshold)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)
        await ctx.send(f"Starboard threshold set to {threshold}.")

    @_roles.command(name="add")
    async def add_role(self, ctx, role: discord.Role = None):
        """Add a role allowed to add messages to the starboard defaults to @everyone"""
        guild = ctx.guild
        settings = await self.database.get_starboard_settings(guild.id)
        if settings is None:
            return await commandError(ctx, f"I am not setup for the starboard on this server!\
                                                     \nuse **{ctx.prefix}starboard set** to set it up.")
        current_roles = await self.database.get_starboard_roles(guild.id)
        everyone_role = await self.get_everyone_role(guild)
        if role is None:
            role = everyone_role
        if role.id in current_roles:
            return await ctx.send(f"{role.name} can already add to the starboard!")
        if everyone_role.id in current_roles and role != everyone_role:
            await self.database.delete_starboard_role(guild.id, everyone_role.id)
        await self.database.post_starboard_role(guild.id, role.id)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)
        await ctx.send(f"{role.name} can now post to the Starboard")

    @_roles.command(name="remove", aliases=["del", "rem"])
    async def remove_role(self, ctx, role: discord.Role):
        """Remove a role allowed to add messages to the starboard"""
        guild = ctx.guild
        settings = await self.database.get_starboard_settings(guild.id)
        if settings is None:
            return await commandError(ctx, f"I am not setup for the starboard on this server!\
                                                            \nuse **{ctx.prefix}starboard set** to set it up.")
        current_roles = await self.database.get_starboard_roles(guild.id)
        everyone_role = await self.get_everyone_role(guild)
        if role.id in current_roles:
            await self.database.delete_starboard_role(guild.id, role.id)
            current_roles.remove(role.id)
        if current_roles == []:
            await self.database.post_starboard_role(guild.id, everyone_role.id)
        await self.database.audit_record(ctx.guild.id,
                                         ctx.guild.name,
                                         ctx.message.content,
                                         ctx.message.author.id)
        await ctx.send(f"{role.name} removed from starboard.")

    async def check_roles(self, user, author, guild):
        """Checks if the user is allowed to add to the starboard
           Allows bot owner to always add messages for testing
           disallows users from adding their own messages"""
        has_role = False
        roles = await self.database.get_starboard_roles(guild.id)
        for role in user.roles:
            if role.id in roles:
                has_role = True
        if user is author:
            has_role = False
        if user.id == 204792579881959424:
            has_role = True
        return has_role

    async def check_is_posted(self, guild, message):
        """
        Check if message is being tracked and on the starboard
        :param guild: Discord server
        :param message: message that was stared
        :return:
        """
        is_posted = False
        message = await self.database.get_one_starboard_message(guild.id, message.id)
        if message is not None and message.starboard_message_id is not None:
            is_posted = True
        return is_posted

    async def check_is_added(self, guild, message):
        """
        Check if message is being tracked
        :param guild: 
        :param message: 
        :return: 
        """
        is_tracked = False
        message = await self.database.get_one_starboard_message(guild.id, message.id)
        if message is not None:
            is_tracked = True
        return is_tracked

    async def get_count(self, guild, message):
        """
        get the number of stars on this message as stored in file
        :param guild:
        :param message:
        :return:
        """
        count = 0
        message = await self.database.get_one_starboard_message(guild.id, message.id)
        if message is not None:
            count = message.count
        return count

    async def get_posted_message(self, guild, message):
        """
        Get the message ID and count of the starboard embed or return None
        Also increment the count and save the count
        :param guild: Discord Server
        :param message: Message that was reacted to
        :return:
        """
        message = await self.database.get_one_starboard_message(guild.id, message.id)
        if message is not None:
            count = message.count + 1
            updated_message = await self.database.update_starboard_message(original_message_id=message.original_message_id, count=count)
            if updated_message is not False:
                return updated_message.starboard_message_id, updated_message.count
        return None, None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        guild = reaction.message.guild
        msg = reaction.message
        guid_id = guild.id
        starboard_settings = await self.database.get_starboard_settings(guild.id)
        if starboard_settings is None or starboard_settings.enabled is False:
            return
        ignored_channels = await self.database.get_ignored_starboard_channels(guild.id)
        if msg.channel.id in ignored_channels:
            return
        if not await self.check_roles(user, msg.author, guild):
            return
        react = starboard_settings.emoji
        if react in str(reaction.emoji):
            threshold = starboard_settings.threshold
            count = await self.get_count(guild, msg) + 1 # add one here in case its not posted to starboard
            if await self.check_is_posted(guild, msg): # check if stared message is in starboard
                channel = reaction.message.guild.get_channel(int(starboard_settings.channel_id))
                msg_id, count = await self.get_posted_message(guild, msg) # Count has been incremented
                if msg_id is not None:
                    msg_edit = await channel.fetch_message(id=int(msg_id))
                    await msg_edit.edit(content=f"{reaction.emoji} **#{count}**")
                    return
            else:
                if count < threshold:
                    message = await self.database.get_one_starboard_message(guild.id, msg.id)
                    if message is not None:
                        await self.database.update_starboard_message(msg.id, count=count)
                    else:
                        await self.database.post_starboard_message(guild_id=guild.id,
                                                                   original_message_id=msg.id,
                                                                   starboard_message_id=None,
                                                                   count=count)
                    return

            author = reaction.message.author
            channel = reaction.message.channel
            starboard_channel = self.bot.get_channel(starboard_settings.channel_id)
            em = await self.build_starboard_message(reaction.message, author, channel)
            post_msg = await starboard_channel.send("{} **#{}**".format(reaction.emoji, count),
                                                   embed=em)
            await self.database.post_starboard_message(guild_id=guild.id, original_message_id=msg.id,
                                                       starboard_message_id=post_msg.id, count=count)
        else:
            return

    async def build_starboard_message(self, message: discord.Message, author: discord.Member, channel: discord.TextChannel):
        msg = message.content
        if message.embeds != []:
            embed = message.embeds[0]  # .to_dict()
            # print(embed)
            if hasattr(message, 'timestamp'):
                em = discord.Embed(timestamp=message.timestamp)
            else:
                em = discord.Embed()
            if hasattr(embed, 'title'):
                em.title = embed["title"]
            if hasattr(embed, 'thumbnail'):
                em.set_thumbnail(url=embed["thumbnail"]["url"])
            if hasattr(embed, 'thumbnail'):
                em.description = msg.clean_content + "\n\n" + embed["description"]
            if not hasattr(embed, 'description'):
                em.description = msg.clean_content
            if hasattr(embed, 'url'):
                em.url = embed["url"]
            if hasattr(embed, 'footer'):
                em.set_footer(text=embed["footer"]["text"])
            if hasattr(embed, 'author'):
                postauthor = embed["author"]
                if "icon_url" in postauthor:
                    if author.nick is not None:
                        em.set_author(name=author.nick, icon_url=author.avatar_url)
                    else:
                        em.set_author(name=author.name, icon_url=author.avatar_url)
                else:
                    if author.nick is not None:
                        em.set_author(name=author.nick)
                    else:
                        em.set_author(name=author.name)
            if not hasattr(embed, 'author'):
                if author.nick is not None:
                    em.set_author(name=author.nick, icon_url=author.avatar_url)
                else:
                    em.set_author(name=author.name, icon_url=author.avatar_url)
            if hasattr(embed, 'color'):
                em.color = embed["color"]
            if not hasattr(embed, 'color'):
                em.color = author.top_role.color
            if hasattr(embed, 'image'):
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
            em = discord.Embed(timestamp=message.created_at)
            em.color = author.top_role.color
            em.description = msg
            if author.nick is not None:
                em.set_author(name=author.nick, icon_url=author.avatar_url)
            else:
                em.set_author(name=author.name, icon_url=author.avatar_url)
            if message.attachments != []:
                em.set_image(url=message.attachments[0].url)
        em.add_field(name="jump to Message", value=f"[Click Here]({message.jump_url})")
        em.set_footer(text='{} | {}'.format(channel.guild.name, channel.name))
        return em


    # TODO: Update this with database rewrite
    # @commands.Cog.listener()
    # async def on_reaction_remove(self, reaction, user):
    #     guild = reaction.message.guild
    #     msg = reaction.message
    #     guid_id = str(guild.id)
    #     if guid_id not in self.settings:
    #         return # server not setup
    #     if str(msg.channel.id) in self.settings[guid_id]["ignore"]:
    #         return # ignored channel
    #     react = self.settings[guid_id]["emoji"]
    #     if react not in str(reaction.emoji):
    #         return
    #     threshold = self.settings[guid_id]["threshold"]
    #     has_message = None
    #     for message in self.settings[guid_id]["messages"]:  # find msg stored in list
    #         if reaction.message.id == message["original_message"]:
    #             has_message = message
    #             break
    #     if await self.check_is_posted(guild, msg) and has_message is not None:
    #         starboard_channel = self.bot.get_channel(int(self.settings[guid_id]["channel"]))
    #         starboard_msg_id, count = await self.get_posted_message(guild, msg)
    #         count -= 1 # counter the increment done by self.get_posted_message
    #         if starboard_msg_id is not None and starboard_channel is not None: # msg is in the starboard
    #             msg = await starboard_channel.fetch_message(id=int(starboard_msg_id)) # get message from starboard
    #             count -= 1
    #             if count < threshold: # this should remove the message from starboard but keep it in the file
    #                 has_message = None
    #                 for message in self.settings[guid_id]["messages"]: # find msg stored in list
    #                     if reaction.message.id == message["original_message"]:
    #                         has_message = message
    #                         break
    #                 if has_message is not None:
    #                     self.settings[guid_id]["messages"].remove(has_message)
    #                     message['count'] = count
    #                     message['new_message'] = None
    #                     self.settings[guid_id]["messages"].append(message)
    #                     await self.save_settings()
    #                     await msg.delete()
    #             else:
    #                 await msg.edit(content=f"{reaction.emoji} **#{count}**")
    #                 store = {"original_message": reaction.message.id, "new_message": msg.id, "count": count}
    #                 has_message = None
    #                 for message in self.settings[guid_id]["messages"]:
    #                     if reaction.message.id == message["original_message"]:
    #                         has_message = message
    #                 if has_message is not None:
    #                     self.settings[guid_id]["messages"].remove(has_message)
    #                     self.settings[guid_id]["messages"].append(store)
    #                     await self.save_settings()


def setup(bot):
    bot.add_cog(Star(bot))
