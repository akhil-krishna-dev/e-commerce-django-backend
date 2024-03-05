import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class OrderUpdate(AsyncWebsocketConsumer):

    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'order_updates_{user_id}'
        self.channel_layer = get_channel_layer()

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            "type":"init",
            "message":"connected"
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("message in consu ",message)
        print("group name ",self.group_name)
        
        if message == 'this is ok':
            await self.send(text_data=json.dumps({
                'message':'successfull'
            }))

        if message == 'order updated':
            print("message in consu ",message)
            await self.send(text_data=json.dumps({
                'message': 'Order updated acknowledgment'
            }))


    async def send_update_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type':'order_update',
            'message':message
        }))

    
    