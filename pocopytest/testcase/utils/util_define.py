# coding=utf-8

from airtest.core.api import ST


class SetupDefine(object):
    PLAT = 'PC_win'  # 平台'Android','Android-sim','PC_win','PC_editor','iOS','MAC_editor'
    POCO_PORT = 5001  # poco-sdk端口
    SIM_PORT = 7555  # 安卓模拟器端口,7555对应mumu模拟器
    SLEEP_TIME = 8  # 启动app后等待时间
    ST.LOG_DIR = "./allure_pytest_results"
    SNAP_OFF = False

    """
    https://poco.readthedocs.io/zh_CN/latest/source/doc/poco-example/index.html
    http://top.gdl.netease.com/poco-res/poco-demo-unity-game-android.zip
    http://top.gdl.netease.com/poco-res/poco-demo-unity-game-win.zip
    """
    PACKAGE_NAME = 'com.netease.poco.u3d.tutorial'
    APP_PATH_ANDROID = r'c:\com.netease.poco.u3d.tutorial.apk'
    APP_PATH_WIN = r'c:\poco-demo-unity-game-win\com.netease.poco.u3d.tutorial.exe'
    APP_PATH_PC_EDITOR = r'C:\Program Files\Unity\Editor\Unity.exe -projectPath C:\xxx'  # U3D工程目录
