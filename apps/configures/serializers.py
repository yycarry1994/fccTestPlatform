import locale
from rest_framework import serializers

from configures.models import Configures
from debugtalks.models import DebugTalks

locale.setlocale(locale.LC_CTYPE, 'chinese')


class ConfigureModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        exclude = ('update_time', )
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class ConfigureNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name')