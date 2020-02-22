import datetime

import discord
from discord.ext import commands
from loguru import logger

from cogs.utils.checks import hastebin


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('help', aliases=["phelp"])
    async def help(self, ctx):
        embed = discord.Embed(title="A modular Discord bot made by J\_C\_\_\_#8947", color=0x93ff50)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name="Peribot Help :: Patreon Support Page", url="http://www.patreon.com/botboi")
        embed.set_thumbnail(url="https://pa1.narvii.com/6363/a99a0f938da2c75791c1cfd8a93173eaf6c54b6a_128.gif")
        embed.add_field(name="View Command Documentation", value="[Here](https://jcsumlin.github.io/peribot-docs/)")
        embed.add_field(name="Support Server", value="[Join Now](https://discord.gg/dGGdQQD)")
        embed.set_footer(text=f"ID: {ctx.author.id}")

        await ctx.send(embed=embed)

    @commands.group(aliases=['server', 'sinfo', 'si'], invoke_without_command=True)
    async def serverinfo(self, ctx, *, msg=""):
        """Various info about the server. [p]help server for more info."""
        if ctx.invoked_subcommand is None:
            if msg:
                server = None
                try:
                    float(msg)
                    server = self.bot.get_guild(int(msg))
                    if not server:
                        return await ctx.send(
                            self.bot.bot_prefix + 'Server not found.')
                except:
                    for i in self.bot.guilds:
                        if i.name.lower() == msg.lower():
                            server = i
                            break
                    if not server:
                        return await ctx.send(
                            self.bot.bot_prefix + 'Could not find server. Note: You must be a member of the server you are trying to search.')
            else:
                server = ctx.message.guild

            online = 0
            for i in server.members:
                if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    online += 1
            all_users = []
            for user in server.members:
                all_users.append('{}#{}'.format(user.name, user.discriminator))
            all_users.sort()
            all = '\n'.join(all_users)

            channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

            role_count = len(server.roles)
            emoji_count = len(server.emojis)

            em = discord.Embed(color=0xea7938)
            em.add_field(name='Name', value=server.name)
            em.add_field(name='Owner', value=server.owner, inline=False)
            em.add_field(name='Members', value=server.member_count)
            em.add_field(name='Currently Online', value=str(online))
            em.add_field(name='Text Channels', value=str(channel_count))
            em.add_field(name='Region', value=server.region)
            em.add_field(name='Verification Level', value=str(server.verification_level))
            em.add_field(name='Highest role', value=server.roles[-1])
            em.add_field(name='Number of roles', value=str(role_count))
            em.add_field(name='Number of emotes', value=str(emoji_count))
            url = await hastebin(str(all))

            hastebin_of_users = '[List of all {} users in this server]({})'.format(server.member_count, url)
            em.add_field(name='Users', value=hastebin_of_users)
            em.add_field(name='Created At', value=server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
            em.set_thumbnail(url=server.icon_url)
            em.set_author(name='Server Info', icon_url='https://i.imgur.com/RHagTDg.png')
            em.set_footer(text='Server ID: %s' % server.id)
            logger.debug(all)
            await ctx.send(embed=em)
            await ctx.message.delete()

    @serverinfo.command(pass_context=True)
    async def emojis(self, ctx, msg: str = None):
        """List all emojis in this server. Ex: [p]server emojis"""
        server = ctx.message.guild
        emojis = [str(x) for x in server.emojis]
        await ctx.send("".join(emojis))
        await ctx.message.delete()

    @serverinfo.command(pass_context=True)
    async def avi(self, ctx, msg: str = None):
        """Get server avatar image link."""
        server = ctx.message.guild
        em = discord.Embed()
        em.set_image(url=server.icon_url)
        await ctx.send(embed=em)
        await ctx.message.delete()

    @serverinfo.command()
    async def role(self, ctx, *, msg):
        """Get more info about a specific role. Ex: [p]server role Admins"""
        guild = ctx.message.guild
        guild_roles = ctx.message.guild.roles
        for role in guild_roles:
            if msg.lower() == role.name.lower() or msg == role.id:
                all_users = [str(x) for x in role.members]
                all_users.sort()
                all_users = ', '.join(all_users)
                em = discord.Embed(title='Role Info', color=role.color)
                em.add_field(name='Name', value=role.name)
                em.add_field(name='ID', value=role.id, inline=False)
                em.add_field(name='Users in this role', value=str(len(role.members)))
                em.add_field(name='Role color hex value', value=str(role.color))
                em.add_field(name='Role color RGB value', value=role.color.to_rgb())
                em.add_field(name='Mentionable', value=role.mentionable)
                if len(role.members) > 10:
                    all_users = all_users.replace(', ', '\n')
                    url = await hastebin(str(all_users))
                    em.add_field(name='All users',
                                 value='{} users. [List of users posted to Hastebin.]({})'.format(len(role.members),
                                                                                                  url), inline=False)
                elif len(role.members) >= 1:
                    em.add_field(name='All users', value=all_users, inline=False)
                else:
                    em.add_field(name='All users', value='There are no users in this role!', inline=False)
                em.add_field(name='Created at', value=role.created_at.__format__('%x at %X'))
                em.set_thumbnail(url='http://www.colorhexa.com/{}.png'.format(str(role.color).strip("#")))
                await ctx.message.delete()
                return await ctx.send(content=None, embed=em)
        await ctx.message.delete()
        await ctx.send(self.bot.bot_prefix + 'Could not find role ``{}``'.format(msg))

    @commands.command(aliases=['channel', 'cinfo', 'ci'], no_pm=True)
    async def channelinfo(self, ctx, channel: int = None):
        """Shows channel information"""
        if not channel:
            channel = ctx.message.channel
        else:
            channel = self.bot.get_channel(channel)
        data = discord.Embed()
        if hasattr(channel, 'mention'):
            data.description = "**Information about Channel:** " + channel.mention
        if hasattr(channel, 'changed_roles'):
            if len(channel.changed_roles) > 0:
                data.color = discord.Color.green() if channel.changed_roles[0].permissions.read_messages else discord.Color.red()
        if isinstance(channel, discord.TextChannel):
            _type = "Text"
        elif isinstance(channel, discord.VoiceChannel):
            _type = "Voice"
        else:
            _type = "Unknown"
        data.add_field(name="Type", value=_type)
        data.add_field(name="ID", value=channel.id, inline=False)
        if hasattr(channel, 'position'):
            data.add_field(name="Position", value=channel.position)
        if isinstance(channel, discord.VoiceChannel):
            if channel.user_limit != 0:
                data.add_field(name="Users Connected", value="{}/{}".format(len(channel.members), channel.user_limit))
            else:
                data.add_field(name="Users Connected", value="{}".format(len(channel.members)))

            userlist = [r.display_name for r in channel.members]
            if not userlist:
                userlist = "None"
            else:
                userlist = "\n".join(userlist)

            data.add_field(name="Users", value=userlist)
            data.add_field(name="Bitrate", value=str(channel.bitrate))
        elif isinstance(channel, discord.TextChannel):
            try:
                pins = await channel.pins()
                data.add_field(name="Pins", value=str(len(pins)), inline=True)
            except discord.Forbidden:
                pass
            data.add_field(name="Members", value="%s" % len(channel.members))
            if channel.topic:
                data.add_field(name="Topic", value=channel.topic, inline=False)
            hidden = []
            allowed = []
            for role in channel.changed_roles:
                if role.permissions.read_messages is True:
                    if role.name != "@everyone":
                        allowed.append(role.mention)
                elif role.permissions.read_messages is False:
                    if role.name != "@everyone":
                        hidden.append(role.mention)
            if len(allowed) > 0:
                data.add_field(name='Allowed Roles ({})'.format(len(allowed)), value=', '.join(allowed), inline=False)
            if len(hidden) > 0:
                data.add_field(name='Restricted Roles ({})'.format(len(hidden)), value=', '.join(hidden), inline=False)
        if channel.created_at:
            data.set_footer(text=("Created on {} ({} days ago)".format(channel.created_at.strftime("%d %b %Y %H:%M"), (
                        ctx.message.created_at - channel.created_at).days)))
        await ctx.send(embed=data)

    @commands.group(invoke_without_command=True, aliases=['user', 'uinfo', 'info', 'ui'])
    async def userinfo(self, ctx, *, name=None):
        """Get user info. Ex: [p]info @user"""
        if ctx.invoked_subcommand is None:
            if name:
                try:
                    user = ctx.message.mentions[0]
                except IndexError:
                    user = ctx.guild.get_member_named(name)
                if not user:
                    user = ctx.guild.get_member(int(name))
                if not user:
                    user = self.bot.get_user(int(name))
                if not user:
                    await ctx.send(self.bot.bot_prefix + 'Could not find user.')
                    return
            else:
                user = ctx.message.author

            avi = user.avatar_url_as(format='png')

            if isinstance(user, discord.Member):
                role = user.top_role.name
                if role == "@everyone":
                    role = "N/A"
                voice_state = None if not user.voice else user.voice.channel
            em = discord.Embed(timestamp=ctx.message.created_at, colour=0x708DD0)
            em.add_field(name='User ID', value=user.id, inline=True)
            if isinstance(user, discord.Member):
                em.add_field(name='Nick', value=user.nick, inline=True)
                em.add_field(name='Status', value=user.status, inline=True)
                em.add_field(name='In Voice', value=voice_state, inline=True)
                for activity in user.activities:
                    if activity.type == 4:
                        continue
                    game = activity.name
                    em.add_field(name='Game', value=game, inline=True)
                em.add_field(name='Highest Role', value=role, inline=True)
            em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
            if isinstance(user, discord.Member):
                em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
            em.set_thumbnail(url=avi)
            em.set_author(name=user, icon_url='')
            await ctx.send(embed=em)
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Help(bot))
