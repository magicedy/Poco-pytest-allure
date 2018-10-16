# coding=utf-8

import pytest
from pocopytest.testcase.utils.util import *
from pocopytest.testcase.utils.paramertrize import Param


@allure.feature('demo测试')
@allure.story('输入')
@allure.title('输入测试')
@pytest.mark.parametrize('text,error_msg', Param.TESTINPUT)
def test_input(poco, text, error_msg):
    print(text)
    poco('playBasic').wait_for_appearance(timeout=5)
    with allure.step('进入playBasic'):
        allure_snap()
    input_field = poco('pos_input')
    with allure.step('输入:{}'.format(text)):  # allure步骤
        input_field.set_text(text)
        sleep(0.5)
    inputed_text = input_field.offspring('Text').attr('text')
    with allure.step('实际输入:{}'.format(inputed_text)):
        allure_snap()  # 截图作为allure图片附件
        sleep(0.5)
    assert inputed_text == text, error_msg
