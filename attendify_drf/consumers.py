# your_app_name/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('broadcast', self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('broadcast', self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages from the WebSocket if needed
        pass

    async def send_event(self, event):
        await self.send(text_data=json.dumps({
            'event': event['event'],
            'data': event['data'],
        }))
