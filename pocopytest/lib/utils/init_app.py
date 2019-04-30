# coding=utf-8

import os

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import start_app, stop_app, sleep, wake
from airtest.core.android.adb import ADB
from airtest.core.win import Windows
from poco.drivers.unity3d.device import UnityEditorWindow

from pocopytest.lib.utils.installation import install_android_app
from pocopytest.testcase.utils.util_define import SetupDefine as SD


def init_app(plat, package_name, app_path, sleep_time):
    dev = None
    if plat.lower().find('android') >= 0:
        if not current_device():
            if plat.lower().find('sim') >= 0:
                dev = connect_device('Android:///127.0.0.1:{}?cap_method=JAVACAP&ori_method=ADBORI'.format(SD.SIM_PORT))
            else:
                dev = connect_device('Android:///')
        wake()
        install_android_app(current_device().adb, app_path)
        stop_app(package_name)
        start_app(package_name)
        sleep(sleep_time / 1.5)
    elif plat == 'PC_editor':
        w = Windows()
        dev = UnityEditorWindow()
        w.keyevent('^P')  # Ctrl+P运行
        sleep(sleep_time / 2)
        dev.stop_app = w.app  # 用于获取进程id，结束进程用
    elif plat == 'PC_win':
        w = Windows()
        w.start_app(app_path)
        sleep(sleep_time)
        w.connect(process=w.app.process)
        dev = connect_device("Windows:///?class_name=UnityWndClass")
        dev.stop_app = w.app
    # elif plat == 'iOS':
    #     pass
    # elif plat == 'MAC_editor':
    #     pass
    return dev
