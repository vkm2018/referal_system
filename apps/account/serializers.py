from rest_framework import serializers

from apps.account.models import User


class PhoneSerializer(serializers.Serializer):
    number_phone = serializers.CharField(max_length=15)

class CodeSerializer(serializers.Serializer):
    number_phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)


class UserProfileSerializer(serializers.ModelSerializer):
    activated_invite_code = serializers.CharField(read_only=True)


    class Meta:
        model = User
        fields = '__all__'
