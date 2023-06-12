from underground.context import Context
import json
import discord

class DictObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictObject(value))
            else:
                setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)

class JSON:
    def __init__(self):
        pass

    def parse(json):
        return DictObject(json)

class UserClient:
    def __init__(self, token):
        self.token = token
        self.session = None
        self.user_cache = []
        self.guild_cache = []
        self.commands = {}
        self.prefix = "!"

    def command(self, name):
        def decorator(func):
            self.commands[name] = func
            return func
        return decorator
    
    def combine_args(self, args):
        combined_args = [args[0]]
        quote_buffer = None

        args = args[1:]

        for arg in args:
            if quote_buffer is None:
                if arg.startswith('"'):
                    quote_buffer = arg[1:]
                else:
                    combined_args.append(arg)
            else:
                if arg.endswith('"'):
                    combined_args.append(quote_buffer + ' ' + arg[:-1])
                    quote_buffer = None
                else:
                    quote_buffer += ' ' + arg

        return combined_args
        
    async def event_handler(self, event):
        if event["t"] == "MESSAGE_CREATE" and event["d"].get("content", "NoneType").startswith(self.prefix):
            context = Context(client=self)
            context.channel_id = event["d"]["channel_id"]
            context.guild_id = event["d"]["guild_id"]
            context.message = JSON.parse(event["d"])

            command = event["d"]["content"][len(self.prefix):].split(" ")[0]
            args = [context, *event["d"]["content"].split(" ")[1:]]
            args = self.combine_args(args)

            try:
                await self.commands[command](*args)
            except Exception as e:
                await context.reply(embed=discord.Embed(description=f"Error: {e}", color=0xff0000))

    async def recieve_events(self, gateway, client):
        print("Sending IDENTIFY")
        identify = json.dumps({
            "op":2,
            "d":{
                "token": client.token,
                "capabilities":509,
                "properties":{
                    "os":"Windows",
                    "browser":"Chrome",
                    "device":"",
                    "system_locale":"en-US",
                    "browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
                },
                "compress":False,
                "presence":{
                    "status":"online",
                    "since":0,
                    "activities":[],
                    "afk":False
                }
            }
        })

        await gateway.send(identify)
        gateway.sequence = 0

        while True:
            try:
                message = await gateway.receive()
            except Exception as e:
                print("Resuming connection...")
                await gateway.connect(gateway.uri)
                await gateway.send(json.dumps({
                    "op": 6,
                    "d":{
                        "token": client.token,
                        "session_id": client.session,
                        "seq": gateway.sequence
                    }
                }))
                continue

            try:
                event = json.loads(message)
                gateway.sequence = event.get("s", gateway.sequence)

                if event.get("t") == "READY":
                    with open("ready.json", "w") as f:
                        f.write(json.dumps(event, indent=4))

                    client.user = JSON.parse(event["d"]["user"])
                    client.session = event["d"]["session_id"]

                    print("Logged into ", client.user.username, "#", client.user.discriminator, "\nSession ID: ", client.session, sep="")

                    continue
                
                if event["op"] == 0:
                    await client.event_handler(event)
                    continue

                if event["op"] == 10:
                    if event["d"].get("heartbeat_interval"):
                        gateway.ping_interval = event["d"]["heartbeat_interval"]

            except Exception as e:
                print(e)
                continue
