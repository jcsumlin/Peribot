import discord
from discord.ext import commands
import json
from loguru import logger
import glob, os
import time
import re

logger.add(f"file_{str(time.strftime('%Y%m%d-%H%M%S'))}.log", rotation="500 MB")

def load_cogs(folder):
    os.chdir(folder)
    files = []
    for file in glob.glob("*.py"):
        file = re.search('^([A-Za-z1-9]{1,})[^.py]', file).group(0)
        files.append(file)
    return files


def config():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config
bot_config = config()
bot = commands.Bot(command_prefix=bot_config['command-prefix'])

@bot.event
async def on_ready():
    """
    When bot is ready and online it prints that its online
    :return:
    """
    logger.debug("Bot is ready!")

@bot.command(pass_context=True)
async def load(ctx, extension):
    try:
        bot.load_extension('cogs.' + extension)
        logger.debug(f'Loaded {extension}')
        await bot.say(f'Loaded {extension}')
    except Exception as error:
        logger.exception(f"Extension {extension} could not be loaded. [{error}]")

@bot.command(pass_context=True)
async def reload(ctx, extension):
    try:
        bot.unload_extension('cogs.' + extension)
        bot.load_extension('cogs.' + extension)
        logger.debug(f'Reloaded {extension}')
        await bot.say(f'Reloaded {extension}')
    except Exception as error:
        logger.exception(f"Extension {extension} could not be reloaded. [{error}]")

@bot.command()
async def unload(extension):
    try:
        bot.unload_extension('cogs.' + extension)
        logger.debug(f'Unloaded {extension}')
        await bot.say(f'{extension} successfully unloaded')
    except Exception as error:
        logger.exception(f"Extension {extension} could not be unloaded. [{error}]")


if __name__ == "__main__":
    extensions = load_cogs('cogs')
    for extension in extensions:
        try:
            bot.load_extension('cogs.'+extension)
            logger.debug(f'Loaded {extension} cog.')
        except Exception as error:
            logger.exception(f"Extension {extension} could not be loaded. [{error}]")

    bot.run(bot_config['token'])
