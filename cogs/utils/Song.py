import discord

from cogs.utils.YouTubeVideo import YouTubeVideo


class Song:

    def __init__(self, video: YouTubeVideo, source: discord.FFmpegOpusAudio):
        self.video = video
        self.requester = video.requester
        self.source = source

    def create_embed(self):
        embed = (discord.Embed(title=':musical_note: Now playing :musical_note:',
                               description=f'```css\n{self.video.title}\n```',
                               color=discord.Color.blurple())
                 .add_field(name='Requested by', value=self.requester.mention, inline=False)
                 .add_field(name='URL', value=f'[Click]({self.video.link})', inline=False)
                 .set_thumbnail(url=self.video.thumbnail))

        return embed
