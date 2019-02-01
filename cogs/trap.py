import discord
from discord.ext import commands
import random

class Trap:

    def __init__(self, bot):
        self.bot = bot
        self.trap_gifs = ['https://media1.tenor.com/images/b43df533b92a60a6302a3fceb6ea532c/tenor.gif',
                     'https://media1.tenor.com/images/1b011a65b404188031d13c866eb7c793/tenor.gif',
                     'https://media1.tenor.com/images/4fd0125d511e202a50bd41e120187506/tenor.gif',
                     'https://thumbs.gfycat.com/WhichGratefulBettong-small.gif',
                     'https://steamuserimages-a.akamaihd.net/ugc/848214956775689562/2DE796CA8D75CEA67F717E22885461760D546479/',
                     'https://i.pinimg.com/originals/36/e6/71/36e671921eecfefde01cbfdd35c25997.gif',
                     'https://66.media.tumblr.com/6ebba4bdefbb672416e86145b621bef9/tumblr_ov0yh7aLHZ1td5qjgo1_400.gif',
                     'https://pa1.narvii.com/6501/0d985d7b0fbdfed6eaac2a7d0c16616301c30de7_hq.gif',
                     'https://66.media.tumblr.com/23ec2fb29499576f465a45557b2b3a55/tumblr_omk741Am1E1qa94xto1_400.gif']

    @commands.command(pass_context=True, no_pm=True)
    async def trap(self):
        '''
        Returns either a gif of Star Wars Trap or Anime Trap... Are you a gambling man?
        :return: What kind of trap is it?
        '''
        type = random.randint(1, 2)
        if type == 1:
            embed = discord.Embed(title="Now ***that's*** a trap!", color=0xffd2e8)
            embed.set_image(url=random.choice(self.trap_gifs))
            await self.bot.say(embed=embed)
        elif type == 2:
            embed = discord.Embed(title="ITS A TRAP!", color=0x381010)
            embed.set_image(url='https://media.giphy.com/media/8McNH1aXZnVyE/giphy.gif')
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Trap(bot))