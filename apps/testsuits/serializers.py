import re

from rest_framework import serializers
from rest_framework import validators

from .models import Testsuits
from projects.models import Projects
from interfaces.models import Interfaces
from utils import validates


def validate_include(value):
    # obj = eval(value)
    obj = re.match(r'^\[\d+(, *\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('参数格式有误')

    result = obj.group()
    try:
        data = eval(result)
    except:
        raise serializers.ValidationError('参数格式有误')

    for item in data:
        if not Interfaces.objects.filter(id=item).exists():
            raise serializers.ValidationError(f'接口id【{item}】不存在')


class TestsuitsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'include': {
                'validators': [validate_include]
            }
        }

    # to_internal_value方法为反序列化输入的入口方法
    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        tmp['project'] = tmp.pop('project_id')
        return tmp

    # def create(self, validated_data):
    #     project = validated_data.pop('project_id')
    #     validated_data['project'] = project
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     if 'project_id' in validated_data:
    #         project = validated_data.pop('project_id')
    #         validated_data['project'] = project
    #         return super().update(instance, validated_data)


class TestsuitRunSerializer(serializers.ModelSerializer):

    env_id = serializers.IntegerField(validators=[validates.is_existed_envs_id])

    class Meta:
        model = Testsuits
        fields = ['id', 'env_id']