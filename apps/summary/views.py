from django.db.models import Sum
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from reports.models import Reports
from testsuits.models import Testsuits
from debugtalks.models import DebugTalks
from configures.models import Configures
from envs.models import Envs

# Create your views here.


class SummaryViewSet(ListModelMixin,
                     GenericViewSet):

    def list(self, request, *args, **kwargs):
        username = request.user.username
        date_joined = request.user.date_joined
        last_login = request.user.last_login
        if request.user.is_superuser is False:
            role = '注册用户'
        else:
            role = '管理员'

        projects_count = Projects.objects.all().count()
        interfaces_count = Interfaces.objects.all().count()
        testcases_count = Testcases.objects.all().count()
        testsuits_count = Testsuits.objects.all().count()
        configures_count = Configures.objects.all().count()
        envs_count = Envs.objects.all().count()
        debug_talks_count = DebugTalks.objects.all().count()
        reports_count = Reports.objects.all().count()
        success = Reports.objects.all().aggregate(Sum('success')).get('success__sum')
        all_cases = Reports.objects.all().aggregate(Sum('count')).get('count__sum')
        success_rate = round(success / all_cases, 2) * 100
        fail_rate = 100 - success_rate
        data = {
            "user": {
                "username": username,
                "role": role,
                "date_joined": date_joined,
                "last_login": last_login
            },
            "statistics": {
                "projects_count": projects_count,
                "interfaces_count": interfaces_count,
                "testcases_count": testcases_count,
                "testsuits_count": testsuits_count,
                "configures_count": configures_count,
                "envs_count": envs_count,
                "debug_talks_count": debug_talks_count,
                "reports_count": reports_count,
                "success_rate": success_rate,
                "fail_rate": fail_rate
            }
        }
        return Response(data, status=status.HTTP_200_OK)

