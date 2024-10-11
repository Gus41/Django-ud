import math
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