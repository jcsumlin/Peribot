import unicodedata
import discord
from discord.ext import commands
from loguru import logger

try:
    import cairosvg
    cairo = True
except Exception as e:
    cairo = False


class Bigmoji(commands.Cog):

    """Emoji tools"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bigmoji")
    async def bigmoji(self, ctx, emoji):
        """Post a large .png of an emoji"""
        logger.debug(emoji)
        if emoji[0] == '<':
            emoji_name = emoji.split(':')[2][:-1]
            anim = emoji.split(':')[0]
            if anim == '<a':
                url = 'https://cdn.discordapp.com/emojis/' + emoji_name + '.gif'
            else:
                url = 'https://cdn.discordapp.com/emojis/' + emoji_name + '.png'
        else:
            chars = []
            name = []
            for char in emoji:
                chars.append(str(hex(ord(char)))[2:])
                try:
                    name.append(unicodedata.name(char))
                except ValueError:
                    # Sometimes occurs when the unicodedata library cannot
                    # resolve the name, however the image still exists
                    name.append("none")
            if cairo:
                url = 'https://twemoji.maxcdn.com/2/svg/' + '-'.join(chars) + '.svg'
            else:
                url = 'https://twemoji.maxcdn.com/2/72x72/' + '-'.join(chars) + '.png'
        e = discord.Embed().set_image(url=url)
        await ctx.send(embed=e)

def setup(bot):
    n = Bigmoji(bot)
    bot.add_cog(n)
    if not cairo:
        logger.error('Could not import cairosvg. Standard emoji conversions will be '
              'limited to 72x72 png.')
