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
    点击，需传入poco+query
    """
    start = time.time()
    while True:
        with poco.freeze() as frozen_poco:
            _obj = new_poco(frozen_poco, query)
            if _obj.exists():
                break
            poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('appearance', _obj)
    with allure.step('点击: {0},{1}'.format(_obj, _obj.attr('text'))):
        allure_snap()
        _obj.focus(obj_focus).click(sleep_interval=sleep_time)


def input_obj(poco=None, query=None, text='', assert_query=None, timeout=8, sleep_time=0.3):
    """
    输入文字，需传入poco+query, assert_query为需要验证的obj的query
    """
    start = time.time()
    while True:
        with poco.freeze() as frozen_poco:
            _obj = new_poco(frozen_poco, query)
            if _obj.exists():
                break
            poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('appearance', _obj)
    with allure.step('{0},输入: {1}'.format(_obj, text)):
        allure_snap()
        new_poco(poco, query).set_text(text)
        sleep(sleep_time)
        if assert_query:
            asser_obj = new_poco(poco, assert_query)
            assert asser_obj.get_text() == text, '实际输入后和预期不一样'


def scroll_find(poco, query, scrollview_query, per=0.4, dur=0.1, timeout=120, is_vertical=True):
    """
    滚动scrollview直到出现obj，scrollview_query为viewport的obj的query, per是滚动percent, dur是滚动duration
    """
    with poco.freeze() as frozen_poco:
        view_obj = new_poco(frozen_poco, scrollview_query)
    if is_vertical:
        index = 1
        sv_top = view_obj.focus([0.5, 0]).get_position()[index]
        sv_bottom = view_obj.focus([0.5, 1]).get_position()[index]
        direction = 'vertical'
    else:
        index = 0
        sv_top = view_obj.focus([0, 0.5]).get_position()[index]
        sv_bottom = view_obj.focus([1, 0.5]).get_position()[index]
        direction = 'horizontal'
    start_time = time.time()
    while True:
        with poco.freeze() as frozen_poco:
            _obj = new_poco(frozen_poco, query)
            if _obj.exists() and sv_top < _obj.get_position()[index] < sv_bottom:
                return _obj
            view_obj.scroll(direction=direction, percent=per, duration=dur)
            sleep(0.3)
            if timeout and time.time() - start_time > timeout:
                with allure.step('scroll_find超时，没找到目标'):
                    return None
