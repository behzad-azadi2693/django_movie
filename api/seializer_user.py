from accounts.views import phone
from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()