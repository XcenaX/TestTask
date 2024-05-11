from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from main.serializers.user import UserSerializer

from project.settings import REFRESH_TOKEN_LIFETIME

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import re
import json

from main.models import User
from rest_framework.permissions import AllowAny


class Login(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Получение JWT токена",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль пользователя'),
            }
        ),
        responses={200: openapi.Response('Токен успешно получен')}
    )
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        unhashed_pass = request.data['password']
        
        try:
            user = User.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            user = None
        if not user:            
            return Response({'success': False, 'message': 'Неверное имя пользователя или пароль'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        data = serializer.data
        data.pop("password", None)
        hashed_pass = user.password
        if check_password(unhashed_pass, hashed_pass):
            refresh = RefreshToken.for_user(user)
            res = {
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                "user": data
            }
            response = Response(res, status=200)
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                expires = REFRESH_TOKEN_LIFETIME,
                httponly=True,
                samesite="None",
                secure=True
            )
            response.set_cookie(
                key='user_id',
                value=user.id,
                httponly=True,
                samesite="None",
                secure=True
            )
            return response
        else:
            return Response({'success': False, 'message': 'Неверное имя пользователя или пароль'}, status=status.HTTP_400_BAD_REQUEST)
            

class Register(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description='Регистрация',        
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'confirm_password'],
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING),
                'password':openapi.Schema(type=openapi.TYPE_STRING),
                'confirm_password':openapi.Schema(type=openapi.TYPE_STRING),                       
                'first_name':openapi.Schema(type=openapi.TYPE_STRING),
                'surname':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            "200": openapi.Response(        
                description='',        
                examples={
                    "application/json": {
                        "success": True,  
                        'message': 'Пользователь успешно создан!'                      
                    },                    
                }
            ),
            "400": openapi.Response(
                description='',                
                examples={
                    "application/json": {
                        "success": False,  
                        'message': 'Такой пользователь уже существует!'                      
                    },                    
                }
            ),            
        })
    def post(self, request):
        try:
            data = json.loads(request.body)
            first_name = data['first_name']
            surname = data['surname']
            unhashed_pass = data['password']
            confirm_pass = data['confirm_password']
            email = data['email']            
        except:
            return Response({'success': False, 'message': 'Переданы не все параметры!'}, status=status.HTTP_400_BAD_REQUEST) 
        
        if(unhashed_pass != confirm_pass):
            return Response({'success': False, 'message': 'Пароли не совпадают!'}, status=status.HTTP_400_BAD_REQUEST) 
        
        for e in first_name + surname:
            if not e.isalnum():
                return Response({'success': False, 'message': 'ФИО не должно содержать специальных символов!'}, status=status.HTTP_400_BAD_REQUEST) 
        
        # phone = request.data['phone']
        # replace_list = ['(', ')', '-', '+', ' ']
        # for symbol in replace_list:
        #     phone = phone.replace(symbol, '')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response({'success': False, 'message': 'Неверный формат Email!'}, status=status.HTTP_400_BAD_REQUEST) 

        if len(unhashed_pass) < 5:
            return Response({'success': False, 'message': 'Пароль должен иметь хотя бы 5 символов!'}, status=status.HTTP_400_BAD_REQUEST) 

        if len(first_name) < 2 or len(surname) < 2:
            return Response({'success': False, 'message': 'Имя и фамилия должны иметь хотя бы 2 символа!'}, status=status.HTTP_400_BAD_REQUEST) 

        try:
            User.objects.get(email__iexact=email)            
            return Response({'success': False, 'message': 'Такой пользователь уже существует!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            pass
        
        new_user = User.objects.create(first_name=first_name, surname=surname, email=email)
        new_user.set_password(unhashed_pass)
        new_user.save()
        
        return Response({'success': True, 'message': 'Пользователь успешно создан!'}, status=status.HTTP_200_OK)

