# coding=utf-8

import os
from airtest.core.api import device as current_device, connect_device
from airtest.core.api import start_app, stop_app, sleep
from airtest.core.android.adb import ADB
from airtest.core.win import Windows
from pocopytest.lib.utils.installation import install_android_app


# 连接安卓模拟器
def connect_sim(sim_port):
    sim_ipport = '127.0.0.1:{}'.format(sim_port)
    ADB().cmd('connect {}'.format(sim_ipport), device=False)  # 实际就是adb conncect 127.0.0.1:port,adb用的是airtest自带的
    connect_device(
        'Android://127.0.0.1:5037/{}?cap_method=JAVACAP&ori_method=ADBORI'.format(sim_ipport))  # 模拟器用JAVACAP和ADBORI


def init_app(plat, sim_port, package_name, app_path, sleeptime):
    if plat == 'Android':
        if not current_device():
            serialno = os.environ.get("Air_serialno", None)  #
            if serialno:
                ADB().cmd('connect {}'.format(serialno), device=False)  # 实际就是adb conncect XXX,adb用的是airtest自带的
                connect_device('Android://127.0.0.1:5037/{}'.format(serialno))
            else:
                connect_device('Android:///')
        install_android_app(current_device().adb, app_path)
        stop_app(package_name)
        start_app(package_name)
        sleep(sleeptime)
    elif plat == 'Android-sim':
        if not current_device():
            connect_sim(sim_port)
        install_android_app(current_device().adb, app_path)
        stop_app(package_name)
        start_app(package_name)
        sleep(sleeptime)
    elif plat == 'PC_editor':
        w = Windows()
        w.start_app(app_path)
        sleep(sleeptime)
        w.keyevent('^P')  # Ctrl+P运行
        sleep(sleeptime)
        w.connect(process=w.app.process)
        dev = connect_device("Windows:///?class_name=UnityContainerWndClass&title_re=Unity.*")
        game_window = dev.app.top_window().child_window(title="UnityEditor.GameView")
        dev._top_window = game_window.wrapper_object()
        dev.focus_rect = (0, 40, 0, 0)
        return w.app  # 用于获取进程id，结束进程用
    elif plat == 'PC_win':
        w = Windows()
        w.start_app(app_path)
        sleep(sleeptime)
        w.connect(process=w.app.process)
        connect_device("Windows:///?class_name=UnityWndClass")
        return w.app
    elif plat == 'iOS':
        pass
    elif plat == 'MAC_editor':
        pass
