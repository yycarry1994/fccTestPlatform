import os
from datetime import datetime

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from envs.models import Envs
from testsuits.models import Testsuits
from testsuits.serializers import TestsuitsModelSerializer, TestsuitRunSerializer
from utils import pagination
from rest_framework import filters
from testcases.models import Testcases
from utils import common
# Create your views here.


class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all().order_by('-create_time')
    serializer_class = TestsuitsModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'project']
    ordering_fields = ['create_time', 'update_time']

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        env, testcase_dir = common.get_env_dir(self.get_serializer(data=request.data))

        # 3、创建用例运行的yaml文件
        testcase_l = Testcases.objects.filter(id__in=instance.include)
        for testcase_obj in testcase_l:
            common.generate_testcase_file(testcase_obj, env, testcase_dir)

        # 4、运行httprunner
        return common.run_testcase(instance, testcase_dir)

    def get_serializer_class(self):
        if self.action == 'run':
            return TestsuitRunSerializer
        else:
            return self.serializer_class
