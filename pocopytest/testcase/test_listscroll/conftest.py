# coding=utf-8

from pocopytest.testcase.utils.util import *


@pytest.fixture(autouse=True)
def fix_listscroll(request):
    click_obj(request.cls.poco, UI.MAIN_START)
    click_obj(request.cls.poco, UI.MENU_LISTVIEW, sleep_time=1)
