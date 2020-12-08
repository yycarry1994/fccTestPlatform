from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import *
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# payload = jwt_payload_handler(user)
#
# return {
#     'token': jwt_encode_handler(payload),
#     'user': user
# }


class UserSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(write_only=True, help_text='确认密码',)
    token = serializers.CharField(read_only=True, help_text='token')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'email', 'token']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'username': {
                'min_length': 6,
                'max_length': 20,
                'required': True,
                'help_text': '用户名',
                'validators': [
                    UniqueValidator(User.objects.all(), message='用户名名不能重复'),
                    # is_container_project_word
                ],
                'error_messages': {
                    'min_length': '用户名不能少于6位',
                    'max_length': '用户名不能超过20位',
                }
            },
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
                'help_text': '密码',
                'error_messages': {
                    'min_length': '密码不能少于6位',
                    'max_length': '密码不能超过20位',
                }
            },
            'email': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
                'help_text': '邮箱',
                'error_messages': {
                    'required': '邮箱为必传参数'
                }
            },

        }

    def validate(self, attrs):
        password = attrs.get('password')
        _password = attrs.get('password_confirm')
        if password != _password:
            raise serializers.ValidationError('两次密码输入不一致，请重新输入')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user

    # def create_uesr(self, validated_data):
    #     pass


class Userloginserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

        extra_kwargs = {
            'username': {
                'min_length': 6,
                'max_length': 20,
                'required': True,
                'help_text': '用户名'
            },
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
                'help_text': '密码',
                'error_messages': {
                    'min_length': '密码不能少于6位',
                    'max_length': '密码不能超过20位',
                }
            }
        }
