import discord
from underground.gateway.ws import GatewayClient
from underground.gateway.client import UserClient
import json

with open("./config.json", "r") as f:
    config = json.load(f)

client = UserClient(config["token"], prefix="!")

@client.command("help")
async def help(ctx):
    await ctx.send("https://underground.haydar.dev/invite/i", embed=discord.Embed(description="Want to contribute to this open source project? Feel free to make a pull request at https://github.com/rn3r/underground.py\n>>> ```bf\n!reply <message>\n```", color=0x000000))

@client.command("reply")
async def reply(ctx, message):
    await ctx.reply(embed=discord.Embed(title="Reply", description=message, color=0x00ff00))

@client.command("invite")
async def invite(ctx):
    await ctx.send(embed=discord.Embed(title="Invite me to your server", description="support: https://underground.haydar.dev/invite/i\nhttps://underground.haydar.dev/api/oauth2/authorize?client_id=1117555508107436742&permissions=8&scope=bot", color=0x000000))

client.run()
