from . import serializers
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserPasswordForgot
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:        
            serializer = serializers.UserProfileSerializer(request.user)
            return Response(data=serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(data={'message':'login required for shopping'})


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny,]

    def post(self,request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
    
            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            verification_url = f"http://localhost:3000/user/{uid}/email-verification/{token}/"
            
            subject = "Activate your account"
            message = verification_url
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )

            return Response({"message":"account created"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        
        uid = urlsafe_base64_decode(uidb64).decode()

        user = CustomUser.objects.filter(id=uid).first()
        token_generator = default_token_generator
        
        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            token = RefreshToken.for_user(user)
            data = {
                    "refresh":str(token),
                    "access":str(token.access_token)
                }
            return Response(data, status=status.HTTP_200_OK)
        
        return Response({"message":"Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.data['email']
            password = request.data['password']
            user = CustomUser.objects.filter(email=email).first()

            if not user:
                return Response(data={"message":"There is no account with this email"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if not user.is_active:
                data={'message':"account is not activated"}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.check_password(password):
                token = RefreshToken.for_user(user)
                data = {
                    "refresh":str(token),
                    "access":str(token.access_token)
                }
                return Response(data, status=status.HTTP_200_OK)
            
            return Response(data={"message":"password wrong"}, status=status.HTTP_401_UNAUTHORIZED)
                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class UserLogOut(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'message':"logout successful"
            }
            return Response(data, status=status.HTTP_200_OK)
        except KeyError:
            data = {
                'message':"refresh token required in the request"
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordForgotView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserPasswordForgot(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                data = {
                    'error':f"There is no account with {email}"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            
            reset_link = f"http://localhost:3000/user/reset-password/{uid}/{token}/"
            send_mail(
                "Reset your password",
                f"Click the link to reset your password {reset_link}",
                settings.EMAIL_HOST_USER,
                [email]                
            )

            data = {
                "success":"password reset link has been send to your email"
            }

            return Response(data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):        
        user_id = request.data['user_id']
        token = request.data['token']
        password = request.data['password']
        
        uid = urlsafe_base64_decode(user_id).decode()
        token_generator = default_token_generator

        try:
            user = CustomUser.objects.get(id = uid)
        except CustomUser.DoesNotExist:
            return Response({"message":"user not found"})
        
        if user and token_generator.check_token(user, token):
            user.set_password(password)
            user.save()

            jwt_token = RefreshToken.for_user(user)
            data = {
                "refresh":str(jwt_token),
                "access":str(jwt_token.access_token)
            }

            return Response(data, status=status.HTTP_200_OK)
        return Response({"message":"link expired"}, status=status.HTTP_400_BAD_REQUEST)