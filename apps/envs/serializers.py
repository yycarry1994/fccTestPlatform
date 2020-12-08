
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from envs.models import Envs


class EnvsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        exclude = ['update_time']
        # fields = '__all__'
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


class EnvsNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        fields = ('id', 'name')