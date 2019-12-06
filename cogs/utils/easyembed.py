import discord

def embed(title="", description="", image=None, color=discord.Embed.Empty):
    embed = discord.Embed(title=title, description=description,color=color)
    if image:
        embed.set_image(url=image)
    return embed

def command_error(operation, description):
    return discord.Embed(title="Error: " + operation, description=description, color=discord.Color.red())

def command_success(operation, description):
    return discord.Embed(title="Success!: " + operation, description=description, color=discord.Color.green())
