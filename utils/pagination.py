from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(_PageNumberPagination):
    # 指定默认每一页的数据条数，优先级最高
    page_size = 10
    # 指定前端获取那一页的key值
    page_query_param = 'page'
    # 指定前端获取每一页总数据的key值
    page_size_query_param = 'size'
    # 指定前端能获取的每一页最大条数
    max_page_size = 10
    # 无效页的错误展示
    invalid_page_message = '页码无效'
    # 排序

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('total_pages', self.page.number),
            ('current_page_num', self.page.paginator.num_pages),
        ]))