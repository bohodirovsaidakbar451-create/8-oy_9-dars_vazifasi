from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class GenrePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class BookPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 50


class CommentPagination(CursorPagination):
    page_size = 10
    ordering = "-created"
