import datetime

import discord
from discord.ext import commands
from loguru import logger

from .utils.checks import admin_or_permissions
from .utils.DailyGames import DailyGamesModel
from .utils.dailygame_parser import parse_game_message
from .utils.genericResponseBuilder import commandError, commandSuccess

MEDALS = ["🥇", "🥈", "🥉"]


def format_mode(game, mode):
    return f"{game} ({mode.title()})" if mode else game


class DailyGames(commands.Cog):
    """Tracks Wordle-like daily game results posted in a channel"""

    def __init__(self, bot):
        self.bot = bot
        self.model = DailyGamesModel()
        # Cached so every message doesn't hit the database
        self.channel_ids = self.model.get_all_channel_ids()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await commandError(ctx, "You need to be an administrator to do that.")
        elif isinstance(error, commands.BadArgument):
            await commandError(ctx, str(error))
        elif isinstance(error, commands.NoPrivateMessage):
            await commandError(ctx, "This command can only be used in a server.")

    @commands.group(aliases=["dg", "dailygame"], invoke_without_command=True)
    @commands.guild_only()
    async def dailygames(self, ctx):
        """Commands for tracking daily game results"""
        await commandError(ctx, "Thats not how you use this command.\n"
                                f"**{ctx.prefix}dailygames track [channel]**\nStart tracking daily game results in a channel (admin)\n"
                                f"**{ctx.prefix}dailygames untrack [channel]**\nStop tracking a channel (admin)\n"
                                f"**{ctx.prefix}dailygames channels**\nList the channels being tracked\n"
                                f"**{ctx.prefix}dailygames leaderboard [game] [mode]**\nShow the leaderboards\n"
                                f"**{ctx.prefix}dailygames stats [member]**\nShow a member's stats\n")

    @dailygames.command(name="track", aliases=["add", "monitor"])
    @admin_or_permissions()
    async def track_channel(self, ctx, channel: discord.TextChannel = None):
        """Start tracking daily game results in a channel"""
        channel = channel or ctx.channel
        if not await self.model.add_channel(ctx.guild.id, channel.id, ctx.author.id):
            return await commandError(ctx, f"I'm already tracking daily games in {channel.mention}!")
        self.channel_ids.add(channel.id)
        await self.model.audit_record(ctx.guild.id, ctx.guild.name, ctx.message.content, ctx.author.id)
        message = f"I'm now tracking daily game results posted in {channel.mention}."
        if not channel.permissions_for(ctx.guild.me).manage_messages:
            message += "\n⚠️ I need the **Manage Messages** permission there to replace results with embeds."
        await commandSuccess(ctx, message)

    @dailygames.command(name="untrack", aliases=["stop", "remove"])
    @admin_or_permissions()
    async def untrack_channel(self, ctx, channel: discord.TextChannel = None):
        """Stop tracking daily game results in a channel"""
        channel = channel or ctx.channel
        if not await self.model.remove_channel(channel.id):
            return await commandError(ctx, f"I'm not tracking daily games in {channel.mention}.")
        self.channel_ids.discard(channel.id)
        await self.model.audit_record(ctx.guild.id, ctx.guild.name, ctx.message.content, ctx.author.id)
        await commandSuccess(ctx, f"I've stopped tracking daily game results in {channel.mention}. "
                                  f"Existing scores are kept on the leaderboard.")

    @dailygames.command(name="channels")
    async def list_channels(self, ctx):
        """List the channels being tracked"""
        channels = await self.model.get_channels(ctx.guild.id)
        if not channels:
            return await ctx.send(f"No channels are being tracked. "
                                  f"An admin can use **{ctx.prefix}dailygames track [channel]** to start.")
        embed = discord.Embed(title="Daily game channels",
                              description="\n".join(f"<#{c.channel_id}>" for c in channels),
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @dailygames.command(name="leaderboard", aliases=["lb", "top"])
    async def leaderboard(self, ctx, game: str = None, mode: str = None):
        """Show the leaderboards, optionally for a single game and mode"""
        game_modes = await self.model.get_game_modes(ctx.guild.id, game, mode)
        if not game_modes:
            return await commandError(ctx, "No results have been recorded yet!" if game is None
                                      else f"No results have been recorded for **{game}** yet!")
        # Show a full top 10 when looking at a single board, otherwise a top 3 for each
        limit = 10 if len(game_modes) == 1 else 3
        embed = discord.Embed(title="Daily Games Leaderboard", color=discord.Color.gold())
        embed.set_footer(text="Ranked by average number of guesses (lower is better)")
        for game_name, game_key, game_mode in game_modes[:25]:
            rows = await self.model.get_leaderboard(ctx.guild.id, game_key, game_mode, limit=limit)
            lines = []
            for rank, row in enumerate(rows):
                place = MEDALS[rank] if rank < len(MEDALS) else f"**{rank + 1}.**"
                lines.append(f"{place} <@{row.user_id}> — **{row.average:.2f}** avg "
                             f"({row.played} played, best {row.best})")
            embed.add_field(name=format_mode(game_name, game_mode), value="\n".join(lines), inline=False)
        await ctx.send(embed=embed)

    @dailygames.command(name="stats")
    async def stats(self, ctx, member: discord.Member = None):
        """Show a member's daily game stats"""
        member = member or ctx.author
        stats = await self.model.get_user_stats(ctx.guild.id, member.id)
        if not stats:
            return await commandError(ctx, f"{member.display_name} hasn't posted any daily game results yet!")
        embed = discord.Embed(title=f"{member.display_name}'s daily game stats", color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        for row in stats[:25]:
            embed.add_field(name=format_mode(row.game, row.mode),
                            value=f"Played: **{row.played}**\n"
                                  f"Solved: **{row.solved}**\n"
                                  f"Average: **{row.average:.2f}**\n"
                                  f"Best: **{row.best}**")
        await ctx.send(embed=embed)

    def build_result_embed(self, author: discord.Member, result):
        embed = discord.Embed(title=f"{result.game} #{result.number}",
                              url=result.url or discord.Embed.Empty,
                              description=result.grid[:2048] or discord.Embed.Empty,
                              color=discord.Color.green() if result.solved else discord.Color.red(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        if result.mode:
            embed.add_field(name="Mode", value=result.mode.title())
        embed.add_field(name="Score" if result.max_attempts else "Shots", value=result.score_display)
        if result.difficulty:
            embed.add_field(name="Difficulty", value=result.difficulty.title())
        return embed

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None or message.channel.id not in self.channel_ids:
            return
        result = parse_game_message(message.content)
        if result is None:
            return

        can_delete = message.channel.permissions_for(message.guild.me).manage_messages
        if await self.model.get_result(message.guild.id, message.author.id, result) is not None:
            await message.channel.send(f"{message.author.mention} you've already posted "
                                       f"{format_mode(result.game, result.mode)} #{result.number}!",
                                       delete_after=10)
            if can_delete:
                await message.delete()
            return

        try:
            await self.model.add_result(message.guild.id, message.channel.id, message.author.id, result)
        except Exception as e:
            logger.exception(f"Could not save daily game result: {e}")
            self.model.session.rollback()
            return

        await message.channel.send(embed=self.build_result_embed(message.author, result))
        if can_delete:
            try:
                await message.delete()
            except discord.HTTPException as e:
                logger.error(f"Could not delete daily game message {message.id}: {e}")


def setup(bot):
    bot.add_cog(DailyGames(bot))
