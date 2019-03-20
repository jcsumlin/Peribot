import discord
from discord.ext import commands
import praw
from psaw import PushshiftAPI
import os
from .utils.dataIO import dataIO
from loguru import logger
import configparser

class TwoSixNine:
    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read('../auth.ini')
        # self.settings = dataIO.load_json("../config.json")
        try:
            reddit = praw.Reddit(client_id=config.get('reddit', 'REDDIT_CLIENT_ID'),
                                 client_secret=config.get('reddit', 'REDDIT_CLIENT_SECRET'),
                                 password=config.get('reddit', 'REDDIT_PASSWORD'),
                                 user_agent='SVTFOE command bot (by u/J_C___)',
                                 username=config.get('reddit', 'REDDIT_USERNAME'))
            self.api = PushshiftAPI(reddit)
        except Exception as e:
            logger.error(f"Cant connect to Reddit with these credentials {e}")

        self.twosixnine_scores = {'PhoenixVersion1':0,
                     'jeepdave':0,
                     'waspstinger106':0,
                     'kotsthepro':0,
                     'BlackoutAviation':0}

    def get_scores(self, user, score=0):
        try:
            results = list(self.api.search_submissions(author=str(user), limit=2000, title='/269'))
            for submission in results:
                if '/269' in submission.title:
                    # print(submission.title + ':' + str(submission.score))
                    score = score + int(submission.score)
                    # print(score)
        except Exception as e:
            logger.error(f"Exception occured in get_scores() : {e}")
        return score

    @commands.command(name="twosixnine", pass_context=True, aliases=['269', 'scores'])
    async def twosixnine(self, ctx):
        '''
        Gets karma for 269 challenge. This command is hardcoded.
        :param ctx: Information on who sent the message
        :return: Returns an embed of the 269 Reddit Karma challenge. The users are set in stone and sealed in blood.
        '''
        for user in self.twosixnine_scores.keys():
            self.twosixnine_scores[user] = self.get_scores(user)
        embedMsg = discord.Embed(color=0xE87722, title="__269 Days of Shitposts Challenge__")
        embedMsg.add_field(name="Jeep", value=str(self.twosixnine_scores['jeepdave']))
        embedMsg.add_field(name="PhoenixVersion1", value=str(self.twosixnine_scores['PhoenixVersion1']))
        embedMsg.add_field(name="Waspstinger106", value=str(self.twosixnine_scores['waspstinger106']))
        embedMsg.add_field(name="Kots", value=str(self.twosixnine_scores['kotsthepro']))
        embedMsg.add_field(name="BlackoutAviation",
                           value=str(self.twosixnine_scores['BlackoutAviation']))
        await self.bot.send_message(ctx.message.channel, embed=embedMsg)


def setup(bot):
    bot.add_cog(TwoSixNine(bot))
