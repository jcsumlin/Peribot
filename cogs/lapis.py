from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

class Lapis:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def lapis(self, ctx, message, *):
        image = Image.open('data/blak_template.jpg')
        draw = ImageDraw.Draw(image)
        (x, y) = (175, 700)
        if len(message) > 15:
            message1 = message[:15]
            message2 = message[15:]
            message = message1 + "\r\n" + message2
        color = '#000000'  # black color
        outline = '#FFFFFF'
        font = ImageFont.truetype('data/theboldfont.ttf', size=100)
        draw.text((x, y), message, fill=outline, font=font)
        font = ImageFont.truetype('data/theboldfont.ttf', size=99)
        draw.text((x + 1, y - 1), message, fill=color, font=font)
        image.save('data/lapis_edit.png')
        area = ctx.message.channel
        with open('data/lapis_edit.png', 'rb') as file:
            await self.bot.send_file(area, file)



def setup(bot):
    bot.add_cog(Lapis(bot))