import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            print(self.channel_name)
            # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            self.group_name = str(self.scope["user"].pk)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    async def recieve(self, text_data):

        self.send(text_data=json({
            'message': message
        }))

    async def notification_sender(self, event):
        """When received a message from a notification."""
        payload = event["payload"]
        await self.send(text_data=json.dumps(payload))
