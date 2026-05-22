from django.core.paginator import Paginator
from projects.constants import NUMBER_OF_PAGINATOR_PAGES


def get_paginator(request, queryset,
                  number_of_pages=NUMBER_OF_PAGINATOR_PAGES):
    paginator = Paginator(queryset, number_of_pages)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)