import shlex

import discord
from discord.ext import commands


def to_keycap(c):
    return '\N{KEYCAP TEN}' if c == 10 else str(c) + '\u20e3'


class Polls(commands.Cog):
    """Poll voting system."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True, )
    async def poll(self, ctx, *, questions_and_choices: str):
        """
        delimit questions and answers by either | or ,
        supports up to 10 choices
        """
        if "|" in questions_and_choices:
            delimiter = "|"
        elif "," in questions_and_choices:
            delimiter = ","
        else:
            delimiter = None
        if delimiter is not None:
            questions_and_choices = questions_and_choices.split(delimiter)
        else:
            questions_and_choices = shlex.split(questions_and_choices)

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 11:
            return await ctx.send('You can only have up to 10 choices.')

        # perms = ctx.channel.permissions_for(ctx.guild.me)
        # if not (perms.read_message_history or perms.add_reactions):
        #     return await ctx.channel.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_keycap(e), v) for e, v in enumerate(questions_and_choices[1:], 1)]
        try:
            await ctx.message.delete()
        except:
            pass
        answers = ""
        number = 1
        for answer in choices:
            answers += f"**{number})** {answer[1]}\n"
            number += 1
        author = ctx.author.name.replace('_', '\_').replace('~', '\~').replace('|', '\|').replace('*', '\*')
        e = discord.Embed(title=f':newspaper: {author} asks: {question}', color=discord.Color.green(), description=answers)

        poll = await ctx.channel.send(embed=e)
        for emoji, _ in choices:
            await poll.add_reaction(emoji)

    @commands.command(no_pm=True, )
    async def quickpoll(self, ctx, *, question: str):
        """
        Quick and easy yes/no poll, for multiple answers, see !quickpoll
        """
        author = ctx.author.name.replace('_', '\_').replace('~', '\~').replace('|', '\|').replace('*', '\*')
        message = "**{}** asks: {}".format(author, question)
        embed = discord.Embed(title=':newspaper: ' +message, color=discord.Color.green())
        msg = await ctx.channel.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass

        yes_thumb = "👍"
        no_thumb = "👎"
        shrug_emoji = "🤷"
        await msg.add_reaction(yes_thumb)
        await msg.add_reaction(shrug_emoji)
        await msg.add_reaction(no_thumb)


def setup(bot):
    bot.add_cog(Polls(bot))
