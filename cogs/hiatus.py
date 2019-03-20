from discord.ext import commands
import re
from datetime import datetime

from discord.ext import commands


class Hiatus:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hiatus',
                    description="How long has this Hiatus been going on for?",
                    breif="The hiatus is cold and long",
                    pass_context=False)
    async def hiatus(self):
        """
        Will return the number of days since the last episode of SVTFOE. The nexus of the hiatus...
        :return: Preformatted Message with calculated days
        """
        # date_of_last_episode = datetime.strptime('Apr 7 2018 01:00AM',
        #                                          '%b %d %Y %I:%M%p')  # Set from config
        # days = re.search('\d{1,3}\s', str(datetime.now() - date_of_last_episode)).group(0)
        # msg = "Days since last episode:\n\n" + "[" + days + "Days]"
        msg = "SEASON 4 IS HERE FOOL!\nGo watch it now!!\nhttp://bit.ly/2u1CGHu"
        return await self.bot.say(msg)



def setup(bot):
    bot.add_cog(Hiatus(bot))
