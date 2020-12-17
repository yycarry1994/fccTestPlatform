import os
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from interfaces.models import Interfaces
from testcases.models import Testcases
from configures.models import Configures
from envs.models import Envs
from interfaces.serializers import InterfaceModelSerializer, InterfaceRunSerializer
from configures.serializers import ConfigureNamesSerializer
from testcases.serializers import TestcasesNameSerializer
from rest_framework import status, filters
from utils import pagination
from utils import common
# Create your views here.


class InterfaceViewSet(ModelViewSet):
    queryset = Interfaces.objects.all().order_by('-create_time')
    serializer_class = InterfaceModelSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'tester']
    ordering_fields = ['create_time', 'update_time']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        """
        获取所有接口信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().list(request, *args, **kwargs)
        results = response.data.get('results')
        for item in results:
            interface_id = item.get('id')
            item['testcases'] = Testcases.objects.filter(interface=interface_id).count()
            item['configures'] = Configures.objects.filter(interface=interface_id).count()
        return response

    @action(methods=['GET'], detail=True, url_path='configs')
    def configures(self, request, *args, **kwargs):
        """
        获取指定接口的配置信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.get_intetfaces_all(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def testcases(self, request, *args, **kwargs):
        """
        获取指定接口下的所有用例
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.get_intetfaces_all(request, *args, **kwargs)

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        env, testcase_dir = common.get_env_dir(self.get_serializer(data=request.data))

        # 3、创建用例运行的yaml文件
        testcases_qs = Testcases.objects.filter(interface=instance.id)
        for testcase_obj in testcases_qs:
            common.generate_testcase_file(testcase_obj, env, testcase_dir)

        # 4、运行测试用例并生成报告
        return common.run_testcase(instance, testcase_dir)

    def get_serializer_class(self):
        """
        a.不过当前类视图中，使用了多个不同的序列化器类，
        b.那么可以将get_serializer_class重写
        :return:
        """
        # c.继承视图集类之后，会提供action属性，指定当前请求的action方法名称
        # d.可以根据不同的action去选择不同的序列化器类（不同的查询集）
        if self.action == 'configures':
            return ConfigureNamesSerializer

        elif self.action == 'testcases':
            return TestcasesNameSerializer

        elif self.action == 'run':
            return InterfaceRunSerializer

        else:
            return self.serializer_class

    def get_queryset(self):
        """
        重写获取查询集方法
        :return:
        """
        if self.action == 'configures':
            return Configures.objects.all()
        elif self.action == 'testcases':
            return Testcases.objects.all()
        else:
            return self.queryset

    def get_intetfaces_all(self, request, *args, **kwargs):
        """
        将获取指定接口下的相关信息的方法抽公用
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        interface_id = self.get_object().id
        qs = self.get_queryset().filter(interface=interface_id)
        serializer = self.get_serializer(instance=qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
