from unittest import TestCase
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

class PaginationTest(TestCase):

    def test_make_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qnt=4,
            current_page=1
        )
        self.assertEqual([1,2,3,4],pagination)

    def test_first_range_is_correct_if_current_page_is_less_than_middle_page(self):

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qnt=4,
            current_page=3
        )
        self.assertEqual([2,3,4,5],pagination)

    def test_middle_range_is_correct(self):

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qnt=4,
            current_page=10
        )
        self.assertEqual([9,10,11,12],pagination)

    def test_final_range_is_correct(self):

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qnt=4,
            current_page=19
        )
        self.assertEqual([17,18,19,20],pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qnt=4,
            current_page=20
        )
        self.assertEqual([17,18,19,20],pagination)
        

    