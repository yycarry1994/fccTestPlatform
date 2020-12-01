from django.shortcuts import render
import logging
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils import pagination
from rest_framework import filters

from projects.serializers import ProjectModelSerializer, ProjectNamesSerializer
from interfaces.serializers import InterfaceNameSerializer
from projects.models import Projects
from testcases.models import Testcases
from testsuites.models import Testsuits
from interfaces.models import Interfaces
from configures.models import Configures
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'leader']
    ordering_fields = ['name', 'id', 'leader']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data.get('results')
        for item in results:
            id = item.get('id')
            # 笨办法通过关联字段一个一个查询
            testsuits_count = Testsuits.objects.filter(project=id).count()
            interfaces = Interfaces.objects.filter(project=id)
            interfaces_count = interfaces.count()
            interfaces_id_l = []
            for obj in interfaces:
                interfaces_id = obj.id
                interfaces_id_l.append(interfaces_id)
            testcases_count = Testcases.objects.filter(interface__in=interfaces_id_l).count()
            configures_count = Configures.objects.filter(interface__in=interfaces_id_l).count()
            new_dict = {
                'interfaces': interfaces_count,
                'testsuits': testsuits_count,
                'testcases': testcases_count,
                'configures': configures_count
            }
            item.update(new_dict)
        response.data['results'] = results
        return Response(response.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectNamesSerializer
        elif self.action == 'interfaces':
            return InterfaceNameSerializer
        else:
            return self.serializer_class

    # def get_queryset(self):
    #     if self.action == 'interfaces':
    #         return Interfaces.objects.all()
    #     else:
    #         return self.queryset

    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        project_id = self.get_object().id
        queryset = Interfaces.objects.filter(project=project_id)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

