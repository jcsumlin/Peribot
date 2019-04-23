from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands


class Wander:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def wander(self, ctx, message: str, *argv):
        '''

        :param ctx: Message Context (who sent the message)
        :param message: First word of the message
        :param argv: The rest of your message delineated by spaces
        :return: Returns an image of a Amethyst from SU and your message
        '''
        image = Image.open('data/wandersays.jpg')
        draw = ImageDraw.Draw(image)
        # Dimensions for text box
        boxWidth = image.size[0]
        boxHeight = image.size[1] * 1 / 4
        # arbitrary beginning size; this will change if the message is too big
        fontSize = 75
        font = ImageFont.truetype('data/theboldfont.ttf', fontSize)
        if '\"' in argv:
            list(argv).remove("\"")
        for word in argv:
            message += ' ' + str(word)
        textSize = font.getsize(message)
        textWidth = textSize[0]
        textHeight = textSize[1]
        # our lines
        lines = []
        if textWidth > boxWidth:
            words = message.split()
            isHeightGood = False
            while not isHeightGood:
                height = 0
                lines = []
                line = ''
                for word in words:
                    # For the special kids who make really long nonsense words to try and break the bot
                    # While the size of the word is larger than the image width, shrink the font
                    while font.getsize(word)[0] > boxWidth:
                        fontSize -= 5
                        font = ImageFont.truetype('data/theboldfont.ttf', fontSize)
                        isHeightGood = True
                    textSize = font.getsize(line + word)
                    if (textSize[0] < boxWidth):
                        line += (word + ' ')
                    # Line is too long; add previous line and start a new one
                    else:
                        height += font.getsize(line)[1]
                        isHeightGood = True
                        lines.append(line)
                        line = word + ' '
                        # check if the new height is too long. If it is, reduce font size
                        if (height + font.getsize(line)[1]) > boxHeight:
                            isHeightGood = False
                            fontSize -= 5
                            font = ImageFont.truetype('data/theboldfont.ttf', fontSize)
                            break
                # Grab leftover line and add it to the collection
                lines.append(line)
        else:
            lines.append(message)
        outline = '#000000'
        y = int(image.size[1] * 3 / 4)
        numberOfLines = 0
        for line in lines:
            textWidth = font.getsize(line)[0]
            center = (int(image.size[0] / 2 - textWidth / 2), y)
            draw.text(center, line, outline, font)
            y += font.getsize(line)[1]
            numberOfLines += 1
        image.save('data/wander-edit.png')
        area = ctx.message.channel
        with open('data/wander-edit.png', 'rb') as file:
            await self.bot.send_file(area, file)

def setup(bot):
    bot.add_cog(Wander(bot))
