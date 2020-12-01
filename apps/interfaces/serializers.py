from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from interfaces.models import Interfaces
# from projects.models import Projects


class InterfaceModelSerializer(serializers.ModelSerializer):
    # a.基于从表创建模型序列化器类，默认创建的外键字段类型为PrimaryKeyRelatedField
    # b.默认输出的是父表外键id值
    # project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
    # project = serializers.PrimaryKeyRelatedField(read_only=True)
    # c.可以定义StringRelatedField来指定，序列化输出时，直接调用父表中的__str__方法，将其作为返回值
    # d.StringRelatedField只能用于序列化输出
    # project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

    # d.可以定义SlugRelatedField来指定父表模型类中的某一个字段（尽量使用具有唯一约束的字段）进行输入或输出
    # e.如果仅仅只需要输出那么添加read_only=True即可
    # f.如果需要进行反序列化器输入（校验），必须得指定queryset
    # project = serializers.SlugRelatedField(slug_field='leader', queryset=Projects.objects.all())
    # project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Interfaces
        # fields = ('name', 'leader', 'desc','email', 'interfaces')
        fields = '__all__'

        # extra_kwargs = {
        #     'project': {
        #         'read_only': True
        #     }
        # }

    # def create(self, validated_data):
    #     pass


class InterfaceNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')