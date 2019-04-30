# coding=utf-8

from pocopytest.testcase.utils.util import *


@allure.feature('demo测试')
@allure.story('滑动列表')
class TestListscoll:
    @allure.title('滑动列表测试')
    # @NewTest
    def test_listscoll(self):
        u_list_view = new_poco(self.poco, UI.LIST_VIEW)
        u_list_view.wait_for_appearance(timeout=5)
        with allure.step('进入playListView'):
            allure_snap()
        scrollview = new_poco(self.poco, UI.LIST_SCROLLVIEW)
        list_top = scrollview.focus([0.5, 0]).get_position()[1]
        list_bottom = scrollview.focus([0.5, 1]).get_position()[1]
        flag = True
        while flag:
            with self.poco.freeze() as frozen_poco:
                u_item12 = new_poco(frozen_poco, UI.LIST_ITEM12)
                if u_item12.exists() and list_top < u_item12.get_position()[1] < list_bottom:
                    flag = False
                scrollview.scroll(percent=0.2, duration=0.5)
                sleep(0.5)
        u_item12.click()
        u_selcted = new_poco(self.poco, UI.LIST_SELECT)
        u_selcted_text = u_selcted.get_text()
        with allure.step('selcted: {0}'.format(u_selcted_text)):
            allure_snap()
        assert u_selcted.get_text() == 'Item 12', "selcted not correct."
