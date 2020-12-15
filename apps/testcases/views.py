import json
import os
from datetime import datetime
import yaml

from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from interfaces.models import Interfaces
from testcases.serializers import TestcasesModelSerializer, TestcasesRunSerializer
from utils import handle_datas
from testcases.models import Testcases
from envs.models import Envs
from utils.pagination import PageNumberPagination
from utils import common
# Create your views here.


class TestcasesViewSet(ModelViewSet):
    queryset = Testcases.objects.all().order_by('-create_time')
    serializer_class = TestcasesModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    search_fields = ['name']
    ordering_fields = ['create_time', 'update_time']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def retrieve(self, request, *args, **kwargs):
        testcase_obj = self.get_object()

        # 获取用例前置信息
        testcase_include = json.loads(testcase_obj.include, encoding='utf-8')

        # 获取用例请求信息
        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        testcase_request_datas = testcase_request['test']['request']

        # 获取validate列表数据
        testcase_validate = testcase_request['test']['validate']
        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 获取param数据
        testcase_params = testcase_request_datas.get('params')
        testcase_params_list = handle_datas.handle_data4(testcase_params)

        # 处理header数据
        testcase_headers = testcase_request_datas.get('headers')
        testcase_headers_list = handle_datas.handle_data4(testcase_headers)

        # 处理用例variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data6(testcase_form_datas)

        # 处理json数据
        # testcase_json_datas = str(testcase_request_datas.get('json'))
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据
        testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas_list = handle_datas.handle_data3(testcase_extract_datas)

        # 处理parameters数据
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data3(testcase_parameters_datas)

        # 处理setupHooks数据
        testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_datas_list = handle_datas.handle_data5(testcase_setup_hooks_datas)

        # 处理teardownHooks数据
        testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data5(testcase_teardown_hooks_datas)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcases')

        datas = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": testcase_request_datas.get('method'),
            "url": testcase_request_datas.get('url'),
            "param": testcase_params_list,
            "header": testcase_headers_list,
            "variable": testcase_form_datas_list,   # form表单请求数据
            "jsonVariable": testcase_json_datas,

            "extract": testcase_extract_datas_list,
            "validate": testcase_validate_list,
            "globalVar": testcase_variables_list,   # 变量
            "parameterized": testcase_parameters_datas_list,
            "setupHooks": testcase_setup_hooks_datas_list,
            "teardownHooks": testcase_teardown_hooks_datas_list,
        }
        return Response(datas, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        # 1、取出用例、env的模型对象
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        # 2、创建一个以时间戳命名的目录
        testcase_dir = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
        os.makedirs(testcase_dir)

        # 3、创建yaml用例文件
        common.generate_testcase_file(instance=instance, env=env, testcase_dir=testcase_dir)

        # 4、运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir)

    def get_serializer_class(self):
        return TestcasesRunSerializer if self.action == 'run' else self.serializer_class
