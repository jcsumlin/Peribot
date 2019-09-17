import os
import re

import discord
from discord.ext import commands
from loguru import logger

from .utils.dataIO import dataIO, fileIO


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_config(self):
        return dataIO.load_json('data/youtube/playlist.json')

    async def save_config(self, data):
        return dataIO.save_json('data/youtube/playlist.json', data)

    async def server_in_config(self, servers, id):
        if id in servers.keys():
            return True
        else:
            return False

    @commands.group('youtube', pass_context=True)
    async def youtube(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Thats not how you use this command, please do it like this. !youtube add [link]")
            return

    @youtube.group(pass_context=True)
    async def add(self, ctx, link):
        youtube_url_regex = "(http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?)"
        regex = re.findall(youtube_url_regex, link)
        if len(regex) > 0 and "youtube.com" in regex[0][0] or "youtu.be" in regex[0][0]:
            servers = await self.get_config()
            if await self.server_in_config(servers, ctx.message.guild.id):
                if ctx.message.author.id not in servers[ctx.message.guild.id]:
                    servers[ctx.message.guild.id][ctx.message.author.id] = []
                if len(servers[ctx.message.guild.id][ctx.message.author.id]) < 3 and regex[0][0] not in servers[ctx.message.guild.id][ctx.message.author.id]:
                    servers[ctx.message.guild.id][ctx.message.author.id].append(regex[0][0])
                    await ctx.send("Added!")
                else:
                    await ctx.send("Sorry! Either you already added that link or you've hit your max of 3 links!")
            else:
                servers[ctx.message.guild.id] = {ctx.message.author.id: [regex[0][0]]}
                await ctx.send("Added!")

            await self.save_config(servers)
        else:
            await ctx.send("Sorry that doesn't seem to be a valid Youtube link!")

    @youtube.group(pass_context=True)
    async def list(self, ctx):
        server_object = ctx.message.guild
        server = await self.get_config()
        e = discord.Embed(title=f'{server_object.name}\'s Member Playlist', color=discord.Color.red())
        e.set_thumbnail(url="https://seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png")
        for user in list(server[server_object.id].keys()):
            user = await self.bot.get_user_info(user_id=user)
            if len(server[server_object.id][user.id]) != 0:
                songs = '\n'.join(server[server_object.id][user.id])
            else:
                songs = "None"
            e.add_field(name=f"{user}'s songs:", value=songs)
        await ctx.send(embed=e)

    @youtube.group(pass_context=True)
    async def delete(self,ctx,  link):
        config = await self.get_config()
        server_config = config[ctx.message.guild.id]
        if ctx.message.author.id in server_config.keys():
            if link in server_config[ctx.message.author.id]:
                server_config[ctx.message.author.id].remove(link)
                await self.save_config(config)
                await ctx.send("Removed!")
            else:
                await ctx.send("Hm I don't think that link was in there to begin with... try adding it?")
        else:
            await ctx.send("Doesn't look like you've added any youtube links.. try adding one!")

def check_folders():
    if not os.path.exists("data/youtube"):
        logger.info("Creating data/youtube folder...")
        os.makedirs("data/youtube")

def check_files():
    f = "data/youtube/playlist.json"
    if not fileIO(f, "check"):
        logger.info("Creating empty youtube.json...")
        fileIO(f, "save", {})

def setup(bot):
    check_folders()
    check_files()
    n = Youtube(bot)
    bot.add_cog(n)
