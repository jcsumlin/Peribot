import discord
from discord.ext import commands
import praw
import os
from .utils.dataIO import dataIO


class TwoSixNine:
    def __init__(self, bot):
        self.bot = bot
        # self.settings = dataIO.load_json("../config.json")
        self.reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                             client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                             password=os.environ['REDDIT_PASSWORD'],
                             user_agent='SVTFOE command bot (by u/J_C___)',
                             username=os.environ['REDDIT_USERNAME'])
        self.twosixnine_scores = {'PhoenixVersion1':0,
                     'jeepdave':0,
                     'waspstinger106':0,
                     'kotsthepro':0,
                     'BlackoutAviation':0}

    def get_scores(self, user, score=0):
        for submission in self.reddit.redditor(user).submissions.new(limit=500):
            if '/269' in submission.title:
                # print(submission.title + ':' + str(submission.score))
                score = score + int(submission.score)
                # print(score)
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