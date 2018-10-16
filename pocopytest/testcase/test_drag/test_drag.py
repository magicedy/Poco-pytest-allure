# coding=utf-8

import pytest
from pocopytest.testcase.utils.util import *
from pocopytest.testcase.utils.paramertrize import Param

@allure.feature('demo测试')
@allure.story('拖动')
@allure.title('拖动测试')
def test_drag(poco):
    poco('playDragAndDrop').wait_for_appearance(timeout=5)
    with allure.step('进入playDragAndDrop'):
        allure_snap()
    shell = poco('shell').focus('center')
    for star in poco('star'):
        with allure.step('拖动: {0}'.format(star.attr('name'))):
            star.drag_to(shell)
            allure_snap()  # 截图作为allure图片附件
            sleep(1)
    scoreVal = poco('scoreVal').get_text()
    assert scoreVal == '100', "score not correct."
