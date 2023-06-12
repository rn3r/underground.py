import websockets
import json
import asyncio

class GatewayClient:
    def __init__(self, uri):
        self.websocket = None
        self.uri = uri
        self.ping_interval = 30000

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def disconnect(self):
        await self.websocket.close()

    async def receive(self):
        return await self.websocket.recv()

    async def send(self, message):
        await self.websocket.send(message)

    async def start_ping(self):
        while True:
            await self.send(json.dumps({
                "op": 1,
                "d": 251
            }))
            await asyncio.sleep(self.ping_interval / 1000)
