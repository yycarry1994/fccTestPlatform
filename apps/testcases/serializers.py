from testcases.models import Testcases
from envs.models import Envs
from utils.validates import *


class InterfaceProjectSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id',
                                   write_only=True, validators=[is_existed_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id',
                                   write_only=True, validators=[is_existed_interfaces_id])

    class Meta:
        model = Interfaces
        fields = ['name', 'project', 'pid', 'iid']
        read_only_fields = ['name']

    def validate(self, attrs):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        _pid = Interfaces.objects.get(id=iid).project.id
        if pid == _pid:
            return attrs
        else:
            raise serializers.ValidationError('项目id与接口id不匹配')


class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfaceProjectSerializer(label='所属项目和接口信息', help_text='所属项目和接口信息')

    class Meta:
        model = Testcases
        exclude = ['create_time', 'update_time']

    # def to_internal_value(self, data):
    #     pass
    #
    def to_representation(self, instance):
        qs = super().to_representation(instance)
        qs.pop('include')
        qs.pop('request')
        return qs

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.pop('interface').get('iid')
        result['interface_id'] = iid
        return result


class TestcasesRunSerializer(serializers.ModelSerializer):

    env_id = serializers.IntegerField(validators=[is_existed_envs_id])

    class Meta:
        model = Testcases
        fields = ['id', 'env_id']


class TestcasesNameSerializer(serializers.ModelSerializer):
    """
    其他关联应用引用的
    """

    class Meta:
        model = Testcases
        fields = ('id', 'name')