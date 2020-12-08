import re

from rest_framework import serializers
from rest_framework import validators

from .models import Reports
from projects.models import Projects
from interfaces.models import Interfaces


class ReportModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ['update_time', 'html']

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    # 反序列化输出的入口（可以重写此方法来实现改变输出内容的作用）
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['result'] = 'Pass' if res['result'] else 'Fail'
        return res

    # # 序列化输入的入口（可以重写此方法实现数据过滤）
    # def to_internal_value(self, data):
    #     res = super().to_internal_value(data)
    #     # 进行你需要的操作
    #     return res

