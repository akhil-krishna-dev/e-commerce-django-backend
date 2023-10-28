from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)