from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

class Lapis:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def lapis(self, ctx, message, *):
        image = Image.open('data/blak_template.jpg')
		
        draw = ImageDraw.Draw(image)
        
		# Dimensions for text box
		boxWidth = image.size[0]
		
		boxHeight = image.size[1] * 1 / 4
		
		# arbitrary beginning size; this will change if the message is too big
		fontSize = 100
		
		font = ImageFont.truetype('data/theboldfont.ttf', fontSize)
		
		textSize = font.getsize(message)
		
		textWidth = textSize[0]
		
		textHeight = textSize[1]
		
		# our lines 
		lines = []
		
		line = ''
		
		if textWidth > boxWidth:
			words = message.split()
			
			isHeightGood = False
			
			while not isHeightGood:
				
				height = 0
				
				for word in words:
					
					# For the special kids who make really long nonsense words to try and break the bot
					# While the size of the word is larger than the image width, shrink the font
					while font.getsize(word)[0] > boxWidth:
						fontSize -= 5
						
						font = ImageFont.truetype('data/theboldfont.ttf', fontSize)
						
					textSize = font.getsize(line + word)
					
					if(textSize[0] < boxWidth):
						line += (word + ' ')
					
					# Line is too long; add previous line and starta new one
					else:
						height += font.getsize(line)[1]
						
						isHeightGood = True
						
						lines.append(line)
						
						line = word + ' '
						
						# check if the new height is too long. If it is, reduce font size
						if (height + font.getsize(line)[1]) > boxHeight:
							isHeightGood = false
							
							fontSize -= 5
							
							font = ImageFont.truetype('data/theboldfont.ttf', fontSize)
							
							break
				
				# Grab leftover line and add it to the collection
				lines.append(line)
		else:
			lines.append(message)
		
        color = '#000000'  # black color
        outline = '#FFFFFF'
		
		y = int(image.size[1] * 3 / 4)
		
		for line in lines:
			textWidth = font.getsize(line)[0]
			
			center = (int(image.size[0] / 2 - textWidth / 2), y)
			
			draw.text(center, line, outline, font)
			
			draw.text(center, line, color, font - 1)
		
        image.save('data/lapis_edit.png')
		
        area = ctx.message.channel
        
		with open('data/lapis_edit.png', 'rb') as file:
			
			await self.bot.send_file(area, file)



def setup(bot):
    bot.add_cog(Lapis(bot))