# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async


# class OrderConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
#         self.group_name = f"order_{self.order_id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()


#     async def disconnect(self, close_code):

#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )


#     async def order_update(self, event):

#         await self.send(text_data=json.dumps({
#             "order_id": event["order_id"],
#             "status": event["status"]
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        user = self.scope["user"]
        print(" websocket userr-------------------------------------")

        # Reject connection if user not authenticated
        if user.is_anonymous:
            await self.close()
            return

        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.group_name = f"order_{self.order_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    async def order_update(self, event):

        await self.send(text_data=json.dumps({
            "order_id": event["order_id"],
            "status": event["status"]
        }))