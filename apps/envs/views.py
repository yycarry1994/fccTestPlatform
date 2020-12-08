from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from utils.pagination import PageNumberPagination

from envs.models import Envs
from envs.serializers import EnvsModelSerializer, EnvsNameSerializer
# Create your views here.


class EnvsViewSet(ModelViewSet):
    queryset = Envs.objects.all().order_by('-create_time')
    serializer_class = EnvsModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['name', 'desc']
    ordering_fields = ['create_time', 'update_time']

    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        """
        返回所有环境变量ID和名称
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNameSerializer
        else:
            return self.serializer_class

    def filter_queryset(self, queryset):
        if self.action == 'names':
            return self.queryset
        else:
            return super().filter_queryset(queryset)

    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)
