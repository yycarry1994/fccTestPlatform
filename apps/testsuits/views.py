import os
import time
from datetime import datetime

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from testsuits.models import Testsuits
from testsuits.serializers import TestsuitsModelSerializer, TestsuitRunSerializer
from utils import pagination
from rest_framework import filters
from testcases.models import Testcases
from utils import common
from .tasks import yb_run_testcase
from rest_framework.response import Response
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
        testcase_l = Testcases.objects.filter(id__in=eval(instance.include))
        for testcase_obj in testcase_l:
            common.generate_testcase_file(testcase_obj, env, testcase_dir)

        # 4、运行httprunner
        run_task = yb_run_testcase.delay(instance, testcase_dir)
        # 测试作用，使用异步接口，但是前端没有做相应调整
        time.sleep(5)
        if run_task.status == 'SUCCESS':
            report_id = run_task.result
            return Response({'id': report_id}, status=201)

        # # 4、运行httprunner
        # return common.run_testcase(instance, testcase_dir)

    def get_serializer_class(self):
        if self.action == 'run':
            return TestsuitRunSerializer
        else:
            return self.serializer_class
