# coding=utf-8

import os
import logging
from configparser import RawConfigParser

from dotenv import load_dotenv, find_dotenv
from airtest.core.api import ST

from logzero import logger


def convert_to_boolean(value):
    """Return a boolean value translating from other types if necessary."""
    boolean_states = RawConfigParser.BOOLEAN_STATES
    if isinstance(value, bool):
        return value
    elif value.lower() not in boolean_states:
        raise ValueError(f'Not a boolean: {value}')
    return boolean_states[value.lower()]


logger.debug('dotenv读取.env文件里的配置作为环境变量')
load_dotenv(find_dotenv())


class SetupDefine(object):
    AIRTEST_LOG_LEVEL = logging.WARN  # logger(airtest.*)的level
    TESTCASE_LOG_LEVEL = logging.DEBUG  # logger(testcase.*)的level
    ST.PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../../../')
    ST.LOG_DIR = os.path.join(ST.PROJECT_ROOT, 'allure_pytest_results')
    PLAT = os.getenv('PLAT', 'Android').lower()  # 平台'Android','PC_win','PC_editor','iOS','MAC_editor'
    POCO_PORT = int(os.getenv('POCO_PORT', '5001'))  # poco-sdk端口
    SLEEP_TIME = float(os.getenv('SLEEP_TIME', 8))  # 启动app后等待时间
    SERIALNO = os.getenv('SERIALNO', None)
    SNAP_OFF = convert_to_boolean(os.getenv('SNAP_OFF', 'false'))  # 是否关闭截图
    """
    https://poco.readthedocs.io/zh_CN/latest/source/doc/poco-example/index.html
    http://top.gdl.netease.com/poco-res/poco-demo-unity-game-android.zip
    http://top.gdl.netease.com/poco-res/poco-demo-unity-game-win.zip
    """
    PACKAGE_NAME = os.getenv('PACKAGE_NAME', 'com.NetEase')
    APP_PATH_ANDROID = os.getenv('APP_PATH_ANDROID', 'C:\\smb\\tmp\\com.netease.poco.u3d.tutorial.apk')
    APP_PATH_WIN = os.getenv('APP_PATH_WIN',
                             'C:\\smb\\tmp\\poco-demo-unity-game-win\\com.netease.poco.u3d.tutorial.exe')
    APP_PATH_PC_EDITOR = os.getenv('APP_PATH_PC_EDITOR',
                                   'C:\\Program Files\\Unity\\Editor\\Unity.exe -projectPath C:\\xxx')
    APP_PATH = {
        'android': APP_PATH_ANDROID,
        'pc_win': APP_PATH_WIN,
        'pc_editor': APP_PATH_PC_EDITOR,
    }
