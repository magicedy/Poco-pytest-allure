# coding=utf-8

from pocopytest.testcase.utils.util import *

LOGGING = get_logger(__name__)


@allure.feature('demo测试')
@allure.story('滑动列表')
class TestListScroll:
    @allure.title('滑动列表测试')
    # @NewTest
    def test_list_scroll(self):
        u_list_view = new_poco(self.poco, UI.LIST_VIEW)
        u_list_view.wait_for_appearance(timeout=5)
        _desc = '已打开{}界面'.format(u_list_view)
        LOGGING.info(_desc)
        with allure.step(_desc):
            allure_snap()
        u_item12 = scroll_find(self.poco, UI.LIST_ITEM12, scrollview_query=UI.LIST_SCROLLVIEW, per=0.2, dur=0.5)
        u_item12.click()
        u_selcted = new_poco(self.poco, UI.LIST_SELECT)
        u_selcted_text = u_selcted.get_text()
        _desc = 'selcted: {0}'.format(u_selcted_text)
        LOGGING.info(_desc)
        with allure.step(_desc):
            allure_snap()
        assert u_selcted_text == 'Item 12', "selcted not correct."
