from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','profile_image')


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','password','password2')
    
    def validate(self, data):
        user_exist = User.objects.filter(email=data['email']).first()
        if user_exist:
            raise serializers.ValidationError("user already exist with this mail")

        if data['password'] != data['password2']:
            raise serializers.ValidationError("password and confirm password does not match")
        return data
    
    def create(self, validated_data):        
        user = User(
            email=validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],            
        )
        user.is_active = False
        user.set_password(validated_data['password'])
        user.save()

        return user

        


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserPasswordForgot(serializers.Serializer):
    email = serializers.EmailField()





