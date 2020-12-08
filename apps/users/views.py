from django.db.models import Q
from django.shortcuts import render
import re
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import logging
from rest_framework_jwt.settings import api_settings
from users.models import *
from django.contrib.auth.models import User
from users import serializers
from users.serializers import Userloginserializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
# 日志器
logger = logging.getLogger('logs')


class Users(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    # def get_success_headers(self, data):
    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}

    @action(methods=['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        """
        创建用户接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        """
        登录接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.data.get('username')
        password = request.data.get('password')
        queryset = Users.queryset.all().filter(Q(username=username) | Q(password=password))
        if queryset.exists() is True:
            payload = jwt_payload_handler(queryset[0])
            token = jwt_encode_handler(payload)
            data = {
                'username': queryset[0].username,
                'user_id': queryset[0].id,
                'token': token
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '用户名或密码错误'}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        """
        重写父类方法：获取序列化器对象
        :return:
        """
        if self.action == 'login':
            return Userloginserializer
        else:
            return self.serializer_class


class Count(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def list_0(self, request, email, *args, **kwargs):
        """
        查询邮箱是否被注册
        :param request:
        :param email:
        :param args:
        :param kwargs:
        :return:
        """
        count = 0
        # if flag:
        qs = self.get_queryset()
        try:
            qs = qs.get(email=email)
        except Exception:
            qs = None
        if qs:
            count = 1
        data = {
            'email': email,
            'count': count
        }
        return Response(data, status=status.HTTP_200_OK)

        # else:
        #     return Response({'msg': '邮箱名不符合规则'}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def list_1(self, request, username, *args, **kwargs):
        """
        查询用户名是否被注册
        :param request:
        :param username:
        :param args:
        :param kwargs:
        :return:
        """
        count = 0
        qs = self.get_queryset()
        try:
            qs = qs.get(username=username)
        except Exception:
            qs = None
        if qs:
            count = 1
        data = {
            'username': username,
            'count': count
        }
        return Response(data, status=status.HTTP_200_OK)
