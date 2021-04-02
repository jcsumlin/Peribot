import glob
import json
import os
import re
import time
from configparser import *
from datetime import datetime

from discord.ext import commands, timers
from loguru import logger

from cogs.utils.checks import is_bot_owner_check
from cogs.utils.database import Database

#initiate logger test
logger.add(f"file_{str(time.strftime('%Y%m%d-%H%M%S'))}.log", rotation="500 MB")
database = Database()


def load_cogs(folder):
    os.chdir(folder)
    files = []
    for file in glob.glob("*.py"):
        file = re.search('^([A-Za-z1-9]{1,})(?:.py)$', file).group(1)
        files.append(file)
    return files


def config():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or('!')(bot, message)
    settings = await database.get_server_settings(message.guild.id)
    if settings:
        prefix = settings.prefix
        return commands.when_mentioned_or(str(prefix))(bot, message)
    else:
        return commands.when_mentioned_or("!")(bot, message)

bot = commands.Bot(command_prefix=get_prefix)

@bot.event
async def on_ready():
    """
    When bot is ready and online it prints that its online
    :return:
    """
    bot.timer_manager = timers.TimerManager(bot)
    logger.debug("Bot is ready!")


@bot.command()
@is_bot_owner_check()
async def load(ctx, extension):
    try:
        bot.load_extension('cogs.' + extension)
        logger.debug(f'Loaded {extension}')
        await ctx.send(f'Loaded {extension}')
    except Exception as error:
        logger.exception(f"Extension {extension} could not be loaded. [{error}]")


@bot.command()
@is_bot_owner_check()
async def reload(ctx, extension):
    try:
        bot.unload_extension('cogs.' + extension)
        bot.load_extension('cogs.' + extension)
        logger.debug(f'Reloaded {extension}')
        await ctx.send(f'Reloaded {extension}')
    except Exception as error:
        logger.exception(f"Extension {extension} could not be reloaded. [{error}]")


@bot.command()
@is_bot_owner_check()
async def unload(ctx, extension):
    try:
        bot.unload_extension('cogs.' + extension)
        logger.debug(f'Unloaded {extension}')
        await ctx.send(f'{extension} successfully unloaded')
    except Exception as error:
        logger.exception(f"Extension {extension} could not be unloaded. [{error}]")


if __name__ == "__main__":
    if "DISCORD_TOKEN" not in os.environ:
        logger.error("No discord token set. Exiting.")
        exit(1)
    else:
        token = os.environ.get('DISCORD_TOKEN')
    bot.start_time = datetime.now()
    bot.remove_command('help')
    extensions = load_cogs('cogs')
    for extension in extensions:
        try:
            bot.load_extension('cogs.'+extension)
            logger.debug(f'Loaded {extension} cog.')
        except Exception as error:
            logger.exception(f"Extension {extension} could not be loaded. [{error}]")

    bot.run(token)
