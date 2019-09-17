from discord.ext import commands
from loguru import logger

from .utils.dataIO import dataIO


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def welcome(self, ctx):
        """
        Sets the channel where welcome messages are sent
        :param ctx:
        :return:
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("That's not how you use this command!\n```!welcome enable #channel [custom message | optional]\n!welcome disable```\nNote: Using [user] in your custom message will mention the user")

    @welcome.group()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, channel=None, *, message=":balloon: Hey! Listen! [user] is here! :100:"):
        if channel is None:
            await ctx.send("Please specify a channel!\nEx: !welcome enable {0} Hey [user]! welcome to our guild!\n\n Note: [user] will mention the user".format(ctx.channel.mention))
        try:
            guild_id = str(ctx.guild.id)
            channel_id = channel.replace("#", "").replace("<", "").replace(">", "")
            config = dataIO.load_json('data/welcome/info.json')
            config[guild_id] = {"channel": channel_id, "message": message}
            dataIO.save_json('data/welcome/info.json', config)
            await ctx.send("Welcome channel set!")
        except Exception as e:
            logger.error(e)
            pass

    @welcome.group()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        try:
            guild_id = ctx.guild.id
            data = dataIO.load_json('data/welcome/info.json')
            if guild_id not in data.keys():
                await ctx.channel.send("Welcome message was never enabled! You can set it up using !welcome enable #channel")
                return
            data[guild_id] = {"channel": "", "message": data[guild_id]['message']}
            dataIO.save_json('data/welcome/info.json', data)
            await ctx.channel.send("Welcome message feature disabled!")
        except Exception as e:
            logger.error(e)
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        data = dataIO.load_json('data/welcome/info.json')
        if guild_id not in data.keys():
            return
        channel = data[guild_id]['channel']
        if channel == "":
            return
        message = data[guild_id]['message'].replace('[user]', member.mention)
        try:
            send_to_channel = self.bot.get_channel(int(channel))
            if send_to_channel is not None:
                await send_to_channel.send(message)
        except Exception as e:
            await member.guild.owner.send("There is an error with a newcomer, please report this to the creator.\n {}".format(e))


def setup(bot):
    bot.add_cog(Welcome(bot))
