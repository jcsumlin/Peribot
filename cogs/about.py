from discord.ext import commands
import discord

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command('help')
    async def help(self, ):
        embed = discord.Embed(title="Modular Discord bot made by J_C___#8947", color=0x93ff50)
        embed.set_author(name="Peribot", url="http://www.patreon.com/botboi")
        embed.set_thumbnail(url="https://pa1.narvii.com/6363/a99a0f938da2c75791c1cfd8a93173eaf6c54b6a_128.gif")
        embed.add_field(name="!source", value="Interested in my source code? This will return my GitHub repository.")
        embed.add_field(name="!botboi", value="Love Peribot? Want your own bot? I have a Patreon with more info on how you can support my creations!")
        embed2 = discord.Embed(title="Meme Commands", color=0x93ff50)
        embed2.set_thumbnail(url="https://pa1.narvii.com/6507/d2f05279a966b21757f9c55b92ef71bc720dba64_128.gif")
        embed2.add_field(name="!amethyst [text]", value="Generate memes with Amethyst's face!", inline=False)
        embed2.add_field(name="!rogu [text]", value="Generate memes with Roguery in a box!", inline=False)
        embed2.add_field(name="!bigmoji :discord-emoji:", value="Returns a larger version of any emoji/reaction",
                        inline=False)
        embed2.add_field(name="!chikadance", value="(or !chika) returns random gif of Chika Dancing from ", inline=False)
        embed2.add_field(name="!xkcd [number]", value="Returns today's XLCD post or a specific XLCD comic using it's number", inline=False)
        embed2.add_field(name="!penis [user]", value="Detects user's penis length (This is 100% accurate.)", inline=False)
        embed2.add_field(name="!trap",
                         value="Returns either a gif of Star Wars Trap or Anime Trap... Are you a gambling man?", inline=False)
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
        embed4.add_field(name="!setwelcome",
                         value="Sets the channel of your server where you want Peribot to welcome users",
                         inline=False)
        embed4.add_field(name="!ded",
                         value="Press F the chat is dead.",
                         inline=False)
        embed4.add_field(name="!eightball [question]", value="(or !8b) Ask the magic conch your deepest questions",
                        inline=False)
        embed4.add_field(name="!ping", value="Pong!",
                         inline=False)
        embed4.add_field(name="!pin [message]", value="Copy your message in a stylish and modern frame, and then fix it!",
                         inline=False)
        embed4.add_field(name="!roll [max]", value="(or !r) rolls a d20 or d[max] die",
                         inline=False)
        embed4.add_field(name="!flip", value="Flips a coin ... or a user. But not me.",
                         inline=False)
        embed4.add_field(name="!hiatus", value="How long has this Hiatus been going on for? (SVTFOE)", inline=False)
        embed4.add_field(name="!urban [word] [definition number]",
                         value="Uses Urban Dictionary to define a word. Example: !urban hello. If there is more than one definition you can return a specific definition by secifying its number",
                         inline=False)
        embed4.add_field(name="!remindme [quantity]  [time_unit] [text]",
                         value="Sends you <text> when the time is up. Accepts: minutes, hours, days, weeks, month. Example: !remindme 3 days Have sushi with Asu and JennJenn",
                         inline=False)
        embed4.add_field(name="!forgetme", value="Removes all your upcoming notifications", inline=False)
        embed5 = discord.Embed(title="Kindness Commands", color=0x93ff50)
        embed5.set_thumbnail(url="http://pa1.narvii.com/6341/7ff7b249739c0841f8a64ecfe23ab0bc15257ace_128.gif")
        embed5.add_field(name="!kiss [user]", value="Smooch someone you love <3", inline=False)
        embed5.add_field(name="!hug [user]", value="Hug someone with a laundry list of gifs", inline=False)
        embed5.add_field(name="!compliment [user]", value="Make someone's day buy sending them a compliment", inline=False)
        embed5.add_field(name="!ship [user1] [user2]", value="Creates a ship name for two users", inline=False)
        embed6 = discord.Embed(title="Stream Alert Commands", color=0x6441a5)
        embed6.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/gaming-platforms-logo-shapes/250/twitch_logo-256.png")
        embed6.add_field(name="!streamalert [source] [url]", value="Example: !streamalert twitch https://www.twitch.tv/J_C___ This will alert this channel when the specified twitch user goes live.")
        embed6.add_field(name="!streamalert stop [url]", value="Example: !streamalert stop https://www.twitch.tv/J_C___ This will stop alerts in this channel.")
        embed6.add_field(name="!streamset mention [mention_type]", value="Sets mentions for stream alerts Types: everyone, here, none. Example: !streamset mention everyone")
        embed7 = discord.Embed(title="Starboard Commands", color=0x6441a5)
        embed7.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/gaming-platforms-logo-shapes/250/twitch_logo-256.png")
        embed7.add_field(name="!starboard setup [channel] [emoji] [role]", value="Sets the starboard channel, emoji and role. All of the parameters are optional.")
        embed7.add_field(name="!starboard ignore [channel]", value="This will ignore all starboard messages in this channel")
        embed7.add_field(name="!starboard emoji [emoji]", value="Sets the emoji that the starboard tracks. Defaults to ⭐")
        embed7.add_field(name="!starboard channel [channel]", value="Sets the channel that the starboard resides in.")
        embed7.add_field(name="!starboard threshold [threshold]", value="Sets the threshold of 'stars' required for a post to make it to the starboard.")
        embed7.add_field(name="!starboard clear", value="Clears the database of previous starred messages.")

        await self.bot.say(embed=embed)
        await self.bot.say(embed=embed2)
        await self.bot.say(embed=embed3)
        await self.bot.say(embed=embed4)
        await self.bot.say(embed=embed5)
        await self.bot.say(embed=embed6)
        await self.bot.say(embed=embed7)

def setup(bot):
    bot.add_cog(Help(bot))
