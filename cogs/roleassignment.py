import discord
from discord.ext import commands
import json
from loguru import logger


class announcements:
    """
    Assign/Design announcement role from user
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def setrole(self, ctx, role: discord.Role):
        try:
            channel = ctx.message.channel.id
            server_id = ctx.message.server.id
            with open('data/roleassignment/info.json', 'r+') as f:
                data = json.load(f)
                data[server_id] = str(role)  # <--- add `id` value.
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
            await self.bot.send_message(self.bot.get_channel(channel) ,"Announcement Role Set!")
        except Exception as e:
            logger.error(e)
            pass

    @commands.command(pass_context=True)
    async def optin(self, ctx):
        member = ctx.message.author
        server = ctx.message.server
        optin_role = self.get_server_role(server.id)
        role_exists = optin_role in [x.name for x in member.roles]
        if role_exists:
            await self.bot.send_message(ctx.message.channel, "You are already opted in to our announcements! :mega: (use !optout to opt out)")
        else:
            role = discord.utils.get(server.roles, name=optin_role)
            await self.bot.add_roles(member, role)
            await self.bot.send_message(ctx.message.channel, "You have opted in to our announcements! :mega: (use !optout to opt out)")


    @commands.command(pass_context=True)
    async def optout(self, ctx):
        member = ctx.message.author
        server = ctx.message.server
        optin_role = self.get_server_role(server.id)
        role_exists = optin_role in [x.name for x in member.roles]
        if role_exists:
            role = discord.utils.get(server.roles, name=optin_role)
            await self.bot.remove_roles(member, role)
            await self.bot.send_message(ctx.message.channel,
                                        "You have opted out to our announcements! :mute: (use !optin to opt back in)")
        else:
            await self.bot.send_message(ctx.message.channel, "You not currently opted in to our announcements! :mega: (use !optin to opt back in)")



    def get_server_role(self, server_id):
        with open('data/roleassignment/info.json', 'r') as f:
            data = json.load(f)
            if server_id not in data.keys():
                logger.debug(f"No channel ID set for reports! {server_id}")
                return
            role = data[server_id]
            return role


def setup(bot):
    bot.add_cog(announcements(bot))
