from django.contrib.auth import get_user_model
from django.shortcuts import render
from applications.account.send_mail import send_message
from applications.account.serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status

User = get_user_model()

class RegisterApiView(APIView):
    # Регистрация пользователя в бд
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response('Вы успешно зарегестрировались!  '
                        'Вам отправлен код активации',
                        status=201)
        

class LoginApiView(ObtainAuthToken):
    # Авторизация пользователя
    
    serializer_class = LoginSerializer
    
    
class LogoutApiView(APIView):
    # Выход пользователя из аккаунта
    
    permission_classes = [IsAuthenticated] # разрешение только для авторизованных пользователей
    
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        
        return Response('Вы успешно разлогонились')
    
    
class ChangePasswordApiView(APIView):
    # Смена пароля пользователя
    
    permission_classes = [IsAuthenticated] # разрешение только для авторизованных пользователей
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        
        return Response('Пароль успешно изменен!')


class AcitvationApiView(APIView):
    # Подтверждение пользователя
    
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'message': 'Вы успшено прошли регистрацию'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message':'Такой пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)