import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('help', aliases=["phelp"])
    async def help(self, ctx):
        embed = discord.Embed(title="A modular Discord bot made by J_C___#8947", color=0x93ff50)
        embed.set_author(name="Peribot", url="http://www.patreon.com/botboi")
        embed.set_thumbnail(url="https://pa1.narvii.com/6363/a99a0f938da2c75791c1cfd8a93173eaf6c54b6a_128.gif")
        embed.add_field(name="!source", value="Interested in my source code? This will return my GitHub repository.")
        embed.add_field(name="!botboi",
                        value="Love Peribot? Want your own bot? I have a Patreon with more info on how you can support my creations!")
        embed2 = discord.Embed(title="Meme Commands", color=0x93ff50)
        embed2.set_thumbnail(url="https://pa1.narvii.com/6507/d2f05279a966b21757f9c55b92ef71bc720dba64_128.gif")
        embed2.add_field(name="!bigmoji :discord-emoji:", value="Returns a larger version of any emoji/reaction",
                         inline=False)
        embed2.add_field(name="!chikadance", value="(or !chika) returns random gif of Chika Dancing from ",
                         inline=False)
        embed2.add_field(name="!xkcd [number]",
                         value="Returns today's XLCD post or a specific XLCD comic using it's number", inline=False)
        embed3 = discord.Embed(title="Custom Commands", color=0x93ff50)

        embed3.set_thumbnail(url="http://pa1.narvii.com/6520/ee53df0ba159bbebb84d3d7ed35bf89e8e978ac5_128.gif")
        embed3.add_field(name="!cc add [command-name] [result]",
                         value="Adds a server specific command that will return whatever text/link you want!",
                         inline=False)
        embed3.add_field(name="!cc list", value="Lists all of the server specific custom commands available",
                         inline=False)
        embed3.add_field(name="!cc edit [command-name] [result]",
                         value="Edit what the bot says when you use your custom command",
                         inline=False)
        embed3.add_field(name="!cc delete [command]",
                         value="Remove custom command from your server.",
                         inline=False)
        embed4 = discord.Embed(title="Utility Commands", color=0x93ff50)
        embed4.set_thumbnail(url="https://pa1.narvii.com/6328/aef12f691e993564ae13c1e19c6d19d907d5886a_128.gif")
        embed4.add_field(name="!welcome enable #channel [custom message | optional]",
                         value="Sets the channel of your server where you want Peribot to welcome users\nNote: you can add [user] to your custom message to mention the new user!",
                         inline=False)
        embed4.add_field(name="!welcome disable",
                         value="Disables the welcome new users function",
                         inline=False)
        embed4.add_field(name="!poll [question], [option 1], [option ...]",
                         value="Creates a poll for users to respond to. You can use up to 10 options!", inline=False)
        embed4.add_field(name="!quickpoll [question]",
                         value="Creates a quick yes, no or i dont car poll for users to respond to", inline=False)
        embed4.add_field(name="!ded",
                         value="Press F the chat is dead.",
                         inline=False)
        embed4.add_field(name="!eightball [question]", value="(or !8b) Ask the magic conch your deepest questions",
                         inline=False)

        embed4.add_field(name="!ping", value="Pong!",
                         inline=False)
        embed4.add_field(name="!avatar [User]", value="Sends the [user]'s Discord Avatar",
                         inline=False)
        embed4.add_field(name="!pin [message]",
                         value="Copy your message in a stylish and modern frame, and then fix it!",
                         inline=False)
        embed4.add_field(name="!roll [max]", value="(or !r) rolls a d20 or d[max] die",
                         inline=False)
        embed4.add_field(name="!flip", value="Flips a coin ... or a user. But not me.",
                         inline=False)
        embed4.add_field(name="!hiatus", value="How long has this Hiatus been going on for? (SVTFOE and SU)",
                         inline=False)
        embed4.add_field(name="!urban [word] [definition number]",
                         value="Uses Urban Dictionary to define a word. Example: !urban hello. If there is more than one definition you can return a specific definition by secifying its number",
                         inline=False)
        embed4.add_field(name="!remindme [quantity] [time_unit] [text]",
                         value="Sends you <text> when the time is up. Accepts: minutes, hours, days, weeks, month. Example: !remindme 3 days Have sushi with Asu and JennJenn",
                         inline=False)
        embed4.add_field(name="!remindhere [quantity] [time_unit] [text]",
                         value="Sends a channel <text> when the time is up. Accepts: minutes, hours, days, weeks, month. Example: !remindhere 3 days Have sushi with Asu and JennJenn. Will use @here! and requires role with name 'RemindHere'",
                         inline=False)
        embed4.add_field(name="!forgetme", value="Removes all your upcoming notifications", inline=False)
        embed5 = discord.Embed(title="Kindness Commands", color=0x93ff50)
        embed5.set_thumbnail(url="http://pa1.narvii.com/6341/7ff7b249739c0841f8a64ecfe23ab0bc15257ace_128.gif")
        embed5.add_field(name="!kiss [user]", value="Smooch someone you love <3", inline=False)
        embed5.add_field(name="!cuddle [user]",
                         value="Cuddle your favorite users with lots of love <3. Results may vary...", inline=False)
        embed5.add_field(name="!cats", value="Sends a cute cat :3", inline=False)
        embed5.add_field(name="!pugs [user]", value="Sends a cute Pug", inline=False)
        embed5.add_field(name="!catsbomb [amount]", value="Throws a cat bomb! Amount Defaults to 5", inline=False)
        embed5.add_field(name="!pugsbomb [amount]", value="Throws a pugs bomb! Amount defaults to 5", inline=False)
        embed5.add_field(name="!hug [user]", value="Hug someone with a laundry list of gifs", inline=False)
        embed5.add_field(name="!compliment [user]", value="Make someone's day buy sending them a compliment",
                         inline=False)
        embed5.add_field(name="!ship [user1] [user2]", value="Creates a ship name for two users", inline=False)
        embed6 = discord.Embed(title="Stream Alert Commands", color=0x6441a5)
        embed6.set_thumbnail(
            url="https://cdn2.iconfinder.com/data/icons/gaming-platforms-logo-shapes/250/twitch_logo-256.png")
        embed6.add_field(name="!streamalert [source] [url]",
                         value="Example: !streamalert twitch https://www.twitch.tv/J_C___ This will alert this channel when the specified twitch user goes live.",
                         inline=False)
        embed6.add_field(name="!streamalert stop [url]",
                         value="Example: !streamalert stop https://www.twitch.tv/J_C___ This will stop alerts in this channel.",
                         inline=False)
        embed6.add_field(name="!streamset mention [mention_type]",
                         value="Sets mentions for stream alerts Types: everyone, here, none. Example: !streamset mention everyone",
                         inline=False)
        embed7 = discord.Embed(title="Starboard Commands", color=0x93ff50)
        embed7.set_thumbnail(
            url="https://66.media.tumblr.com/6a26e7bb8eb024d8a8b5ee7eef1ac04f/tumblr_p0xl72aK9y1vdwh7uo2_500.gif")
        embed7.add_field(name="!starboard setup [channel] [emoji] [role]",
                         value="Sets the starboard channel, emoji and role. All of the parameters are optional.",
                         inline=False)
        embed7.add_field(name="!starboard ignore [channel]",
                         value="This will ignore all starboard messages in this channel", inline=False)
        embed7.add_field(name="!starboard emoji [emoji]",
                         value="Sets the emoji that the starboard tracks. Defaults to ⭐", inline=False)
        embed7.add_field(name="!starboard channel [channel]", value="Sets the channel that the starboard resides in.",
                         inline=False)
        embed7.add_field(name="!starboard threshold [threshold]",
                         value="Sets the threshold of 'stars' required for a post to make it to the starboard.",
                         inline=False)
        embed7.add_field(name="!starboard clear", value="Clears the database of previous starred messages.",
                         inline=False)

        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)
        await ctx.send(embed=embed4)
        await ctx.send(embed=embed5)
        await ctx.send(embed=embed6)
        await ctx.send(embed=embed7)

    @commands.command(aliases=['server', 'sinfo', 'si'], )
    async def serverinfo(self, ctx):
        """Various info about the server. !help server for more info."""
        guild = ctx.guild
        online = 0
        for i in guild.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        all_users = []
        for user in guild.members:
            all_users.append('{}#{}'.format(user.name, user.discriminator))
        all_users.sort()
        all = '\n'.join(all_users)

        channel_count = len(
            [x for x in guild.channels if type(x) == self.bot.get_all_channels()])

        role_count = len(guild.roles)
        emoji_count = len(guild.emojis)
        print("Done with calculations")
        em = discord.Embed(title="", color=discord.Color.green())
        em.add_field(name='Name', value=guild.name)
        em.add_field(name='Owner', value=guild.owner.nick, inline=False)
        em.add_field(name='Members', value=str(guild.member_count))
        em.add_field(name='Currently Online', value=str(online))
        em.add_field(name='Text Channels', value=str(channel_count))
        em.add_field(name='Region', value=guild.region)
        em.add_field(name='Verification Level', value=str(guild.verification_level))
        # em.add_field(name='Highest role', value=guild.role_hierarchy[0])
        em.add_field(name='Number of roles', value=str(role_count))
        em.add_field(name='Number of emotes', value=str(emoji_count))
        em.add_field(name='Number of boosts', value=str(guild.premium_subscription_count))
        if len(guild.features) > 0:
            em.add_field(name='Guild Features', value=f"{guild.features.join(', ')}")
        em.add_field(name='Created At',
                     value=guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        if guild.is_icon_animated():
            em.set_thumbnail(url=guild.icon_url_as(format='gif'))
        else:
            em.set_thumbnail(url=guild.icon_url_as(format='png'))
        em.set_author(name='Server Info')
        em.set_footer(text='Server ID: %s' % guild.id)
        print("sending")
        message = await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))
