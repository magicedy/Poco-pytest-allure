# coding=utf-8


import allure
import pytest
from logzero import setup_default_logger
from airtest.core.api import *
from poco.exceptions import *
from poco.proxy import UIObjectProxy

from pocopytest.testcase.utils.util_define import SetupDefine as SD
from pocopytest.testcase.utils.ui_define import UIDefine as UI
from pytest_markers import *

# todo: 待兼容实时输出日志
logger = setup_default_logger(level=SD.TESTCASE_LOG_LEVEL)


def allure_snap(snap_off=SD.SNAP_OFF):
    """
    截图作为allure图片附件,snap_off为是否关闭截图
    """
    if not snap_off:
        allure.attach.file(os.path.join(ST.LOG_DIR, snapshot()), attachment_type=allure.attachment_type.JPG)


def new_poco(poco=None, query=None):
    if poco is None:
        raise Exception('未指定poco实例')
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
    _desc = f'点击: {_obj}, text={_obj.attr("text")}'
    logger.debug(_desc)
    with allure.step(_desc):
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
    _desc = f'{_obj},输入: {text}'
    logger.debug(_desc)
    with allure.step(_desc):
        allure_snap()
        new_poco(poco, query).set_text(text)
        sleep(sleep_time)
        if assert_query:
            asser_obj = new_poco(poco, assert_query)
            logger.debug(f'\n输入: {text}\n显示: {asser_obj.get_text()}')
            try:
                assert asser_obj.get_text() == text, '实际输入后和预期不一样'
            except Exception as e:
                logger.error(e)
                raise e


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
            logger.debug(f'scroll direction:{direction}, percent={per}, duration={dur}')
            view_obj.scroll(direction=direction, percent=per, duration=dur)
            sleep(0.3)
            if timeout and time.time() - start_time > timeout:
                _msg = 'scroll_find超时，没找到目标'
                with allure.step(_msg):
                    logger.warn(_msg)
                    return None


def wait_for_any_in_screen(poco, querys, timeout=120):
    """在屏幕显示范围内wait_for_any"""
    start = time.time()
    while True:
        with poco.freeze() as frozen_poco:
            for query in querys:
                _obj = new_poco(frozen_poco, query)
                if _obj.exists():
                    pos = _obj.attr('pos')
                    if (0 <= pos[0] <= 1) and (0 <= pos[1] <= 1):
                        return _obj
            if time.time() - start > timeout:
                raise PocoTargetTimeout('any to appear', _obj)
            poco.sleep_for_polling_interval()
