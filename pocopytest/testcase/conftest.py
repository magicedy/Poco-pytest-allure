# coding=utf-8

import pytest
from airtest.core.api import *
from airtest.core.win import Windows
from poco.drivers.unity3d import UnityPoco
from pocopytest.lib.utils.init_app import init_app


# 相当于setup
@pytest.fixture(scope='module', autouse=True)  # 每个模块只运行一次
def poco():
    # 平台'Android','Android-sim','PC_win','PC_editor','iOS','MAC_editor'
    plat = os.environ.get('Air_plat', 'Android')
    sleeptime = os.environ.get('Air_sleeptime', 10)  # 启动app后等待时间
    sim_port = int(os.environ.get('Air_sim_port', '7555'))  # 安卓模拟器端口,7555对应mumu模拟器
    poco_port = os.environ.get('Air_sim_port', 5001)  # poco-sdk端口
    ST.LOG_DIR = "Poco-pytest-allure/allure_pytest_results"
    package_name = None
    app_path = None
    if plat == 'Android' or plat == 'Android-sim':
        # from https://poco.readthedocs.io/zh_CN/latest/source/doc/poco-example/index.html
        # http://top.gdl.netease.com/poco-res/poco-demo-unity-game-android.zip
        package_name = 'com.netease.poco.u3d.tutorial'
        app_path = r'C:\com.netease.poco.u3d.tutorial.apk'
    elif plat == 'PC_win':
        # http://top.gdl.netease.com/poco-res/poco-demo-unity-game-win.zip
        app_path = r'c:\poco-demo-unity-game-win\com.netease.poco.u3d.tutorial.exe'
        pass
    elif plat == 'PC_editor':
        app_path = r'C:\Program Files\Unity\Editor\Unity.exe -projectPath C:\xxx'  # U3D工程目录
    app = init_app(plat=plat, sim_port=sim_port, package_name=package_name, app_path=app_path,
                   sleeptime=sleeptime)  # 启动app
    poco = UnityPoco(addr=("localhost", poco_port))  # 初始化poco
    yield poco
    # yield语句后面相当于teardown
    if plat == 'Android' or plat == 'Android-sim':
        stop_app(package_name)  # 整个测试session结束后，关闭app
    elif plat == 'PC_win' or plat == 'PC_editor':
        Windows().stop_app(app.process)  # PC平台是结束进程
