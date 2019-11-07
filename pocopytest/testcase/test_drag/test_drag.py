# coding=utf-8

from pocopytest.testcase.utils.util import *

logger = get_logger(__name__)


@allure.feature('demo测试')
@allure.story('拖动')
class TestDrag:
    @allure.title('拖动测试')
    @DebugTest
    def test_drag(self):
        u_drag = new_poco(self.poco, UI.DRAG_VIEW)
        u_drag.wait_for_appearance(timeout=5)
        _desc = f'已打开界面: {u_drag}'
        logger.info(_desc)
        with allure.step(_desc):
            allure_snap()
        with self.poco.freeze() as frozen_poco:
            logger.debug('freeze()获取shell和star的位置, 因为shell和未拖动的star位置一直不变')
            u_shell = new_poco(frozen_poco, UI.DRAG_SHELL)
            u_stars = new_poco(frozen_poco, UI.DRAG_STAR)
            for u_star in u_stars:
                _desc = f'拖动: {u_stars.attr("name")}'
                logger.info(_desc)
                with allure.step(_desc):
                    if SD.PLAT == 'pc_win':
                        _dur = 0.2
                    else:
                        _dur = 1
                    u_star.drag_to(u_shell.focus('center'), duration=_dur)
                    allure_snap()
                    sleep(1)
        u_score = new_poco(self.poco, UI.DRAG_SCORE)
        u_score_text = u_score.get_text()
        logger.debug(f'u_score_text={u_score_text}')
        assert u_score_text == '100', "score not correct."
