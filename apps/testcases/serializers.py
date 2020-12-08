from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from testcases.models import Testcases


class TestcasesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        # fields = '__all__'
        exclude = ['update_time']
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        tmp['project'] = tmp.pop('project_id')
        return tmp


class TestcasesNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        fields = ('id', 'name')