# coding=utf-8

from pocopytest.testcase.utils.util import *


@allure.feature('demo测试')
@allure.story('拖动')
class TestDrag:
    @allure.title('拖动测试')
    @NewTest
    def test_drag(self):
        u_drag = new_poco(self.poco, UI.DRAG_VIEW)
        u_drag.wait_for_appearance(timeout=5)
        with allure.step('已打开{}界面'.format(u_drag)):
            allure_snap()
        with self.poco.freeze() as frozen_poco:
            u_shell = new_poco(frozen_poco, UI.DRAG_SHELL)
            u_stars = new_poco(frozen_poco, UI.DRAG_STAR)
            for u_star in u_stars:
                with allure.step('拖动: {0}'.format(u_stars.attr('name'))):
                    u_star.drag_to(u_shell.focus('center'))
                    allure_snap()
                    sleep(1)
        u_score = new_poco(self.poco, UI.DRAG_SCORE)
        assert u_score.get_text() == '100', "score not correct."
