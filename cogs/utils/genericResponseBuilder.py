import discord


async def commandError(ctx, message):
    embed = discord.Embed(title="Command Error!", description=message, color=discord.Color.red())
    await ctx.send(embed=embed)


async def commandSuccess(ctx, message):
    embed = discord.Embed(title="Success!", description=message, color=discord.Color.green())
    await ctx.send(embed=embed)
