import discord


class YouTubeVideo:
    def __init__(self, title: str, link: str, thumbnail: str, requester: discord.Member):
        self.title = title
        self.link = link
        self.thumbnail = thumbnail
        self.requester = requester
