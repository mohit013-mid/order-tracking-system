import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        # 👤 user group
        self.user_group = f"user_{user.id}"
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        # 👑 admin group (using Profile)
        if user.profile.role == "ADMIN":
            self.admin_group = "admins"
            await self.channel_layer.group_add(
                self.admin_group,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group,
            self.channel_name
        )

        if hasattr(self, "admin_group"):
            await self.channel_layer.group_discard(
                self.admin_group,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"]
        }))