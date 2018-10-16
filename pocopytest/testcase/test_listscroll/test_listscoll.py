# coding=utf-8

import pytest
from pocopytest.testcase.utils.util import *
from pocopytest.testcase.utils.paramertrize import Param


@allure.feature('demo测试')
@allure.story('滑动列表')
@allure.title('滑动列表测试')
def test_listscoll(poco):
    poco('playListView').wait_for_appearance(timeout=5)
    with allure.step('进入playListView'):
        allure_snap()
    scrollview = poco('playListView').child('Scroll View')
    list_top = scrollview.focus([0.5, 0]).get_position()[1]
    list_bottom = scrollview.focus([0.5, 1]).get_position()[1]
    while not poco(nameMatches='Text.*', text='Item 12').exists():
        scrollview.scroll(percent=0.2, duration=0.5)
        sleep(0.5)
    while not (list_top < poco(nameMatches='Text.*', text='Item 12').get_position()[1] < list_bottom):
        scrollview.scroll(percent=0.2, duration=0.5)
        sleep(0.5)
    poco(nameMatches='Text.*', text='Item 12').click()
    selcted = poco('list_view_current_selected_item_name').get_text()
    with allure.step('selcted: {0}'.format(selcted)):
        allure_snap()
    assert selcted == 'Item 12', "selcted not correct."
