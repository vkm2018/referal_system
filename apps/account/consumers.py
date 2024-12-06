import django
from channels.generic.websocket import WebsocketConsumer
import json
from django.template.loader import get_template
django.setup()
from apps.account.models import User


class InviteCodeConsumer(WebsocketConsumer):
    def connect(self):
            self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
            data = json.loads(text_data)
            invite_code_data = data.get('invite_code')
            activate_invite_code = data.get('activate_invite_code')
            user = User.objects.get(activate_invite_code=activate_invite_code)
            if not invite_code_data:
                response = {
                    'message': 'Введите инвайт код',
                    'status': 'error'
                        }
            if user.invite_code:
                response = {
                    'message': 'инвайт код уже актвирован',
                    'status': 'error'
                }
            try:
                user = User.objects.get(activate_invite_code=activate_invite_code)
            except:
                response = {
                    'message': 'Пользователь с таким инвайт кодом не найден',
                    'status': 'error'
                }
                self.send(text_data=json.dumps(response))
                return
            else:
                user.invite_code = invite_code_data
                user.save()
                response = {
                    'message': 'Инвайт код успешно активирован',
                    'status': 'success'
                }
            self.send(text_data=json.dumps(response))

