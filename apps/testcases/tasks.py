from __future__ import absolute_import, unicode_literals

from celery import shared_task
from utils.common import run_testcase


@shared_task
def yb_run_testcase(instance, testcase_dir_path):
    run_testcase(instance, testcase_dir_path)