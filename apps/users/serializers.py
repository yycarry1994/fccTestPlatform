from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import *

# payload = jwt_payload_handler(user)
#
# return {
#     'token': jwt_encode_handler(payload),
#     'user': user
# }


class UserSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(write_only=True, help_text='确认密码',)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password', 'password_confirm', 'email']
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
                    UniqueValidator(UserModel.objects.all(), message='用户名名不能重复'),
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
        user = UserModel.objects.create_user(**validated_data)
        return user

    # def create_uesr(self, validated_data):
    #     pass
