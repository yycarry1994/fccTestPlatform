from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from testsuits.models import Testsuits
from testsuits.serializers import TestsuitsModelSerializer
from utils import pagination
from rest_framework import filters
# Create your views here.


class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all().order_by('-create_time')
    serializer_class = TestsuitsModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'project']
    ordering_fields = ['create_time', 'update_time']