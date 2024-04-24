from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class ContentPaginator(Paginator):
    """
    Paginator for Django content types.
    """
    def __init__(self, object_list, per_page, **kwargs):
        super().__init__(object_list, per_page, **kwargs)

    def page(self, number):
        try:
            return super().page(number)
        except PageNotAnInteger:
            return super().page(1)
        except EmptyPage:
            return super().page(self.num_pages)
