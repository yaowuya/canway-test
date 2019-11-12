# -*- coding: utf-8 -*-
'''
-------------------------------------------------
   File Name：     helper
   Author :        zhongrf
   Date：          2019/10/22
-------------------------------------------------
'''
__author__ = 'zhongrf'


def paging(page_size, current_page):
    first_page = int(page_size) * (int(current_page) - 1)
    last_page = first_page + int(page_size)
    return [first_page, last_page]
