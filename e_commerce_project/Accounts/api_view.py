from . import serializers
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        if request.user.is_authenticated:        
            serializer = serializers.UserProfileSerializer(request.user)
            return Response(data=serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(data={'message':'login required for shopping'})


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny,]
    serializer_class =serializers.UserRegisterSerializer
    
    
             
        


class UserLoginView(APIView):
    permission_classes = [AllowAny,]
    authentication_classes = [SessionAuthentication,]
    
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password =serializer.validated_data['password']
            
            if CustomUser.objects.filter(email=email).exists():
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)

                    data = {'message':"login successful"}
                    return Response(serializer.data , status=status.HTTP_200_OK)
                else:
                    data = {'message':"password wrong"}
                    return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
            else:
                 data = {"message":"there is no account with this email"}
                 return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class UserLogOut(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        logout(request)
        data = {
            'message':"logout successful"
        }
        return Response(data,status=status.HTTP_200_OK)