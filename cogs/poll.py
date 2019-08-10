import shlex

import discord
from discord.ext import commands


def to_keycap(c):
    return '\N{KEYCAP TEN}' if c == 10 else str(c) + '\u20e3'


class Polls:
    """Poll voting system."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True, pass_context=True)
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
            return await self.bot.send_message(ctx.message.channel, 'Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 11:
            return await self.bot.send_message(ctx.message.channel, 'You can only have up to 10 choices.')

        # perms = ctx.channel.permissions_for(ctx.message.server.me)
        # if not (perms.read_message_history or perms.add_reactions):
        #     return await self.bot.send_message(ctx.message.channel, 'Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_keycap(e), v) for e, v in enumerate(questions_and_choices[1:], 1)]
        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass
        answers = ""
        number = 1
        for answer in choices:
            answers += f"**{number})** {answer[1]}\n"
            number += 1
        author = ctx.message.author.name.replace('_', '\_').replace('~', '\~').replace('|', '\|').replace('*', '\*')
        e = discord.Embed(title=f':newspaper: {author} asks: {question}', color=discord.Color.green(), description=answers)

        poll = await self.bot.send_message(ctx.message.channel, embed=e)
        for emoji, _ in choices:
            await self.bot.add_reaction(poll, emoji)

    @commands.command(no_pm=True, pass_context=True)
    async def quickpoll(self, ctx, *, question: str):
        """
        Quick and easy yes/no poll, for multiple answers, see !quickpoll
        """
        author = ctx.message.author.name.replace('_', '\_').replace('~', '\~').replace('|', '\|').replace('*', '\*')
        message = "**{}** asks: {}".format(author, question)
        embed = discord.Embed(title=':newspaper: ' +message, color=discord.Color.green())
        msg = await self.bot.send_message(ctx.message.channel, embed=embed)
        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass

        yes_thumb = "👍"
        no_thumb = "👎"
        shrug_emoji = "🤷"
        await self.bot.add_reaction(msg, yes_thumb)
        await self.bot.add_reaction(msg, shrug_emoji)
        await self.bot.add_reaction(msg, no_thumb)


def setup(bot):
    bot.add_cog(Polls(bot))
