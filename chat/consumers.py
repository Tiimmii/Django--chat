import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from chat.models import Thread, Chatmessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):     
        user = self.scope['user']
        room_group_name = f'user_chatroom_{user.id}'
        self.room_group_name = room_group_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type':'tester_message',
            'message': 'connected successfully'
            }
        )
        print("connected")

    async def tester_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))



    async def receive(self, text_data):
        text = json.loads(text_data)
        message = text['message']
        sent_by_id = text['sent_by']
        sent_to_id = text['sent_to']
        thread_id = text['thread_id']
        print(thread_id)

        sent_by_user = await self.get_user_object(sent_by_id)
        sent_to_user = await self.get_user_object(sent_to_id)
        thread_obj = await self.get_thread_object(thread_id)

        if not sent_by_user:
            print("sent by user not correct")
        if not sent_to_user:
            print("Send to user not correct")
        if not thread_obj:
            print("thread not correct")

        await self.create_chat_message(thread_obj, sent_by_user, message)
        # time = await self.message_checker(message)
        # print(time)

        other_user_chat_room = f'user_chatroom_{sent_to_id}'
        self_user = self.scope['user']

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
            'type': 'chat_message',
            'message':message,
            'sent_by': self_user.id,
            'thread_id': thread_id,
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message':message,
            'sent_by': self_user.id,
            'thread_id': thread_id,
            }
        )
        print('message:', message)

    async def chat_message(self, event):
        message = event['message']
        sent_by = event['sent_by']
        thread_id = event['thread_id']
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sent_by': sent_by,
            'thread_id':thread_id,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
    
    @database_sync_to_async
    def get_thread_object(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        print(qs)
        if qs.exists():
            obj = qs.first()
            print(obj)
        else:
            obj = None
        return obj
    
    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        Chatmessage.objects.create(thread=thread, user=user, message=msg)
    
    @database_sync_to_async
    def message_checker(self, msg):
        qs = Chatmessage.objects.filter(message=msg).values_list('timestamp')
        return qs.first()

