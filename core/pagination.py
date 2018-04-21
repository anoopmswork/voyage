"""
Pagination
==========
"""

from rest_framework.pagination import PageNumberPagination


class ExPageNumberPagination(PageNumberPagination):
    """
    Extends standard drf.PageNumberPagination class to enabled page_size param
    """
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_next_link(self):
        """
        Overriding to get page number instead of page url
        """
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        """
        Overriding to get page number instead of page url
        """
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number
