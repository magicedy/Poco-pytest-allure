# coding=utf-8

import random
import logging

import pytest
import allure
from airtest.core.api import *
from airtest.core.win import Windows
from poco.drivers.unity3d import UnityPoco

from pocopytest.lib.utils.init_app import init_app
from pocopytest.testcase.utils.util import allure_snap, get_logger, init_logging
from pocopytest.testcase.utils.util_define import SetupDefine as SD

LOGGING = get_logger(__name__)


@pytest.fixture(autouse=True)
def poco(request):
    """相当于setup"""
    get_logger("airtest").setLevel(SD.AIRTEST_LOG_LEVEL)
    _log_name = __name__.split('.')[0]
    init_logging(name=_log_name, level=SD.TESTCASE_LOG_LEVEL)
    plat = SD.PLAT
    if plat.lower().find('pc_editor') >= 0:
        app_path = SD.APP_PATH_PC_EDITOR
    elif plat.lower().find('win') >= 0:
        app_path = SD.APP_PATH_WIN
    else:
        app_path = SD.APP_PATH_ANDROID
        sleep(random.choice(range(1, 8)) * 1)
        SD().save_dev_status()
        if SD.WORKER_ID:
            LOGGING.info(SD.SERIALNO)
            with allure.step('当前设备：{}'.format(SD.SERIALNO)):
                pass
    dev = init_app(plat=plat, package_name=SD.PACKAGE_NAME, app_path=app_path, sleep_time=SD.SLEEP_TIME,
                   serialno=SD.SERIALNO)
    poco = UnityPoco(addr=("localhost", SD.POCO_PORT))  # 初始化poco
    request.cls.poco = poco
    yield request.cls.poco
    # yield语句后面相当于teardown
    allure_snap()
    if plat.lower().find('android') >= 0:
        stop_app(SD.PACKAGE_NAME)  # 整个测试session结束后，关闭app
        SD().clean_dev_status()
    elif plat.lower().find('pc') >= 0:
        Windows().stop_app(dev.stop_app.process)  # PC平台是结束进程
