from rest_framework import serializers
from debugtalks.models import DebugTalks


class DebugTalksModelSerializer(serializers.ModelSerializer):

    project = serializers.StringRelatedField(help_text='项目名称')

    class Meta:
        model = DebugTalks
        fields = ['id', 'project', 'name']


class DebugTalksNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebugTalks
        fields = ['id', 'debugtalk']




# from rest_framework import serializers
#
# from .models import DebugTalks
#
#
# class DebugTalksSerializer(serializers.ModelSerializer):
#     """
#     DebugTalks序列化器
#     """
#     project = serializers.StringRelatedField(help_text='项目名称')
#
#     class Meta:
#         model = DebugTalks
#         exclude = ('create_time', 'update_time')
#         # read_only_fields指定哪些字段需要添加read_only=True
#         read_only_fields = ('name', 'project')
#
#         extra_kwargs = {
#             'debugtalk': {
#                 'write_only': True
#             }
#         }
