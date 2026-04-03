import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):

    # ── DB helpers (must wrap all ORM calls) ──────────────────────────────────

    @database_sync_to_async
    def get_user_role(self, user):
        """Fetch profile.role safely from async context."""
        return user.profile.role  # DB hit — must be wrapped

    # ── Connect ───────────────────────────────────────────────────────────────

    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close(code=4001)  # 4001 = our "unauthorized" code
            return

        # ✅ Use sync_to_async wrapper for DB call
        role = await self.get_user_role(user)

        # 👤 Personal user group — every user joins this
        self.user_group = f"user_{user.id}"
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        # 👑 Admin group — only admins join this
        if role == "ADMIN":
            self.admin_group = "admins"
            await self.channel_layer.group_add(
                self.admin_group,
                self.channel_name
            )

        await self.accept()

    # ── Disconnect ────────────────────────────────────────────────────────────

    async def disconnect(self, close_code):
        # Always clean up user group
        if hasattr(self, "user_group"):
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )

        # Clean up admin group if joined
        if hasattr(self, "admin_group"):
            await self.channel_layer.group_discard(
                self.admin_group,
                self.channel_name
            )

    # ── Receive (optional — handle messages from frontend if needed) ──────────

    async def receive(self, text_data=None, bytes_data=None):
        pass  # This consumer is push-only (server → client)

    # ── Handler — called by channel_layer.group_send ──────────────────────────

    async def send_notification(self, event):
        """
        Called when someone does:
            channel_layer.group_send("user_<id>", {
                "type": "send_notification",
                "message": "Your order has been shipped!"
            })
        """
        await self.send(text_data=json.dumps({
            "type":    "notification",
            "message": event["message"]
        }))