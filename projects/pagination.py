from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    # page_size = 10
    # def get_page_size(self, request):
    #     page_size = request.query_params.get('page_size', 10)
    #     return page_size


    page_size_query_param = 'page_size'
    max_page_size = 100




    # page_size_query_param = 'page_size'
    # max_page_size = 100

    # def get_paginated_response(self, data):
    #     page_size = self.get_page_size(self.request)
    #     page_number = self.request.query_params.get(self.page_query_param, 1)
    #     return self.get_response_with_metadata(data, page_size, page_number)

    # def get_response_with_metadata(self, data, page_size, page_number):
    #     return {
    #         'pagination': {
    #             'page_size': page_size,
    #             'page_number': page_number,
    #             'total_pages': self.page.paginator.num_pages,
    #             'count': self.page.paginator.count,
    #         },
    #         'results': data
    #     }