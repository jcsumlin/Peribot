import discord

def embed(title="", description="", image=None, color=discord.Embed.Empty):
    embed = discord.Embed(title=title, description=description,color=color)
    if image:
        embed.set_image(url=image)
    return embed

