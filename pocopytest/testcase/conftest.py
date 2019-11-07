# coding=utf-8

import random

import pytest
from airtest.core.api import *
from airtest.core.win import Windows
from airtest.utils.logger import get_logger
from poco.drivers.unity3d import UnityPoco

from pocopytest.lib.utils.init_app import init_app
from pocopytest.testcase.utils.util import allure_snap, logger
from pocopytest.testcase.utils.util_define import SetupDefine as SD
from pocopytest.lib.utils.atxserver2 import AtxServer2


@pytest.fixture(autouse=True)
def poco(request):
    """相当于setup"""
    logger.info('===conftest poco===')
    logger.debug(f'设置logger(airtest.*)的level为{SD.AIRTEST_LOG_LEVEL}')
    get_logger("airtest").setLevel(SD.AIRTEST_LOG_LEVEL)
    random_time = random.choice(range(1, 5)) * 1 + random.choice(range(10)) * 0.1
    logger.debug(f'random_time={random_time}')
    sleep(random_time)
    dev = init_app()
    logger.debug('初始化poco')
    poco = UnityPoco(addr=("localhost", SD.POCO_PORT))
    request.cls.poco = poco
    yield request.cls.poco
    logger.info('===teardown===')
    logger.debug('结束前截图')
    allure_snap()
    if SD.PLAT == 'android':
        logger.debug('整个测试session结束后，关闭app')
        stop_app(SD.PACKAGE_NAME)
        if SD.USE_ATX_SERVER2:
            atx_server2 = AtxServer2()
            ret = atx_server2.release_device(SD.UDID)
    elif SD.PLAT.find('pc') >= 0:
        pid = dev.stop_app.process
        logger.debug(f'PC平台是结束进程，进程id:{pid}')
        Windows().stop_app(pid)
