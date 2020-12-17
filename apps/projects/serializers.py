import locale
from rest_framework import serializers
from projects.models import Projects
from debugtalks.models import DebugTalks
from utils import validates

locale.setlocale(locale.LC_CTYPE, 'chinese')


class ProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        exclude = ('update_time', )
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def create(self, validated_data):
        project = super().create(validated_data)
        # 创建一条debugtalk数据
        # DebugTalks.objects.create(project=project)
        DebugTalks.objects.create(project_id=project.id)
        return project


class ProjectRunSerializer(serializers.ModelSerializer):

    env_id = serializers.IntegerField(validators=[validates.is_existed_envs_id])

    class Meta:
        model = Projects
        fields = ['id', 'env_id']


class ProjectNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('name', 'id')
