
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class UpdateJWT(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room_name']
        self.id = self.room
        self.perodical = asyncio.create_task(self.send_periodic_updates())
        await self.accept()

    async def disconnect(self, code):
        self.perodical.cancel()
        await self.perodical

    async def send_periodic_updates(self):
        try:
            while True:
                # Lakukan operasi yang diperlukan untuk memperbarui database atau aktivitas lainnya
                await sync_to_async(self.update_periodic_data)()

                await self.send(text_data=json.dumps({
                    'message': self.jwtdata
                }))

                # Tunggu selama 10 menit sebelum mengulang
                await asyncio.sleep(3)  # 600 detik = 10 menit

        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f'Periodic update failed: {str(e)}'
            }))

    def update_periodic_data(self):
        try:
            if self.id:
                # Verifikasi user berdasarkan email
                user = User.objects.get(id=self.id)

                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                respon = {
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'user_id': user.id,
                    'message': status.HTTP_200_OK
                }

                self.jwtdata = respon
            else:
                self.jwtdata = {'message': 'ID not found'}
        except Exception as e:
            self.jwtdata = {'message': 'Error updating data'}
