import discord
import git
from discord.ext import commands
from discord.ext.commands import CommandNotFound



class Management(commands.Cog):

    """
    Set of commands for Administration.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error

    @commands.command(name='setcolor', no_pm=True)
    async def set_member_color(self, ctx, role: discord.Role, color: discord.Color):
        """
        Color the nickname of the participant. * Let there be bright colors and colors! *
        [!] In development.
        Arguments:
        color in HEX

        For example:
        !setcolor #FF0000
        """
        try:
            await role.edit(color=color)
            if not role.is_default():
                embed = discord.Embed(title=f"Changed the role color for {role.name} to {color}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Peribot cannot affect the default roles.")
                await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title="Peribot does not have permissions to change roles." )
            await ctx.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(title=f"Peribot failed to update {role.name}'s color" )
            await ctx.send(embed=embed)
        except discord.InvalidArgument:
            embed = discord.Embed(title=f"Invalid Arguments!", description="!setcolor @Role [Hex Code or Generic Name]")
            await ctx.send(embed=embed)
        except discord.ext.commands.errors.BadArgument:
            embed = discord.Embed(title=f"Invalid Arguments!", description="!setcolor @Role [Hex Code or Generic Name]")
            await ctx.send(embed=embed)

    @commands.command(name='nick', aliases=["setnick"])
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def nick(self, ctx, user: discord.Member, *, nick):
        if ctx.author.id == 309089769663496194 or ctx.author.id == 204792579881959424:
            await user.edit(nick=nick, reason="Jeep made me do it")

    @commands.command(name='gitpull')
    async def git_pull(self, ctx):
        if ctx.author.id == 204792579881959424:
            git_dir = "./"
            try:
                g = git.cmd.Git(git_dir)
                g.pull()
                embed = discord.Embed(title=":white_check_mark: Successfully pulled from repository", color=0x00df00)
                await ctx.channel.send(embed=embed)
            except Exception as e:
                errno, strerror = e.args
                embed = discord.Embed(title="Command Error!",
                                      description=f"Git Pull Error: {errno} - {strerror}",
                                      color=0xff0007)
                await ctx.channel.send(embed=embed)
        else:
            await ctx.send("You don't have access to this command!")

    @commands.command(name='mute')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.User):
        pass


    @commands.command(name='pin')
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
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        msg = await ctx.send(embed=embed)
        await ctx.message.delete()
        await msg.pin()
#
#     @commands.command(name='resetmute', )
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
#     @commands.command(name='cleanup', )
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
#     @commands.command(name='ban', )
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
#         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
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
#     @commands.command(name='banlist', aliases=['bans'], )
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
#         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#         embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
#
#         await ctx.send(embed=embed)
#
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = 'N/A'):
        """
        `:member` - The person you are kicking
        `:reason` - Reason for kick

        """
        try:
            await member.kick(reason=reason)
        except Exception as e:
            await ctx.send("error")
            return
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                              description=f'User {member.name} was kicked.\nReason: {reason}.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = 'N/A', delete: int = 0):
        """
        `:member` - The person you are banning @ them
        `:reason` - Reason for kick

        """
        try:
            await member.ban(reason=reason, delete_message_days=delete)
        except discord.Forbidden:
            embed = discord.Embed(title="Command Error!", description=f"I do not have permissions to do that", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        except discord.HTTPException:
            embed = discord.Embed(title="Command Error!", description=f"Banning failed. Try again", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                              description=f'User {member.name} was banned.\nReason: {reason}.\nMessages Deleted: {delete} days')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        await ctx.send(embed=embed)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: int, *, reason: str = 'N/A'):
        """
        `:member` - The person you are unbanning (their ID)
        `:reason` - Reason for kick

        """
        for banentry in await ctx.guild.bans():
            if member == banentry.user.id:
                try:
                    await ctx.guild.unban(banentry.user, reason=reason)
                except discord.Forbidden:
                    embed = discord.Embed(title="Command Error!", description=f"I do not have permissions to do that",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                except discord.HTTPException:
                    embed = discord.Embed(title="Command Error!", description=f"Unbanning failed. Try again",
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                                      description=f'User {banentry.user.name} was unbanned.\nReason: {reason}.')
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
                await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Management(bot))
