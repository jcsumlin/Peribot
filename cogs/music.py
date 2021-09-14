import asyncio
import datetime
import math
import re

import discord
import youtube_dl
from discord.ext import commands, tasks
from youtubesearchpython import VideosSearch

from cogs.utils.Song import Song
from cogs.utils.VoiceState import VoiceState
from cogs.utils.YouTubeVideo import YouTubeVideo

youtube_dl.utils.bug_reports_message = lambda: ''


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
        self.check_voice_state.start()

    def cog_unload(self):
        self.check_voice_state.cancel()

    @tasks.loop(seconds=60)
    async def check_voice_state(self):
        for state in self.voice_states.values():
            if state.is_playing and len(state.voice.channel.members) == 1:
                await state.stop()
                await state.leave_due_to_inactivity()


    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.peribot_voice_state = self.get_voice_state(ctx)

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @tasks.loop(seconds=3.0)
    async def vc_checker(self):
        await self.bot.wait_until_ready()
        vcs = self.bot.voice_clients
        for vc in vcs:
            member_count = len(vc.members)
            if member_count == 1:
                vc.disconnect()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            msg = await ctx.send(":x: You must be in a voice channel to use this command")
            await msg.delete(delay=5)
            return False

        destination = ctx.author.voice.channel
        if ctx.peribot_voice_state.voice:
            await ctx.peribot_voice_state.voice.move_to(destination)
            return True

        ctx.peribot_voice_state.voice = await destination.connect()
        return True

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice is None:
            msg = await ctx.send(":x: You must be in a voice channel to use this command")
            return await msg.delete(delay=5)

        if ctx.peribot_voice_state is None:
            return await ctx.send(":x: I'm not in a voice channel!")

        await ctx.peribot_voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command()
    async def queue(self, ctx, *, page: int = 1):
        if len(ctx.peribot_voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.peribot_voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.peribot_voice_state.songs[start:end], start=start):
            queue += f'`{i+1}.` [**{song.video.title}**]({song.video.link})\n'

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.peribot_voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.peribot_voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.peribot_voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    async def send_currently_playing_message(self, title, url, thumbnail, ctx: discord.ext.commands.Context):
        embed = discord.Embed(
            title=f":musical_note: **Now Playing** {title} :musical_note:",
            description=f"Added by {ctx.author.mention}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    async def get_source(self, video: YouTubeVideo):
        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed  1 -reconnect_delay_max 5",
            "options": "-vn"
        }
        source = await discord.FFmpegOpusAudio.from_probe(video.link, **FFMPEG_OPTIONS)
        return source

    @commands.command()
    async def play(self, ctx, *, url: str):
        if not ctx.peribot_voice_state.voice:
            success = await ctx.invoke(self.join)
            if not success:
                return


        YDL_OPTIONS = {
            "format": "bestaudio",
            'extractaudio': True,
            'audioformat': 'mp3',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
        }
        async with ctx.typing():
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                if self.youtube_url_validation(url):
                    info = ydl.extract_info(url, download=False)
                    video = YouTubeVideo(info["title"], info["formats"][0]["url"], info["thumbnail"], ctx.author)
                else:
                    videosSearch = VideosSearch(url, limit=1)
                    result = videosSearch.resultComponents[0]
                    info = ydl.extract_info(result["link"], download=False)
                    video = YouTubeVideo(result["title"], info["formats"][0]["url"], result["thumbnails"][0]["url"], ctx.author)
                source = await self.get_source(video)
                source.channel = ctx.channel
                song = Song(video, source)
                await ctx.peribot_voice_state.songs.put(song)
                await ctx.send(f'Enqueued {song.video.title}')

    @commands.command()
    async def skip(self, ctx):
        if not ctx.peribot_voice_state.is_playing:
            return await ctx.send(':x: Not playing any music right now...')
        ctx.peribot_voice_state.skip()
        await ctx.send("<a:check:806712532249214976> Skipped!")

    def youtube_url_validation(self, url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            return youtube_regex_match

        return youtube_regex_match


def setup(bot):
    bot.add_cog(Music(bot))
