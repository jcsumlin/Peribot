from discord.ext import commands
from loguru import logger


#
# This is a modified version of checks.py, originally made by Rapptz
#
#                 https://github.com/Rapptz
#          https://github.com/Rapptz/RoboDanny/tree/async
#

def is_bot_owner_check(ctx):
    _id = ctx.author.id
    onwer_id = 204792579881959424
    logger.info(_id == onwer_id or _id in onwer_id)
    return _id == onwer_id

def is_owner():
    return commands.has_role('administrator')

# The permission system of the bot is based on a "just works" basis
# You have permissions and the bot has permissions. If you meet the permissions
# required to execute the command (and the bot does as well) then it goes through
# and you can execute the command.
# If these checks fail, then there are two fallbacks.
# A role with the name of Bot Mod and a role with the name of Bot Admin.
# Having these roles provides you access to certain commands without actually having
# the permissions required for them.
# Of course, the owner will always be able to execute commands.


def admin_or_permissions():
    return commands.has_permissions(administrator=True)


def admin():
    return admin_or_permissions()


def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

