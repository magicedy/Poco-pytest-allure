# coding=utf-8

from pocopytest.testcase.utils.util import *
from pocopytest.testcase.utils.parametrize import Param


@allure.feature('demo测试')
@allure.story('输入')
class TestInput:
    @allure.title('输入测试')
    # @NewTest
    @pytest.mark.parametrize('text,error_msg', Param.TEST_INPUT)
    def test_input(self, text, error_msg):
        u_input_view = new_poco(self.poco, UI.INPUT_VIEW)
        u_input_view.wait_for_appearance(timeout=5)
        with allure.step('已打开{}界面'.format(u_input_view)):
            allure_snap()
        input_obj(self.poco, UI.INPUT_FILED, text=text, assert_query=UI.INPUT_ASSERT)
