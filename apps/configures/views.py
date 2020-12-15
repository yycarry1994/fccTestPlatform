from django.shortcuts import render
import json
from django.shortcuts import render
from rest_framework import filters
from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins

from configures.serializers import ConfigureModelSerializer
from utils import validates, handle_datas
from configures.models import Configures
from utils.pagination import PageNumberPagination
from interfaces.models import Interfaces

# Create your views here.


class ConfiguresViewSet(ModelViewSet):
    queryset = Configures.objects.all().order_by('-create_time')
    serializer_class = ConfigureModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # lookup_field = ['id', 'name'] 传入url中的
    search_fields = ['name']
    ordering_fields = ['id', 'update_time']

    def retrieve(self, request, *args, **kwargs):
        configure_obj = self.get_object()
        author = configure_obj.author
        configure_name = configure_obj.name
        selected_interface_id = configure_obj.id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project.id
        others = json.loads(configure_obj.request, encoding='utf-8')['config']['request']
        data = {
            "author": author,
            "configure_name": configure_name,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
        }
        data.update(others)
        return Response(data, status=status.HTTP_200_OK)

