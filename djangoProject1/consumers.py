import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data['profileId']
        is_online = data['is_active']

        await self.channel_layer.group_send(
            'online_users_group',
            {
                'type': 'user_status',
                'user_id': user_id,
                'is_online': is_online
            }
        )

    async def user_status(self, event):
        user_id = event['profileId']
        is_online = event['is_active']

        # Відправка повідомлення про онлайн статус користувача на клієнт
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'is_online': is_online
        }))


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        post = data.copy()

        await self.channel_layer.group_send(
            'posts_group',
            {
                'type': 'post_message',
                'post': post
            }
        )

    async def post_message(self, event):
        post_id = event['identifier']

        await self.send(text_data=json.dumps({
            'post_message': post_id
        }))