# coding=utf-8

import allure
from airtest.core.api import *
from poco.exceptions import *
from poco.utils.simplerpc.utils import sync_wrapper
from poco.proxy import UIObjectProxy

from pytest_markers import *
from pocopytest.testcase.utils.util_define import SetupDefine
from pocopytest.testcase.utils.ui_define import UIDefine as UI


def allure_snap(snap_off=SetupDefine.SNAP_OFF):
    """
    截图作为allure图片附件,snap_off为截图开关
    """
    if not snap_off:
        allure.attach.file(os.path.join(ST.LOG_DIR, snapshot()), attachment_type=allure.attachment_type.JPG)


def new_poco(poco=None, query=None):
    _obj = UIObjectProxy(poco)
    _obj.query = query
    return _obj


def click_obj(poco=None, query=None, obj_focus=[0.5, 0.5], timeout=8, sleep_time=0.3):
    """
    传入poco+query
    """
    flag = True
    start = time.time()
    while flag:
        with poco.freeze() as frozen_poco:
            _obj = new_poco(frozen_poco, query)
            if _obj.exists():
                flag = False
            frozen_poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('appearance', _obj)
    with allure.step('点击: {0},{1}'.format(_obj, _obj.attr('text'))):
        allure_snap()
        _obj.focus(obj_focus).click()
        sleep(sleep_time)
