import os
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from reports.serializers import ReportModelSerializer
from reports.models import Reports
from django.http.response import StreamingHttpResponse
from utils.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .utils import get_file_content
import json
from django.conf import settings
# Create your views here.


class ReportsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet
                     ):

    queryset = Reports.objects.all().order_by('-create_time')
    serializer_class = ReportModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'update_time']

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        result = response.data
        result['summary'] = json.loads(result['summary'])
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 从数据库读取html源码
        instance = self.get_object()

        # 将源码写入html文件中
        # 获取测试报告存放路径
        report_dir = settings.REPORT_DIR
        # 生成测试报告完整路径
        report_full_dir = os.path.join(report_dir, instance.name + '.html')
        with open(report_full_dir, 'w') as f:
            f.write(instance.html)

        # 读写html文件对象，并将其传递给StreamingHttpResponse
        # 第一个参数需要传递生成器对象（每次迭代需要返回文件数据）
        response = StreamingHttpResponse(get_file_content(report_full_dir))

        # 如果要提高用户下载，必须添加相关的响应头
        # Content-Type
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition
        # response['Content-Disposition'] = f"attachment; filename*=UTF-8''{instance.name}"
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{instance.name}"

        return response
