# coding=utf-8

from pocopytest.testcase.utils.util import *

LOGGING = get_logger(__name__)


@pytest.fixture(autouse=True)
def fix_input(request):
    LOGGING.info(__name__)
    poco = request.cls.poco
    click_obj(poco, UI.MAIN_START)
    click_obj(poco, UI.MENU_INPUT, sleep_time=1)
