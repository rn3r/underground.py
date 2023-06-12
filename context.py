import requests
import discord

class Context:
    def __init__(self, client):
        self.client = client
        self.channel_id = None
        self.guild_id = None
        self.message = None

    async def send(self, content=None, embed=None, tts=False):
        if not self.channel_id:
            raise Exception("Channel ID not set")
        
        if isinstance(embed, discord.Embed):
            embed = embed.to_dict()
        
        req = requests.post(f"https://underground.haydar.dev/api/v9/channels/{self.channel_id}/messages", 
                            json={
                                "content": content,
                                "embed": embed,
                                "tts": tts
                            }, 
                            headers={
                                "authorization": f"{self.client.token}"
                            }
        )
        return req
    
    async def reply(self, content=None, embed=None, tts=False):
        if not self.channel_id:
            raise Exception("Channel ID not set")
        
        if not self.message:
            raise Exception("Message not set")
        
        if isinstance(embed, discord.Embed):
            embed = embed.to_dict()
        
        reference = {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_id": self.message.id
        }

        if reference["guild_id"] == None:
            del reference["guild_id"]
        

        req = requests.post(f"https://underground.haydar.dev/api/v9/channels/{self.channel_id}/messages", 
                            json={
                                "content": content,
                                "embed": embed,
                                "tts": tts,
                                "message_reference": reference
                            }, 
                            headers={
                                "authorization": f"{self.client.token}"
                            }
        )
        return req
