# coding=utf-8

from pocopytest.testcase.utils.util import *


@allure.feature('demo测试')
@allure.story('滑动列表')
class TestListScroll:
    @allure.title('滑动列表测试')
    # @DebugTest
    def test_list_scroll(self):
        u_list_view = new_poco(self.poco, UI.LIST_VIEW)
        u_list_view.wait_for_appearance(timeout=5)
        _desc = f'已打开界面: {u_list_view}'
        logger.info(_desc)
        with allure.step(_desc):
            allure_snap()
        u_item12 = scroll_find(self.poco, UI.LIST_ITEM12, scrollview_query=UI.LIST_SCROLLVIEW, per=0.2, dur=0.5)
        u_item12.click()
        u_selected = new_poco(self.poco, UI.LIST_SELECT)
        u_selected_text = u_selected.get_text()
        _desc = f'selcted: {u_selected_text}'
        logger.info(_desc)
        with allure.step(_desc):
            allure_snap()
        assert u_selected_text == 'Item 12', "selcted not correct."
