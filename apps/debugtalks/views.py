from django.shortcuts import render
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from debugtalks.models import DebugTalks
from debugtalks.serializers import DebugTalksModelSerializer, DebugTalksNameSerializer
from utils import pagination


class DebugTalksViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksModelSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['create_time', 'update_time']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == 'update':
            return DebugTalksNameSerializer
        elif self.action == 'retrieve':
            return DebugTalksNameSerializer
        else:
            return self.serializer_class


# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins
# from rest_framework import permissions
# from rest_framework.response import Response
#
# from .models import DebugTalks
# from .serializers import DebugTalksSerializer
#
#
# class DebugTalksViewSet(mixins.ListModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.RetrieveModelMixin,
#                         GenericViewSet):
#     """
#     list:
#     返回debugtalk（多个）列表数据
#
#     update:
#     更新（全）debugtalk
#
#     partial_update:
#     更新（部分）debugtalk
#     """
#     queryset = DebugTalks.objects.all()
#     serializer_class = DebugTalksSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     ordering_fields = ('id', 'project_id')
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         data_dict = {
#             "id": instance.id,
#             "debugtalk": instance.debugtalk
#         }
#         return Response(data_dict)
