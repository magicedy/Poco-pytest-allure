# coding=utf-8

from pocopytest.testcase.utils.util import *

LOGGING = get_logger(__name__)


@pytest.fixture(autouse=True)
def fix_drag(request):
    LOGGING.info(__name__)
    poco = request.cls.poco
    click_obj(poco, UI.MAIN_START)
    click_obj(poco, UI.MENU_DRAG_DROP, sleep_time=1)
