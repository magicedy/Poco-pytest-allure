# coding=utf-8

from pocopytest.testcase.utils.util import *
from pocopytest.testcase.utils.parametrize import Param


@allure.feature('demo测试')
@allure.story('输入')
class TestInput:
    @allure.title('输入测试')
    # @DebugTest
    @pytest.mark.parametrize('input_text,error_msg', Param.TEST_INPUT)
    def test_input(self, input_text, error_msg):
        u_input_view = new_poco(self.poco, UI.INPUT_VIEW)
        u_input_view.wait_for_appearance(timeout=5)
        _desc = f'已打开界面: {u_input_view}'
        logger.info(_desc)
        with allure.step(_desc):
            allure_snap()
        input_obj(self.poco, UI.INPUT_FILED, text=input_text, assert_query=UI.INPUT_ASSERT)
