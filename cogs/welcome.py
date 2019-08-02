from discord.ext import commands
import discord
import json
from loguru import logger
from .utils.dataIO import dataIO

class Welcome():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def welcome(self, ctx):
        """
        Sets the channel where welcome messages are sent
        :param ctx:
        :return:
        """
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,
                                        "That's not how you use this command!\n"
                                        "```!welcome enable #channel [custom message | optional]\n"
                                        "!welcome disable```\n"
                                        "Note: Using [user] in your custom message will mention the user")

    @welcome.group(pass_context=True)
    async def enable(self, ctx, channel=None, *, message=":balloon: Hey! Listen! [user] is here! :100:"):
        if channel is None:
            await self.bot.send_message(ctx.message.channel ,"Please specify a channel!\nEx: !welcome enable {0} Hey [user]! welcome to our server!\n\n Note: [user] will mention the user".format(ctx.message.channel.mention))
        try:
            server_id = ctx.message.server.id
            channel_id = channel.replace("#", "").replace("<", "").replace(">", "")
            channel = self.bot.get_channel(channel_id)
            config = dataIO.load_json('data/welcome/info.json')
            config[server_id] = {"channel": channel_id, "message": message}
            dataIO.save_json('data/welcome/info.json', config)
            await self.bot.send_message(ctx.message.channel ,"Welcome channel set!")
        except Exception as e:
            logger.error(e)
            pass

    @welcome.group(pass_context=True)
    async def disable(self, ctx):
        try:
            server_id = ctx.message.server.id
            data = dataIO.load_json('data/welcome/info.json')
            if server_id not in data.keys():
                await self.bot.send_message(ctx.message.channel, "Welcome message was never enabled! You can set it up using !welcome enable #channel")
                return
            data[server_id] = {"channel": "", "message": data[server_id]['message']}
            dataIO.save_json('data/welcome/info.json', data)
            await self.bot.send_message(ctx.message.channel, "Welcome message feature disabled!")
        except Exception as e:
            logger.error(e)
            pass

    async def on_member_join(self, member):
        server_id = member.server.id
        data = dataIO.load_json('data/welcome/info.json')
        if server_id not in data.keys():
            return
        channel = data[server_id]['channel']
        if channel == "":
            return
        message = data[server_id]['message'].replace('[user]', member.mention)
        try:
            await self.bot.send_message(self.bot.get_channel(channel), message)
        except Exception as e:
            await self.bot.send_message(member.server.owner,
                                        "There is an error with a newcomer, please report this to the creator.\n {}".format(
                                            e))


def setup(bot):
    bot.add_cog(Welcome(bot))
