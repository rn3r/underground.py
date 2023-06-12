import asyncio
import discord
from underground.gateway.ws import GatewayClient
from underground.gateway.client import UserClient
import json

async def main(client):
    gateway = GatewayClient("wss://underground.haydar.dev/?encoding=json&v=9")
    await gateway.connect()

    task1 = asyncio.create_task(client.recieve_events(gateway, client))
    task2 = asyncio.create_task(gateway.start_ping())

    await asyncio.gather(task1, task2)

client = UserClient("UNDERGROUND_CLIENT_TOKEN")

@client.command("help")
async def help(ctx):
    await ctx.send("https://underground.haydar.dev/invite/i", embed=discord.Embed(description=">>> ```bf\n!reply <message>\n```", color=0x000000))

@client.command("reply")
async def reply(ctx, message):
    await ctx.reply(embed=discord.Embed(title="Reply", description=message, color=0x00ff00))


asyncio.run(main(client))
