# coding=utf-8

import re

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import start_app, stop_app, sleep, wake
from airtest.core.win import Windows
from poco.drivers.unity3d.device import UnityEditorWindow

from pocopytest.lib.utils.installation import install_android_app
from pocopytest.testcase.utils.util import logger


def init_app(plat, package_name, app_path, sleep_time, serialno=None):
    dev = None
    if plat == 'android':
        if serialno and serialno.strip() != '':
            if re.search(r'127.0.0.1:\d+', serialno):
                logger.debug('模拟器用JAVACAP和ADBORI')
                dev = connect_device(f'Android:///{serialno}?cap_method=JAVACAP&ori_method=ADBORI')
            else:
                logger.debug(f'指定连接serialno: {serialno}')
                dev = connect_device(f'Android:///{serialno}')
        else:
            dev = connect_device('Android:///')
        wake()
        install_android_app(current_device().adb, app_path)
        stop_app(package_name)
        logger.debug(f'启动app:{package_name}')
        start_app(package_name)
        sleep(sleep_time / 1.5)
    elif plat == 'pc_editor':
        w = Windows()
        dev = UnityEditorWindow()
        w.keyevent('^P')  # Ctrl+P运行
        sleep(sleep_time / 2)
        dev.stop_app = w.app  # 用于获取进程id，结束进程用
    elif plat == 'pc_win':
        w = Windows()
        w.start_app(app_path)
        sleep(sleep_time)
        w.connect(process=w.app.process)
        dev = connect_device("Windows:///?class_name=UnityWndClass")
        dev.stop_app = w.app
    # elif plat == 'ios':
    #     pass
    # elif plat == 'mac_editor':
    #     pass
    return dev
