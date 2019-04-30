# coding=utf-8

import pytest
from airtest.core.api import *
from airtest.core.win import Windows
from poco.drivers.unity3d import UnityPoco

from pocopytest.lib.utils.init_app import init_app
from pocopytest.testcase.utils.util_define import SetupDefine as SD


@pytest.fixture(autouse=True)
def poco(request):
    """相当于setup"""
    plat = SD.PLAT
    if plat.lower().find('pc_editor') >= 0:
        app_path = SD.APP_PATH_PC_EDITOR
    elif plat.lower().find('win') >= 0:
        app_path = SD.APP_PATH_WIN
    else:
        app_path = SD.APP_PATH_ANDROID
    dev = init_app(plat=plat, package_name=SD.PACKAGE_NAME, app_path=app_path, sleep_time=SD.SLEEP_TIME)
    poco = UnityPoco(addr=("localhost", SD.POCO_PORT))  # 初始化poco
    request.cls.poco = poco
    yield request.cls.poco
    # yield语句后面相当于teardown
    if plat.lower().find('android') >= 0:
        stop_app(SD.PACKAGE_NAME)  # 整个测试session结束后，关闭app
    elif plat.lower().find('pc') >= 0:
        Windows().stop_app(dev.stop_app.process)  # PC平台是结束进程
