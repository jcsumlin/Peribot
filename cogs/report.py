import json
from datetime import datetime

import discord
from discord.ext import commands
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# declaration for User class is in here
from create_databases import Base, Report
from .utils.easyembed import embed


class reeeport:
    """Report system for admins"""

    def __init__(self, bot):
        self.bot = bot
        engine = create_engine('sqlite:///warnings.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()  # session.commit() to store data, and session.rollback() to discard changes

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
    async def report(self, ctx, server_id: int = None, *, message: str):
        """
        For users to report something going wrong.
        :param message: What you want included in the report
        """
        if ctx.message.channel.is_private:
            if server_id is None:
                await self.bot.send_message(ctx.message.author,
                                            embed=embed(
                                                title="No Server ID Specified!",
                                                description="!report [server-id] [message]. You can get the server ID from right clicking on the Server icon and selecting 'Copy ID'"))
            else:
                server_id = str(server_id)
                with open('data/report/info.json', 'r') as f:
                    data = json.load(f)
                    if server_id not in data.keys():
                        logger.debug(f"No channel ID set for reports! {server_id}")
                        await self.bot.say(embed(
                            title="Invalid Server ID!",
                            description="Either this server hasn't specified a channel to recieve reports or that ID you gave me is not a valid server ID"))
                        return
                    channel = data[server_id]
                member = ctx.message.author
                em = discord.Embed(title="Report Case", description=message)
                em.add_field(name="author", value=member)
                em.set_footer(text=f"#{ctx.message.channel}")
                await self.bot.send_message(self.bot.get_channel(id=channel), embed=em)
                # await self.bot.send_message(self.bot.get_channel(id=channel), '@here')
                await self.bot.say(
                    "Your report has been sent, the mods will look in to it as soon as possible.")
                # break

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,
                                        embed=embed(title="Sorry thats not how this command workd!",
                                                    description="ex: !warn add [user id] Stop spamming please"))

    @warn.group(pass_context=True, name="add", aliases=['user'])
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, user_id = None, *, reason = None):
        if user_id is None and reason is None:
            await self.bot.send_message(ctx.message.channel,
                                        embed=embed(title="Sorry thats not how this command workd!",
                                                    description="ex: !warn add [user id] Stop spamming please"))
        elif user_id is not None and reason is None:
            await self.bot.send_message(ctx.message.channel,
                                        embed=embed(title="Sorry thats not how this command workd!",
                                                    description="ex: !warn add [user id] Stop spamming please"))
        elif user_id is not None and reason is not None:
            logger.info(user_id)
            user = await self.bot.get_user_info(user_id)
            logger.info(user.name)
            try:
                new_report = Report(date=datetime.utcnow(), server_id=str(ctx.message.server.id),
                                    user_name=user.name, user_id=str(user_id),
                                    mod_name=str(ctx.message.author.name),
                                    mod_id=str(ctx.message.author.id), reason=reason)
                self.session.add(new_report)
                self.session.commit()
            except:
                await self.bot.send_message(ctx.message.channel,
                                      embed=embed(title="Error adding report to databse"))
            await self.bot.send_message(user,
                                        embed=embed(
                                            title=f"Hey there {user.name} the mods from {ctx.message.server.name} have warned you!",
                                            description=f"Their reason is as follows: {reason}"))
            await self.bot.send_message(ctx.message.channel,
                                        embed=embed(
                                            title="User has been warned in the DM's",
                                            color=discord.Color.green()))

    @warn.group(pass_context=True, name="list")
    async def list(self, ctx):
        reports = self.session.query(Report).filter(Report.server_id == str(ctx.message.server.id)).all()
        users = {}
        logger.info(reports)
        logger.info(len(reports))
        if len(reports) == 0:
            await self.bot.send_message(ctx.message.channel, "There have been no users warned on this server yet.")
        else:
            for report in reports:
                if report.user_name not in users.keys():
                    users[report.user_name] = 1
                else:
                    users[report.user_name] += 1
            embed = discord.Embed(title=f"Warned Users from {ctx.message.server.name}")
            for user, number_of_reports in users.items():
                embed.add_field(name=user, value=str(number_of_reports))
            await self.bot.send_message(ctx.message.channel, embed=embed)



def setup(bot):
    bot.add_cog(reeeport(bot))
