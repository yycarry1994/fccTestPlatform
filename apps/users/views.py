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
from users import serializers


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
# 日志器
logger = logging.getLogger('logs')


class Users(viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
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
        user = self.get_queryset().get(id=serializer.data.get('id'))
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data = {
            'user': serializer.data,
            'token':  token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class Count(viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def list_0(self, request, email, *args, **kwargs):
        email_rule = r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
        flag = re.match(email_rule, email, flags=0)
        count = 0
        data = {
            'email': email,
            'count': count
        }
        if flag:
            qs = self.get_queryset()
            try:
                qs = qs.get(email=email)
            except Exception:
                qs = None
            if qs:
                count = 1
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '邮箱名不符合规则'}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def list_1(self, request, username, *args, **kwargs):
        count = 0
        data = {
            'username': username,
            'count': count
        }
        qs = self.get_queryset()
        try:
            qs = qs.get(username=username)
        except Exception:
            qs = None
        if qs:
            count = 1
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_200_OK)