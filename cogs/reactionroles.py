import discord
from discord.ext import commands

from .utils.checks import admin_or_permissions


class ReactionRoleGroup():
    def __init__(self, name, server_id):
        self.name = name
        self.server_id = server_id

    def add_role(self, name, id):
        pass

    def save_to_file(self):
        pass


class ReactionRoles(commands.Cog):
    """Easy to set up reaction roles feature"""

    def __init__(self, bot):
        self.bot = bot

    @reactionroles.group(no_pm=True)
    async def reactionroles(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Error: That's not how you use this command!",
                              description="", color=discord.Color.red())
            e.add_field(name="!cc delete [command]",
                        value="This will completly delete a custom command from this server. I will no lover respond to it.")
            await ctx.send(embed=e)

    @reactionroles.command()
    @admin_or_permissions()
    async def setup(self, ctx):
        exit = False
        timeout = False

        def check(m):
            try:
                m = int(m)
            except ValueError:
                return False
            if m >= 1 and m <= 3:
                return True
            else:
                return False

        embed = discord.Embed(title="Peribot's Reaction Roles Setup Menu",
                              description="Reply with a number to edit settings")
        embed.add_field(name="1) Add Reaction Role Group",
                        value="Create a group of roles that users can react to to quickly assign and un-assign roles from themselves.")
        embed.add_field(name="2) Add a role", value="Add role to an existing role group")
        embed.add_field(name="3) Send a role group",
                        value="Have Peribot send your role group so users can start reacting to them!")
        while not exit or timeout:
            await ctx.send(embed=embed)
            msg = await self.bot.wait_for('message', check=check)
            msg = int(msg)
            await self.process_response(ctx, msg)

    async def process_response(self, ctx, option):
        if option == 1:
            await ctx.send("Please reply with the desired name of your group.")
            msg = await self.bot.wait_for('message')
            pass
        elif option == 2:
            pass
        elif option == 3:
            pass


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
