from random import randint as ri

import discord
from discord.ext import commands
from loguru import logger

from .utils.checks import admin_or_permissions
from .utils.database import Database
from .utils.easyembed import command_error, command_success


class ReactionRoleGroup:
    def __init__(self, name, server_id):
        self.name = name
        self.server_id = server_id

    def add_role(self, role_id):
        pass

    def remove_role(self):
        pass


class ReactionRoles(commands.Cog):
    """Easy to set up reaction roles feature"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reaction = payload.emoji
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
        user = discord.utils.get(guild.members, id=payload.user_id)
        channel = discord.utils.get(guild.channels, id=payload.channel_id)
        message = await channel.fetch_message(id=message_id)

        if not user.bot:
            reaction_role_group = await self.database.get_reaction_role_message(message_id=message_id,
                                                                                role_emoji=str(reaction))
            if reaction_role_group is not None:
                if str(reaction) == reaction_role_group['role'].role_emoji:
                    try:
                        role = discord.utils.get(guild.roles, id=reaction_role_group['role'].role_id)
                    except Exception as e:
                        logger.error(f'Could not get role {e}')
                        await reaction.message.remove_reaction(reaction, user)
                        return await reaction.message.channel.send(embed=command_error('Removing Role From User',
                                                                                       "That role could not be found! Please contact an admin!"))
                    if role not in user.roles:
                        await user.send(f"You don't have the {role.name} role, no action was preformed!")
                        return
                    try:
                        await user.remove_roles(role, reason=f"Reaction Role Group {reaction_role_group['group'].group_name}")
                        await user.send(f"You have successfully removed the {role.name} role!")
                    except discord.errors.Forbidden:
                        await user.send(embed=command_error('Removing Role from User', "Permission Denied! Please make sure that I have 'Manage Roles' turned on!"))
                        await message.remove_reaction(reaction, user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction = payload.emoji
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
        user = discord.utils.get(guild.members, id=payload.user_id)
        channel = discord.utils.get(guild.channels, id=payload.channel_id)
        message = await channel.fetch_message(id=message_id)
        if not user.bot:
            reaction_role_group = await self.database.get_reaction_role_message(message_id=message_id, role_emoji=str(reaction))
            if reaction_role_group is not None:
                if str(reaction) == reaction_role_group['role'].role_emoji:
                    try:
                        role = discord.utils.get(guild.roles, id=reaction_role_group['role'].role_id)
                    except Exception as e:
                        logger.error(f'Could not get role {e}')
                        await reaction.message.remove_reaction(reaction, user)
                        return await reaction.message.channel.send(embed=command_error('Adding Role to User', "That role could not be found! Please contact an admin!"))
                    if role in user.roles:
                        await user.send(f"You already have the {role.name} role, no action was preformed!")
                        return

                    try:
                        await user.add_roles(role, reason=f"Reaction Role Group {reaction_role_group['group'].group_name}")
                        await user.send(f"You have successfully received the {role.name} role!")
                    except discord.errors.Forbidden:
                        await user.send(embed=command_error('Adding Role to User', "Permission Denied! Please make sure that I have 'Manage Roles' turned on!"))
                        await message.remove_reaction(reaction, user)
                pass

    @commands.group(aliases=['rr'])
    async def reactionroles(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Error: That's not how you use this command!",
                              description="You can either use \"reactionroles\" or \"rr\" for base command", color=discord.Color.red())
            e.add_field(name=f"{ctx.prefix}rr group add [name] [description]",
                        value="This will create a new reaction role group that you can add roles to", inline=False)
            e.add_field(name=f"{ctx.prefix}rr role add @[role] :emoji: [group name]]",
                        value="This will add a role to your reaction role group. **EMOJI MUST BE PRESENT ON YOUR SERVER**", inline=False)
            e.add_field(name=f"{ctx.prefix}rr send [group name]]",
                        value="This will send the reaction role group with the appropriate reactions", inline=False)
            await ctx.send(embed=e)

    @reactionroles.group(name="list")
    @admin_or_permissions()
    async def list_reaction_roles(self, ctx):
        groups = await self.database.get_reaction_roles_by_server(ctx.guild.id)
        e = discord.Embed(title=f"{ctx.guild.name}'s Reaction Roles",
                          description=f"Use **{ctx.prefix}rr send [group name]** to activate that group",
                          color=discord.Color.from_rgb(ri(1, 255), ri(1, 255), ri(1, 255)))
        for group in groups:
            roles = ""
            if len(group['roles']) > 0:
                for role in group['roles']:
                    roles += f"@{role.role_name} | {role.role_emoji}\n"
            else:
                roles += f"None\nYou can add roles with **{ctx.prefix}rr role add @[role] [reaction] [group_name]**"
            e.add_field(name=f"**Name**: {group['name']}, \n"
                             f"**Description**: {group['description'] if group['description'] != '' else 'None'}\n"
                             f"**Message**: {group['message'].message_id if group['message'] else 'None'}",
                        value=f"Roles:\n"
                              f"{roles}",
                        inline=False)
        await ctx.send(embed=e)

    @reactionroles.group()
    @admin_or_permissions()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Error: That's not how you use this command!",
                              description="", color=discord.Color.red())
            e.add_field(name="!cc delete [command]",
                        value="This will completly delete a custom command from this server. I will no lover respond to it.")
            await ctx.send(embed=e)

    @role.command(name='add')
    async def _add(self, ctx, role: discord.Role, reaction, group_name: str):
        rr = await self.database.post_reaction_role(role.id,
                                               str(reaction),
                                               role.name,
                                               group_name,
                                               ctx.guild.id)
        msg = await ctx.send(embed=command_success(f"\"{role.name}\" added to {group_name}!", f"Use **{ctx.prefix}reactionroles send [group-name]**"))
        await msg.add_reaction(reaction)

    @reactionroles.group()
    @admin_or_permissions()
    async def group(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Error: That's not how you use this command!",
                              description="", color=discord.Color.red())
            e.add_field(name="!cc delete [command]",
                        value="This will completly delete a custom command from this server. I will no lover respond to it.")
            await ctx.send(embed=e)

    @group.command(name="delete")
    @admin_or_permissions()
    async def _delete(self, ctx, group):
        pass

    @group.command()
    async def add(self, ctx, name=None, *, description=None):
        if name is None and description is None:
            await ctx.send(embed=command_error("Missing parameters when creating reaction role group",
                                               "A group must include a name and an optional description"
                                               f"\nex: **{ctx.prefix}reactionroles group add [name] [description]**"))
        group = await self.database.add_reaction_role_group(server_id=ctx.guild.id,
                                                            group_name=name,
                                                            group_description=description)
        await ctx.send(embed=command_success("Reaction role group successfully created!", f"{group.group_name}: {group.group_description}"))

    @reactionroles.group()
    @admin_or_permissions()
    async def send(self,ctx, group_name=None):
        await self.database.check_for_reaction_role_messages(group_name=group_name, server_id=ctx.guild.id)
        group = await self.database.get_reaction_role_by_group(group_name=group_name, server_id=ctx.guild.id)
        desc = ""
        for role in group['roles']:
            desc += f"**{role.role_name}** : {role.role_emoji}\n"
        e = discord.Embed(title="React to get your roles!", description=desc, color=discord.Color.from_rgb(ri(1, 255), ri(1, 255), ri(1, 255)))
        msg = await ctx.send(embed=e)
        for role in group['roles']:
            await msg.add_reaction(role.role_emoji)
        await self.database.post_reaciton_role_message(group_id=group['group'].id, message_id=msg.id)

    # @reactionroles.command()
    # @admin_or_permissions()
    # async def setup(self, ctx):
    #     exit = False
    #     timeout = False
    #
    #     def check(m):
    #         try:
    #             m = int(m.content)
    #         except ValueError:
    #             return False
    #         if m >= 1 and m <= 3:
    #             return m
    #         else:
    #             return False
    #
    #     embed = discord.Embed(title="Peribot's Reaction Roles Setup Menu",
    #                           description="Reply with a number to edit settings")
    #     embed.add_field(name="1) Add Reaction Role Group",
    #                     value="Create a group of roles that users can react to to quickly assign and un-assign roles from themselves.",
    #                     inline=False)
    #     embed.add_field(name="2) Add a role",
    #                     value="Add role to an existing role group",
    #                     inline=False)
    #     embed.add_field(name="3) Send a role group",
    #                     value="Have Peribot send your role group so users can start reacting to them!",
    #                     inline=False)
    #     while not exit or timeout:
    #         await ctx.send(embed=embed)
    #         msg = await self.bot.wait_for('message', check=check)
    #         if not msg:
    #             return False
    #         await self.process_response(ctx, int(msg.content))
    #
    #
    # async def process_response(self, ctx, option):
    #     if option == 1:
    #         await ctx.send("Please reply with the desired name of your group.")
    #         msg = await self.bot.wait_for('message')
    #         pass
    #     elif option == 2:
    #         pass
    #     elif option == 3:
    #         pass


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
