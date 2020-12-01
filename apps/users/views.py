from django.shortcuts import render
import re
from rest_framework import viewsets, status
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import logging
from rest_framework_jwt.settings import api_settings
from users.models import *
from django.contrib.auth.models import User
from users import serializers


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Count(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def list_0(self, request, email, *args, **kwargs):
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
