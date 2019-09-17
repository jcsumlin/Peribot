import asyncio
import os
import random

import discord
from discord.ext import commands

from cogs.utils.dataIO import dataIO
from .utils import checks


class Giveaways(commands.Cog):
    """Giveaways."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/giveaways/settings.json")
        self.started = False

    @commands.group()
    async def giveaway(self, ctx):
        """Start or stop giveaways."""
        if not ctx.invoked_subcommand:
            await self.bot.send_cmd_help(ctx)

    @giveaway.command()
    @checks.mod_or_higher()
    async def start(self, ctx, *, settings):
        """Start a giveaway.
        Usage"
        [p]giveaway start name: <Giveaway  name>; length: <Time length>; entries: [Max entries]
        Giveaway name is mandatory.
        Length is mandatory.
        Max entries is optional.

        Example:
        [p]giveaway start name: Minecraft account; entries: 99; length: 3 days
        [p]giveaway start name: Minecraft account; length: 2 hours; entries: 42
        [p]giveaway start name: Minecraft account; length: 5 days"""
        settings = settings.split("; ")
        setdict = False
        guild = ctx.message.guild
        if guild.id not in self.settings:
            self.settings[guild.id] = {}
        # Setting all of the settings.
        for setting in settings:
            if not setdict:
                settings = {"name": "", "length": -1, 'entries': 0, "users": [], "started": True}
                setdict = True
            if setting.startswith("name: "):
                if setting[6:] in self.settings[ctx.message.guild.id]:
                    await ctx.send("There's already a giveaway running with this name.")
                    return
                else:
                    settings['name'] = setting[6:]
            elif setting.startswith("length: "):
                length = setting[7:]
                lengths = {'hour': 3600, 'day': 86400}
                if "days" in length.split() or "day" in length.split():
                    try:
                        settings['length'] = int(length.split()[0]) * lengths['day']
                    except:
                        await ctx.send("The 'length' parameter, {}, does not start with an integer.".format(length))
                        return
                elif "hour" in length.split() or "hours" in length.split():
                    try:
                        settings['length'] = int(length.split()[0]) * lengths['hour']
                    except:
                        await ctx.send("The 'length' parameter, {}, does not start with an integer.".format(length))
                        return
                else:
                    await ctx.send("You can only use hours and days.")
                    return
                # Checking if mandatory settings are there.
        if settings['name'] == "":
            await ctx.send("The 'name' parameter cannot be empty.")
            return
        if settings['length'] == -1:
            await ctx.send("The 'length' parameter cannot be empty.")
            return
        embed = discord.Embed(title=":tada: New Giveaway Started! :tada:",
                              description="React to this message to enter!", color=discord.Color.green())
        embed.add_field(name=f"Prize:", value=f"{settings['name']}")
        embed.add_field(name=f"Length:", value=f"{int(settings['length']) / 3600} Hours")
        embed.add_field(name=f"Sponsored by:", value=f"{ctx.message.author}")
        message = await ctx.send(embed=embed)
        self.settings[guild.id][str(message.id)] = settings
        self.save_settings()
        await self.bot.add_reaction(message, "✅")
        await self.bot.delete_message(ctx.message)

    @giveaway.command()
    @checks.mod_or_higher()
    async def stop(self, ctx, message_id):
        """Stops a giveaway early so you can pick a winner.
        Example:
        [p]giveaway stop 620715054211268637"""
        guild = ctx.message.guild
        if guild.id not in self.settings:
            await ctx.send("There are no giveaways in this server.")
        elif message_id not in self.settings[guild.id]:
            await ctx.send(
                "That's not a valid giveaway, to see all giveaways you can do {}giveaway list".format(ctx.prefix))
        elif not self.settings[guild.id][message_id]['started']:
            await ctx.send("That giveaway's already stopped.")
        else:
            self.settings[guild.id][message_id]['started'] = False
            self.save_settings()
            await ctx.send(
                "You can now pick a winner with {}giveaway pick <amount> <message_id>".format(ctx.prefix))

    @giveaway.command()
    @checks.mod_or_higher()
    async def pick(self, ctx, amount: int, giveaway_id):
        """Picks <amount> of winners for the giveaway, which usually should be 1.
        Example:
        [p]giveaway pick 5 Minecraft account (This will pick 5 winners from all the people who entered the Minecraft account giveaway)"""
        guild = ctx.message.guild
        if guild.id not in self.settings:
            return await ctx.send("This server does not have any giveaways yet.")
        giveaways = self.settings[guild.id]
        if giveaway_id not in giveaways:
            return await ctx.send(
                "Sorry thats not a valid message ID!\n```\nHINT: The message ID will be found on the bot's message announcing the giveaway\n```")
        giveaway = giveaways[giveaway_id]
        if giveaways[giveaway_id]['started'] == True:
            return await ctx.send(
                "This giveaway has not ended yet! Please end it with `!giveaway stop <message_id>`")
        if len(giveaways[giveaway_id]['users']) == 0:
            del self.settings[guild.id][giveaway_id]
            self.save_settings()
            return await ctx.send("This giveaway has no entries! I guess that means no one wins :(")
        status = await ctx.send("Picking winners.")
        winnersIDs = []
        winners = []
        for i in range(amount):
            winnersIDs.append(random.choice(giveaway['users']))
        for winner in winnersIDs:
            winner = discord.utils.get(guild.members, id=winner)
            while winner == None:
                winner = discord.utils.get(guild.members,
                                           id=random.choice(giveaway['users']))
            winners.append(winner.mention)
        del self.settings[guild.id][giveaway_id]
        self.save_settings()
        if amount == 1:
            await self.bot.edit_message(status,
                                        "And thats a wrap! The winner is: {}! Congratulations, you won {}!".format(
                                            " ".join(winners),
                                            giveaway['name']))
        else:
            await self.bot.edit_message(status,
                                        "And thats a wrap! The winners are: {}! Congratulations, you won {}!".format(
                                            " ".join(winners),
                                            giveaway['name']))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Enter a giveaway.
        Example:
        [p]giveaway enter Minecraft account."""
        guild = reaction.message.guild
        author_id = user.id
        message_id = reaction.message.id
        if author_id == 608824312689983488 or author_id == 484461035315527700:
            return
        if message_id in self.settings[guild.id]:
            giveaway = self.settings[guild.id][message_id]
            if author_id not in self.settings[guild.id][message_id]['users']:
                self.settings[guild.id][message_id]['users'].append(author_id)
                self.settings[guild.id][message_id]['entries'] =+ 1
                self.save_settings()
                return await self.bot.send_message(user,
                                                   "You have successfully entered the {} giveaway, good luck!".format(
                                                       giveaway['name']))

    @giveaway.command()
    async def list(self, ctx):
        """Lists all giveaways running in this guild."""
        guild = ctx.message.guild
        if guild.id not in self.settings or self.settings[guild.id] == {}:
            await ctx.send("This server has no giveaways running.")
        else:
            await ctx.send("This server has the following giveaways running:\n\t{}".format(
                "\n\t".join(list(self.settings[guild.id].keys()))))

    @giveaway.command()
    async def info(self, ctx, giveaway):
        """Get information for a giveaway.
        Example:
        [p]giveaway info Minecraft account"""
        guild = ctx.message.guild
        if guild.id not in self.settings:
            await ctx.send("This server has no giveaways running.")
        elif giveaway not in self.settings[guild.id]:
            await ctx.send("That's not a valid giveaway running in this server.")
        else:
            settings = self.settings[guild.id][giveaway]
            await ctx.send("Name: **{}**\nTime left: **{}**\nEntries: **{}**".format(settings['name'],
                                                                                         self.secondsToText(
                                                                                             settings['length']),
                                                                                         len(settings['users'])))

    def save_settings(self):
        return dataIO.save_json("data/giveaways/settings.json", self.settings)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.started:
            self.started = True
            print("Giveaways loop started.")
            while True:
                if self.bot.get_cog("Giveaways") != None:
                    await asyncio.sleep(1)
                    self.settings = dataIO.load_json("data/giveaways/settings.json")
                    for guild in self.settings:
                        for giveaway in self.settings[guild]:
                            if self.settings[guild][giveaway]['started']:
                                self.settings[guild][giveaway]['length'] -= 1
                                if self.settings[guild][giveaway]['length'] == 0:
                                    self.settings[guild][giveaway]['started'] = False
                    self.save_settings()
                else:
                    print("Giveaways loop stopped, cog not loaded anymore.")
                    break

    def secondsToText(self, secs):
        days = secs // 86400
        hours = (secs - days * 86400) // 3600
        minutes = (secs - days * 86400 - hours * 3600) // 60
        seconds = secs - days * 86400 - hours * 3600 - minutes * 60
        result = ("{0} day{1}, ".format(days, "s" if days != 1 else "") if days else "") + \
                 ("{0} hour{1}, ".format(hours, "s" if hours != 1 else "") if hours else "") + \
                 ("{0} minute{1}, ".format(minutes, "s" if minutes != 1 else "") if minutes else "") + \
                 ("{0} second{1}".format(seconds, "s" if seconds != 1 else "") if seconds else "")
        return result


def check_folders():
    if not os.path.exists("data/giveaways"):
        print("Creating data/giveaways folder...")
        os.makedirs("data/giveaways")


def check_files():
    if not os.path.exists("data/giveaways/settings.json"):
        print("Creating data/giveaways/settings.json file...")
        dataIO.save_json("data/giveaways/settings.json", {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Giveaways(bot))
