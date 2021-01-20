from django.db.models import Count
import logging
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from projects.serializers import ProjectModelSerializer, ProjectNamesSerializer, ProjectRunSerializer
from interfaces.serializers import InterfaceNameSerializer
from projects.models import Projects
from utils import pagination, common
from testcases.models import Testcases
from testsuits.models import Testsuits
from interfaces.models import Interfaces
from configures.models import Configures
from .tasks import yb_run_testcase
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all().order_by('-create_time')
    serializer_class = ProjectModelSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'leader']
    ordering_fields = ['create_time', 'update_time']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        """
        获取所有项目信息，分页展示
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().list(request, *args, **kwargs)
        results = response.data.get('results')
        for item in results:
        #     id = item.get('id')
        #     # 笨办法通过关联字段一个一个查询
        #     testsuits_count = Testsuits.objects.filter(project=id).count()
        #     interfaces = Interfaces.objects.filter(project=id)
        #     interfaces_count = interfaces.count()
        #     interfaces_id_l = []
        #     for obj in interfaces:
        #         interfaces_id = obj.id
        #         interfaces_id_l.append(interfaces_id)
        #     testcases_count = Testcases.objects.filter(interface__in=interfaces_id_l).count()
        #     configures_count = Configures.objects.filter(interface__in=interfaces_id_l).count()
        #     new_dict = {
        #         'interfaces': interfaces_count,
        #         'testsuits': testsuits_count,
        #         'testcases': testcases_count,
        #         'configures': configures_count
        #     }
        #     item.update(new_dict)
        # response.data['results'] = results
            # 获取当前项目下的所有接口总数
            # item['interfaces'] = Interfaces.objects.filter(project_id=item.get('id')).count()
            # 获取当前项目下的所有套件总数
            item['testsuits'] = Testsuits.objects.filter(project_id=item.get('id')).count()

            # 获取用例总数
            # a.使用annotate方法来进行分组运算
            # b.annotate方法可以传递聚合运算对象
            # c.聚合运算会默认设置字段别名，testcases__count
            # d.可以给聚合运算设置别名，别名=聚合运算对象
            # e.values方法指定需要查询的字段
            interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(project_id=item.get('id'))
            item['interfaces'] = interface_testcase_qs.count()
            testcases_count = 0
            for one_dict in interface_testcase_qs:
                testcases_count += one_dict.get('testcases')
            item['testcases'] = testcases_count

            interface_configure_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(
                project_id=item.get('id'))

            configures_count = 0
            for one_dict in interface_configure_qs:
                configures_count += one_dict.get('configures')
            item['configures'] = configures_count
        return Response(response.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        """
        获取所有项目名称
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        """
        重写父类方法：获取序列化器对象
        :return:
        """
        if self.action == 'names':
            return ProjectNamesSerializer

        elif self.action == 'interfaces':
            return InterfaceNameSerializer

        elif self.action == 'run':
            return ProjectRunSerializer

        else:
            return self.serializer_class

    def filter_queryset(self, queryset):
        """
        重写父类方法：获取查询集
        :param queryset:
        :return:
        """
        if self.action == 'names':
            return self.queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        """
        重写父类方法：分页
        :param queryset:
        :return:
        """
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)

    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        """
        获取指定项目下的所有接口信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        project_id = self.get_object().id
        queryset = Interfaces.objects.filter(project=project_id)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        # 2、创建目录
        env, testcase_dir = common.get_env_dir(self.get_serializer(data=request.data))

        # 3、创建用例运行需要的yaml文件
        interface_qs = Interfaces.objects.filter(project=instance.id)
        for interface_obj in interface_qs:
            testcases_qs = Testcases.objects.filter(interface=interface_obj.id)
            for testcases_obj in testcases_qs:
                common.generate_testcase_file(testcases_obj, env, testcase_dir)

        # 4、运行测试用例并生成报告
        # 使用异步框架celery，方法使用delay调用
        return yb_run_testcase.delay(instance, testcase_dir)
