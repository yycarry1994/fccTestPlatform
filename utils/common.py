import locale
import os
import json
import yaml

from rest_framework.response import Response
from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from httprunner.task import HttpRunner


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y-%m-%d %H:%M:%S'


def generate_testcase_file(instance, env, testcase_dir):
    # 3、生成用例的yaml文件
    testcase_list = []

    # 构造公共的配置信息（如果在创建用例时，未选择关联的配置，那么就使用公共的config）
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)
    # 取出用例所属接口信息，并获取接口所属的项目名称
    intesrface_name = instance.interface.name
    project_name = instance.interface.project.name

    # 获取include，并解析所属的配置信息和前置用例信息
    include = json.loads(instance.include, encoding='utf-8')

    # 获取用例的request信息
    request = json.loads(instance.request, encoding='utf-8')

    # 拼接以项目命名的路径
    testcase_dir = os.path.join(testcase_dir, project_name)

    # 如果要创建嵌套的多级目录时，往往使用os.makedirs
    # os.mkdir()
    if not os.path.exists(testcase_dir):
        os.makedirs(testcase_dir)

        # 通过项目名称获取当前项目下的debugtalk.py文件的内容，并写入项目目录下
        debugtalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj.debugtalk else ''
        with open(os.path.join(testcase_dir, 'debugtalk.py'), 'w') as f:
            f.write(debugtalk)

    # 获取以接口名命名的路径，如果没有则创建
    testcase_dir = os.path.join(testcase_dir, intesrface_name)
    if not os.path.exists(testcase_dir):
        os.makedirs(testcase_dir)

    # 获取config
    config_id = include.get('config')
    if config_id is not None:
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request['config']['request']['base_url'] = env.base_url if env.base_url else ''
            testcase_list[0] = config_request

    # 获取前置用例
    prefix_testcase_list = include.get('testcases')
    if prefix_testcase_list:
        for testcase_id in prefix_testcase_list:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue

            # 将前置用例的request数据添加到testcase_list中
            testcase_list.append(testcase_request)

    # 将当前用例的request，添加到testcase_list中
    testcase_list.append(request)

    testcase_dir = os.path.join(testcase_dir, instance.name + '.yaml')
    with open(testcase_dir, 'w', encoding='uff-8') as f:
        # 使用yaml.dump可以将python中的基本类型（字典、嵌套字典的列表）转化为yaml文件
        # 第一个参数为基本类型数据，第二个参数为文件对象
        yaml.dump(testcase_list, f, allow_unicode=True)


def run_testcase(instance, testcase_dir_path):
    # 创建HttpRunner对象
    runner = HttpRunner()
    try:
        # 2、运行用例
        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'msg': '用例执行失败', 'code': '0'}
        return Response(res, status=400)