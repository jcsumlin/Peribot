from configparser import ConfigParser

import requests

import discord
from discord.ext import commands


class TTT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_servers = [540580897959968781]
        auth = ConfigParser()
        auth.read('../auth.ini')
        self.api_key = auth.get("TTTAPI", "API_KEY")

    @commands.group(name="ttt")
    async def ttt(self, ctx):
        if ctx.guild.id not in self.allowed_servers:
            return
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a status [start, stop]")

    async def query_api(self, endpoint):
        url = "https://ji5vy5feva.execute-api.us-east-1.amazonaws.com/prod/" + endpoint
        headers = {
            'x-api-key': self.api_key
        }
        return requests.request("POST", url, headers=headers)

    @ttt.command()
    async def start(self, ctx):
        response = await self.query_api("start")
        if response.status_code == 200:
            embed = discord.Embed(title="Server Started!", description="**Public IP Address:** 44.194.75.109", color=discord.Color.green())
        else:
            embed = discord.Embed(title="Failed to start server", description=response.text, color=discord.Color.red())
        await ctx.send(embed=embed)

    @ttt.command()
    async def stop(self, ctx):
        response = await self.query_api("stop")
        if response.status_code == 200:
            embed = discord.Embed(title="Server Stopped!",color=discord.Color.green())
        else:
            embed = discord.Embed(title="Failed to stop server", description=response.text, color=discord.Color.red())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TTT(bot))
