import math
from django.core.paginator import Paginator

def make_pagination(request,queryset,per_page,qty_pages=4):
    try:
        current_page = int(request.GET.get("page",1)) #if parameter page not exists, return 1
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset,per_page)
    page_obj = paginator.get_page(current_page)
    
    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return page_obj, pagination_range,current_page


def make_pagination_range(page_range,qnt,current_page):

    middle_range = math.ceil(qnt/2) #int number
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)


    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)
    return page_range[start_range:stop_range] #slice