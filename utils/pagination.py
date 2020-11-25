from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    # 指定默认每一页的数据条数，优先级最高
    page_size = 10
    # 指定前端获取那一页的key值
    page_query_param = 'p'
    # 指定前端获取每一页总数据的key值
    page_size_query_param = 's'
    # 指定前端能获取的每一页最大条数
    max_page_size = 20
    # 无效页的错误展示
    invalid_page_message = '页码无效'