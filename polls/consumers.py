from fileinput import close
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.generic.websocket import WebsocketConsumer
from celery.result import AsyncResult


def get_task_info(task_id):
    """
    return task information according to task_id
    """
    task = AsyncResult(task_id)
    if task.state == 'FAILURE':
        error = str(task.result)
        reponse = {
            'state': task.state,
            'error': error,
        }
    else:
        response = {
            'state': task.state,
        }
    return response

def notify_channel_layer(task_id):
    """
    This function would be call in the Celery task.

    Since Celery now still does not support 'asyncio', so we should 
    use async_to_sync to make it synchronous.
    """

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        task_id,
        {'type': 'update_task_status', 'data': get_task_info(task_id)}
    )

# # Basic Websocket Consumers
# class TaskStatusConsumer(WebsocketConsumer):
#     def connect(self):
#         self.task_id = self.scope['url_route']['kwargs']['task_id']

#         async_to_sync(self.channel_layer.group_add)(
#             self.task_id,
#             self.channel_name
#         )

#         self.accept()

#         self.send(text_data=json.dumps(get_task_info(self.task_id)))

#     def disconnet(self, close_code):
#         async_to_sync(self.channel_layer.group_discard(
#             self.task_id,
#             self.channel_name
#         ))

#     def update_task_status(self, event):
#         data = event['data']

#         self.send(text_data=json.dumps(data))

# Advanced high proformance (high tolerant) async Websocket Consumers
class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']

        await self.channel_layer.group_add(
            self.task_id,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps(get_task_info(self.task_id)))
    
    async def disconnet(self, close_code):
        await self.channel_layer.group_discard(
            self.task_id,
            self.channel_name
        )
    
    async def update_task_status(self, event):
        data = event['data']

        await self.send(text_data=json.dumps(data))
