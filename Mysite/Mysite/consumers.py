import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile

from Home.models import Room,Message,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        room_name = text_data_json.get("room_name")
        image_data = text_data_json.get("image")  # Nhận ảnh từ dữ liệu
        
        await self.save_message(message, username, room_name, image_data)     

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "send_message",
                "message": message,
                "username": username,
                "room_name": room_name,
                "image_data": image_data,  # Truyền ảnh khi gửi tin nhắn đi
            }
        )
        
    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        image_data = event.get("image_data")  # Lấy ảnh từ dữ liệu event
        await self.send(text_data=json.dumps({"message": message, "username": username, "image_data": image_data}))
    
    @sync_to_async
    def save_message(self, message, username, room_name, image_data):
        print(username, room_name, "----------------------")
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        new_message = Message.objects.create(user=user, room=room, content=message)
        
        # Xử lý và lưu ảnh nếu có
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"{room_name}-{username}-image.{ext}")
            new_message.image.save(f"{room_name}-{username}-image.{ext}", image_data, save=True)
