import json

import discord
from discord.ext import commands
from loguru import logger

from .utils.easyembed import embed


class reeeport:
    """Report system for admins"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def setreport(self, ctx):
        """
        Sets the channel that reports come into.
        """
        try:
            channel = ctx.message.channel.id
            server_id = ctx.message.server.id
            with open('data/report/info.json', 'r+') as f:
                data = json.load(f)
                data[server_id] = str(channel)  # <--- add `id` value.
                f.seek(0)  # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # remove remaining part
            await self.bot.send_message(self.bot.get_channel(channel) ,"Report channel set! Any user reports will alert users here.")
        except Exception as e:
            logger.error(e)
            pass


    @commands.command(pass_context=True)
    async def report(self, ctx, *, message: str):
        """
        For users to report something going wrong.
        :param message: What you want included in the report
        """
        server = ctx.message.server
        with open('data/report/info.json', 'r') as f:
            data = json.load(f)
            if server.id not in data.keys():
                logger.debug(f"No channel ID set for reports! {server.id}")
                return
            channel = data[server.id]
        member = ctx.message.author

        em = discord.Embed(title="Report Case", description=message)
        em.add_field(name="author", value=member)
        em.set_footer(text=f"#{ctx.message.channel}")
        await self.bot.send_message(self.bot.get_channel(id=channel), embed=em)
        # await self.bot.send_message(self.bot.get_channel(id=channel), '@here')
        await self.bot.say(
            "Your report has been sent, the mods will look in to it as soon as possible.")
        # break

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.User = None, reason = None):
        if user is None and reason is None:
            await self.bot.send_message(ctx.message.channel, embed(title="Sorry thats not how this command workd!", description="ex: !warn @user Stop spamming please"))
        elif user is not None and reason is None:
            await self.bot.send_message(ctx.message.channel, embed(title="Sorry thats not how this command workd!", description="ex: !warn @user Stop spamming please"))
        elif user is not None and reason is not None:
            await self.bot.send_message(user,
                                        embed(title=f"Hey there {user.name} the mods from {ctx.message.server.name} have warned you!",
                                              description=f"Their reason is as follows: {reason}"))

def setup(bot):
    bot.add_cog(reeeport(bot))
