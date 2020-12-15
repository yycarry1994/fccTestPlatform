import locale
from rest_framework import serializers

from configures.models import Configures
from testcases.serializers import InterfaceProjectSerializer
from interfaces.models import Interfaces
from debugtalks.models import DebugTalks

locale.setlocale(locale.LC_CTYPE, 'chinese')


class ConfigureModelSerializer(serializers.ModelSerializer):

    interface = InterfaceProjectSerializer(help_text='接口id', label='接口id')

    class Meta:
        model = Configures
        exclude = ('update_time', 'create_time')
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'request': {
                'write_only': True
            }
        }

    # def create(self, validated_data):
    #     interface_id = validated_data.get('interface')['iid']
    #     validated_data['interface'] = Interfaces.objects.get(id=interface_id)
    #     return super().create(validated_data)

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.pop('interface').get('iid')
        result['interface_id'] = iid
        return result


class ConfigureNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name')