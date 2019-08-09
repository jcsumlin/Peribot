import asyncio
import os
from datetime import datetime

import discord
from discord.ext import commands
from loguru import logger

from .utils.dataIO import dataIO, fileIO


class Birthdays:
    def __init__(self, bot):
        self.bot = bot

    async def get_config(self):
        return dataIO.load_json('data/birthday/birthdays.json')

    async def save_config(self, data):
        return dataIO.save_json('data/birthday/birthdays.json', data)

    @commands.group(pass_context=True)
    async def birthday(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @birthday.group(pass_context=True)
    async def add(self, ctx, user: discord.User, birthday):
        birthday = birthday.split('/')
        birthdays = await self.get_config()
        logger.info(birthday)
        logger.info(birthdays)
        logger.info(str(ctx.message.server.id) in birthdays.keys())
        if str(ctx.message.server.id) in birthdays.keys():
            logger.info(birthday)
            birthday = datetime(year=int(birthday[2]), month=int(birthday[0]), day=int(birthday[1]))
            logger.info(birthday)
            birthdays[ctx.message.server.id]['users'].append({'user_id': user.id, 'birthday': str(birthday), 'COMPLETE': False})
            await self.save_config(birthdays)
            await self.bot.send_message(ctx.message.channel,"Done!")
        else:
            await self.bot.send_message(ctx.message.channel,"Birthdays not setup!")



    @birthday.group(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel):
        birthdays = await self.get_config()
        channel_id = channel.replace("#", "").replace("<", "").replace(">", "")
        if ctx.message.server.id not in birthdays.keys():
            birthdays[ctx.message.server.id] = {'channel': channel_id, 'users': []}
        else:
            birthdays[ctx.message.server.id]['channel'] = channel_id

        await self.save_config(birthdays)
        return await self.bot.send_message(ctx.message.channel, "Birthday Channel Set! :birthday:")

    @birthday.group(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        birthdays = await self.get_config()
        if ctx.message.server.id in birthdays.keys():
            birthdays[ctx.message.server.id]['channel'] = ""
            await self.save_config(birthdays)
            return await self.bot.send_message(ctx.message.channel, ":x: Birthday Messages Disabled!")
        else:
            return await self.bot.send_message(ctx.message.channel, ":interrobang: Birthday Message Channel Not Set For This Server!")

    async def check_birthdays(self):
        while self is self.bot.get_cog("Birthdays"):
            birthdays = await self.get_config()
            for key, value in birthdays.items():
                for user in value['users']:
                    birthday = datetime.strptime(user['birthday'], "%Y-%m-%d 00:00:00")
                    now = datetime.now()
                    if birthday.month != now.month or birthday.day != now.day and user['COMPLETE']:
                        user['COMPLETE'] = False
                        await self.save_config(birthdays)
                    if birthday.month == now.month and birthday.day == now.day and not user['COMPLETE']:
                        channel = self.bot.get_channel(value['channel'])
                        if channel is None:
                            continue
                        years = now.year - birthday.year
                        if 4 <= years <= 20 or 24 <= years <= 30:
                            suffix = "th"
                        else:
                            suffix = ["st", "nd", "rd"][years % 10 - 1]
                        await self.bot.send_message(channel, f"Hey  <@{user['user_id']}>! I just wanted to wish you the happiest of brthdays on your {years}{suffix} birthday! :birthday: :heart:")
                        user['COMPLETE'] = True
                        await self.save_config(birthdays)
                await asyncio.sleep(1)


def check_folders():
    if not os.path.exists("data/birthday"):
        logger.info("Creating data/birthday folder...")
        os.makedirs("data/birthday")


def check_files():
    f = "data/birthday/birthdays.json"
    if not fileIO(f, "check"):
        logger.info("Creating empty birthdays.json...")
        fileIO(f, "save", {})


def setup(bot):
    check_folders()
    check_files()
    n = Birthdays(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_birthdays())
    bot.add_cog(n)
