#!coding=utf-8

from celery import Celery

# 第一个参数 是当前脚本的名称，第二个参数 是 broker 服务地址
from httprunner import HttpRunner
from rest_framework.response import Response
from utils.common import generate_report

app = Celery('tasks', backend='redis://172.25.17.34', broker='redis://172.25.17.34')


@app.task
def add(x, y):
    return x + y


@app.task
def run_testcase(instance, testcase_dir_path):
    # 创建HttpRunner对象
    runner = HttpRunner()
    try:
        # 2、运行用例
        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'msg': '用例执行失败', 'code': '0'}
        return Response(res, status=400)

    # 3、创建报告
    report_id = generate_report(runner, instance)
    return Response({'id': report_id}, status=201)
