import configparser
from datetime import datetime

import discord
from discord.ext import commands
from tmdbv3api import TMDb, Season


class Hiatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read('../auth.ini')

        self.tmdb = TMDb()
        self.tmdb.api_key = config.get('TMDB', 'api_key')
        self.StevenUniverseServerIDs = [593887030216228973]
        self.StarVsServerIDs = [
            448695150135345152,
            452307445059026946,
            606970684136226846
        ]

    @commands.command(name='hiatus',
                    description="How long has this Hiatus been going on for?",
                    breif="The hiatus is cold and long",
                    )
    async def hiatus(self, ctx):
        """
        Will return the number of days since the last episode of SVTFOE. The nexus of the hiatus...
        :return: Preformatted Message with calculated days
        """
        # date_of_last_episode = datetime.strptime('Apr 7 2018 01:00AM',
        #                                          '%b %d %Y %I:%M%p')  # Set from config
        # days = re.search('\d{1,3}\s', str(datetime.now() - date_of_last_episode)).group(0)
        # msg = "Days since last episode:\n\n" + "[" + days + "Days]"

        if ctx.guild.id in self.StevenUniverseServerIDs:
            season = Season()
            latest_season = False
            season_number = 1
            while latest_season is False:
                show_season = season.details(61175, season_number)
                if "status_code" in show_season.entries and show_season.entries["status_code"] == 34:
                    show_season = season.details(61175, season_number-1)
                    latest_season = True
                else:
                    season_number += 1
            episode =show_season.entries['episodes'][-1]
            air_date = episode['air_date']
            diffrence = datetime.now() - datetime.strptime(air_date, "%Y-%m-%d")
            a = datetime(2019, 9, 2)
            b = datetime.now()
            embed = discord.Embed(title="Steven Universe Hiatus Calculator")
            embed.set_thumbnail(url='https://image.tmdb.org/t/p/w600_and_h900_bestv2/g31ZPZSjv8ySPbclyYZZU50XhZy.jpg')
            embed.add_field(name=f"Days Since Season {episode['season_number']} {episode['name']}", value=f"{diffrence.days} Days", inline=False)
            embed.add_field(name=f"Days Since Season The Movie", value=f"{(b-a).days} Days", inline=False)
            return await ctx.channel.send(embed=embed)

        if ctx.guild.id in self.StarVsServerIDs:
            season = Season()
            latest_season = False
            season_number = 1
            while latest_season is False:
                show_season = season.details(61923, season_number)
                if "status_code" in show_season.entries and show_season.entries["status_code"] == 34:
                    show_season = season.details(61923, season_number-1)
                    latest_season = True
                else:
                    season_number += 1
            episode =show_season.entries['episodes'][-1]
            air_date = episode['air_date']
            diffrence = datetime.now() - datetime.strptime(air_date, "%Y-%m-%d")
            embed = discord.Embed(title="Star Vs The Forces Of Evil Hiatus Calculator")
            embed.set_thumbnail(url="https://image.tmdb.org/t/p/w600_and_h900_bestv2/dKFL1AOdKNoazqZDg1zq2z69Lx1.jpg")
            embed.add_field(name=f"Days Since Season {episode['season_number']} {episode['name']}", value=f"{diffrence.days} Days")
            return await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Hiatus(bot))
