import time
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import string
import random
from redis import Redis
from apps.account.models import User
from apps.account.serializers import PhoneSerializer, CodeSerializer

redis = Redis(host='localhost', port=6379, db=0)

def create_invite_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class CodeView(APIView):

    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            number_phone = serializer.validated_data['number_phone']
            code = f'{random.randint(1000, 9999)}'
            redis.set(number_phone, code, ex=300)
            time.sleep(1)
            print(code)
            context = {'code': code,
                       'number_phone': number_phone}
            return render(request, 'number_phone.html', context)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):

    def get(self, request):
        return render(request, 'profile.html')

    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = create_invite_code()
            number_phone = serializer.validated_data['number_phone']
            code = serializer.validated_data['code']
            save_code = redis.get(number_phone)
            if save_code and save_code.decode() == code:
                try:
                    user = User.objects.get(number_phone=number_phone)
                    return redirect('profile', number_phone=user.number_phone)

                except:
                    user = User.objects.create(number_phone=number_phone, activate_invite_code=invite_code)
                    context = {
                               'number_phone': number_phone}
                    return render(request, 'profile.html', context)

            return Response({'message': 'Неверный код'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):

    def get(self, request,number_phone):
            user = User.objects.get(number_phone=number_phone)
            users = User.objects.filter(invite_code=user.activate_invite_code)
            serialized_users = [{'id': invitee.id, 'number_phone': invitee.number_phone} for invitee in users]
            context = {'user': user,
                       'users': users}


            return render(request, 'profile.html', context)

    def post(self, request, number_phone):
        try:
            user = User.objects.get(number_phone=number_phone)
            invite_code = request.data.get("invite_code")

            if not invite_code:
                return Response({"error": "Код приглашения обязателен."}, status=status.HTTP_400_BAD_REQUEST)

            if user.invite_code:
                return Response({"error": "Код приглашения уже активирован."}, status=status.HTTP_400_BAD_REQUEST)

            inviter = User.objects.filter(activate_invite_code=invite_code).first()
            if not inviter:
                return Response({"error": "Код приглашения не существует."}, status=status.HTTP_404_NOT_FOUND)

            user.invite_code = invite_code
            user.save()

            return Response({"message": "Код приглашения успешно активирован."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)