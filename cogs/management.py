import discord
from discord.ext import commands
from loguru import logger
import git



class Management(object):

    """
    Set of commands for Administration.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setcolor', pass_context=True)
    async def set_member_color(self, ctx, color: discord.Color):

        """
        Color the nickname of the participant. * Let there be bright colors and colors! *
        [!] In development.
        Arguments:
        color in HEX

        For example:
        !setcolor #FF0000
        """
        member = ctx.message.author

        role_exists = f'PeriColored - {member.name}' in [x.name for x in member.roles]
        logger.debug("Role exists?: " + str(role_exists))
        server = ctx.message.server
        try:
            if role_exists:
                role = discord.utils.get(server.roles, name=f'PeriColored - {member.name}')
                await self.bot.edit_role(server,role ,color=color)
                await self.bot.send_message(ctx.message.channel,
                                            '%s, Your color role was successfully changed (new color: %s).' % (
                member.mention, color))
            else:
                role = await self.bot.create_role(server=server, name=f'PeriColored - {member.name}',
                                                   color=color)
                await self.bot.move_role(server, role, int(member.top_role.position)+1)
                await self.bot.add_roles(member, role)
                await self.bot.send_message(ctx.message.channel,
                    '%s, You have successfully added a role with color %s' % (member.mention, color))
        except discord.errors.HTTPException as e:
            await self.bot.send_message(ctx.message.channel,
                f':x: Failed. \nYou may have entered the color incorrectly? \nCheck in case %s {e}' % color)

    @commands.command(name='gitpull', pass_context=True)
    async def git_pull(self, ctx):
        git_dir = "./"
        try:
            g = git.cmd.Git(git_dir)
            g.pull()
            embed = discord.Embed(title="Successfully pulled from repository", color=0x00df00)
            await self.bot.send_message(ctx.message.channel, embed=embed)
        except Exception as e:
            errno, strerror = e.args
            embed = discord.Embed(title="Command Error!",
                                  description=f"Git Pull Error: {errno} - {strerror}",
                                  color=0xff0007)
            await self.bot.send_message(ctx.message.channel, embed=embed)


    @commands.command(name='pin', pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def pin_message(self, ctx, *, message):
        """Copy your message in a stylish and modern frame, and then fix it!
        Arguments:
        `: message` - message
        __ __
        For example:
        ```
        !pin This text was written by the ancient Elves in the name of Discord!
        ```
        """
        embed = discord.Embed(color=0x71f442,
                              title='Pin it up!',
                              description=message)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        msg = await self.bot.say(embed=embed)
        await self.bot.pin_message(msg)
#
#     @commands.command(name='resetmute', pass_context=True)
#     @commands.has_permissions(manage_roles=True)
#     async def resetmute(self, ctx):
#         """Reset the settings of` !mute` and remove the role of PeriMute. * When peace times have arrived, without flooding! *
#         """
#
#         mute = discord.utils.get(ctx.guild.roles, name='PeriMute')
#         if not mute:
#             return await ctx.send('User isn\'t muted.')
#
#         try:
#             await mute.delete()
#
#         except discord.errors.Forbidden:
#             await ctx.message.add_reaction('❌')
#
#         else:
#             await ctx.message.add_reaction('✅')
#
# #     @commands.command(name='mute')
# #     @commands.has_permissions(manage_roles=True)
# #     async def mute(self, ctx, member: discord.Member, *, reason: str = 'отсутствует'):
# #         """Mute the member. * He will not be able to send messages, cool! *
# #         Arguments:
# #         `: member` - member
# #         `: reason` - reason
# #         __ __
# #         For example:
# #         ```
# #         !mute @Username#1234 Spam
# #         !mute @Username
# #         ```
# #         For the team to work correctly, I need to make some edits to the text channels and roles on this server.
# #         [!?] What changes will be made?
# #         > PeriMute role will be created;
# #         > The PeriMute role will be added to the access settings of all text feeds;
# #         > All roles (except @everyone) will have the "send_messages" right (sending messages) removed; ```
# #         """
# #         mute = discord.utils.get(ctx.guild.roles, name='NaomiMute')
# #
# #         if not mute:
# #             try:
# #                 def message_check(m):
# #                     return m.author.id == ctx.author.id
# #
# #                 failed_channels = []
# #                 failed_roles = []
# #
# #                 await ctx.send(
# #                     f'The command {ctx.prefix} {ctx.command} was used for the first time on this server. \nCan I make changes to the channel and role settings for this command to work correctly? (Yes/No)',
# #                     delete_after=120.0)
# #                 msg = await self.bot.wait_for('message', check=message_check, timeout=120.0)
# #
# #                 if msg.content.lower() in ['yes', 'aha', 'yep']:
# #                     counter_msg = await ctx.send(
# #                         'Ok, I’m working ... \nModification of channels: pending. \nModification of roles: pending.')
# #
# #                     mute = await ctx.guild.create_role(name='PeriMute',
# #                                                        reason='The !mute command was used, but the "PeriMute" role was missing.')
# #
# #                     modified_channels = 0
# #                     modified_roles = 0
# #                     for tchannel in ctx.guild.text_channels:
# #                         try:
# #                             await tchannel.set_permissions(mute,
# #                                                            send_messages=False,
# #                                                            add_reactions=False)
# #
# #                         except:
# #                             failed_channels.append(f'`{tchannel.name}`')
# #
# #                         else:
# #                             modified_channels += 1
# #                             try:
# #                                 await counter_msg.edit(
# #                                     content=f'Хорошо, выполняю... \nМодификация каналов: {modified_channels}/{len(ctx.guild.text_channels)}\nМодификация ролей: в ожидании.')
# #                             except:
# #                                 pass
# #
# #                     # mute_perms = discord.Permissions()
# #                     # mute_perms.update(send_messages=False)
# #                     # К черту discord.Permissions()
# #
# #                     mute_perms = discord.PermissionOverwrite()
# #                     mute_perms.send_messages = False
# #                     mute_perms.add_reactions = False
# #
# #                     for role in ctx.guild.roles:
# #                         if role != ctx.guild.default_role:
# #                             try:
# #                                 await role.edit(permissions=mute_perms)
# #                             except:
# #                                 failed_roles.append(f'`{role.name}`')
# #                             else:
# #                                 modified_roles += 1
# #                             await counter_msg.edit(
# #                                 content=f'Хорошо, выполняю... \nМодификация каналов: {modified_roles}/{len(ctx.guild.text_channels)}.\nМодификация ролей: {x1}/{len(ctx.guild.roles) - 1}')
# #                 else:
# #                     return await ctx.send(':x: Отменено.')
# #             except asyncio.TimeoutError:
# #                 await ctx.send(
# #                     'Я не столь терпелива, чтобы ждать ответа так долго...\nПросто повторно введите команду.')
# #         try:
# #             if not len(failed_channels) == 0 or not len(failed_roles) == 0:
# #                 await ctx.send(
# #                     f'Модификация завершена не полностью:\n- Каналы: {", ".join(failed_channels)}\n- Роли: {", ".join(failed_roles)}')
# #         except:
# #             pass
# #
# #         await member.add_roles(mute, reason='Был приглушен через n!mute.')
# #
# #         embed = discord.Embed(timestamp=ctx.message.created_at, color=0x35FF81,
# #                               description=f'Участник {member.mention} приглушен.\nПричина: {reason}')
# #         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
# #         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
# #
# #         await ctx.send(embed=embed)
#
#     # @commands.command(name='unmute')
#     # @commands.has_permissions(manage_roles=True)
#     # async def unmute(self, ctx, member: discord.Member, *, reason: str = 'отсутствует'):
#     #     """Снять приглушение с участника. *Да будет свобода чата!*
#     #     Аргументы:
#     #     `:member` - участник
#     #     `:reason` - причина
#     #     __                                            __
#     #     Например:
#     #     ```
#     #     n!unmute @Username#1234
#     #     n!unmute Username Просто так
#     #     ```
#     #     """
#     #
#     #     mute = discord.utils.get(ctx.guild.roles, name='NaomiMute')
#     #
#     #     if not mute:
#     #         embed = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000,
#     #                               description='Не найдена роль "NaomiMute", а раз ее нет, то и снимать мут мне не с кого...')
#     #         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#     #         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#     #
#     #     elif mute not in member.roles:
#     #         embed = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000,
#     #                               description=f'{member.mention} не приглушен!')
#     #         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#     #         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#     #
#     #     else:
#     #         await member.remove_roles(mute, reason='Приглушение снято - n!unmute.')
#     #
#     #         embed = discord.Embed(timestamp=ctx.message.created_at, color=0x35FF81,
#     #                               description=f'Снято приглушение с участника {member.mention}.\nПричина: {reason}')
#     #         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#     #         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#     #
#     #     await ctx.send(embed=embed)
#
#
#     @commands.command(name='cleanup', pass_context=True)
#     @commands.has_permissions(manage_messages=True)
#     async def cleanup(self, ctx, member: discord.Member, count: int):
#
#         """Delete messages from a specific member.
#         Arguments:
#         `: member` - member
#         `: count` - number of messages
#         __ __
#         For example:
#         ```
#         !cleanup @ Username # 1234 5
#         !cleanup Username 100
#         ```
#         """
#         if count > 100:
#             await ctx.send(f'Число сообщений не должно превышать {count}.')
#         else:
#             def is_member(m):
#                 return m.message.author == member
#
#             await ctx.channel.purge(limit=count, check=is_member)
#
#     @commands.command(name='ban', pass_context=True)
#     @commands.has_permissions(ban_members=True)
#     async def ban(self, ctx, member: discord.Member, *, reason: str = 'N/A'):
#
#         """Block a member on the server. * Yes, the banhammer will rise above <member>! *
#         Arguments:
#         `: member` - member
#         `: reason` - reason
#         __ __
#         For example:
#         ```
#         !ban Username You were a bad guy
#         !ban @ Username # 1234
#         ```
#         """
#         await ctx.guild.ban(user=member, reason=reason)
#
#         embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
#                               description=f'Пользователь {member.mention} забанен!\nПричина: {reason}.')
#         embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
#         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#
#         await ctx.send(embed=embed)
#
#     # @commands.command(name='unban', aliases=['pardon'])
#     # @commands.has_permissions(ban_members=True)
#     # async def unban(self, ctx, user: discord.User, *, reason: str = 'N/A'):
#     #
#     #     """Unblock a member on the server.
#     #     Arguments:
#     #     `: user` - user
#     #     `: reason` - reason
#     #     __ __
#     #     For example:
#     #     ```
#     #     !unban @ Username # 1234 You're good
#     #     ```
#     #     """
#     #     ban_entries = await ctx.guild.bans()
#     #     banned_users = [user.user.name for user in ban_entries]
#     #
#     #     for u in banned_users:
#     #         if u.id == user.id:
#     #             try:
#     #                 await ctx.guild.unban(user=u, reason=reason)
#     #             except:
#     #                 stats = f'Не удалось разбанить {user}.'
#     #             else:
#     #                 stats = f'Пользователь {u.mention} успешно разбанен.'
#     #
#     #     embed = discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000,
#     #                           description=stats)
#     #     embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#     #     embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#     #
#     #     await ctx.send(embed=embed)
#
#     @commands.command(name='banlist', aliases=['bans'], pass_context=True)
#     @commands.has_permissions(ban_members=True)
#     async def banlist(self, ctx):
#         """
#         List of banned members.
#         """
#
#         bans = await ctx.guild.bans()
#
#         if len(bans) <= 0:
#             embed = discord.Embed(timestamp=ctx.message.created_at,
#                                   color=0xff0000,
#                                   description='No banned users.')
#         else:
#             embed = discord.Embed(timestamp=ctx.message.created_at,
#                                   color=0xff0000,
#                                   description=f'Banned users:\n{", ".join([user.user.name for user in bans])}')
#         embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
#         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#
#         await ctx.send(embed=embed)
#
#     @commands.command(name='kick', pass_context=True)
#     @commands.has_permissions(kick_members=True)
#     async def kick(self, ctx, member: discord.Member, *, reason: str = 'N/A'):
#         """
#         `:member` - The person you are kicking
#         `:reason` - Reason for kick
#
#         """
#         await member.kick(reason=reason)
#
#         embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
#                               description=f'User {member} was kicked.\nReason: {reason}.')
#         embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
#         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#
#         await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Management(bot))
