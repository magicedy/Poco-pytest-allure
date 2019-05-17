# coding=utf-8

import os
import json
import time
import random

from airtest.core.api import ST
from airtest.core.android.adb import ADB


class SetupDefine(object):
    PLAT = 'Android'  # 平台'Android','PC_win','PC_editor','iOS','MAC_editor'
    POCO_PORT = 5001  # poco-sdk端口
    SLEEP_TIME = 8  # 启动app后等待时间
    ST.PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../../../')
    ST.LOG_DIR = os.path.join(ST.PROJECT_ROOT, 'allure_pytest_results')
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

    JSON_FILE = os.path.join(ST.PROJECT_ROOT, 'data.json')
    SERIALNO = None

    def load_json_data(self):
        if os.path.isfile(self.JSON_FILE):
            data = json.load(open(self.JSON_FILE))
            data['start'] = time.time()
        else:
            data = {
                'start': time.time(),
                'tests': {}
            }
            devices = [tmp[0] for tmp in ADB().devices()]
            for dev in devices:
                data['tests'][dev] = {
                    'status': 0
                }
        return data

    def save_dev_status(self):
        data = self.load_json_data()
        devs = [dev for dev in data['tests'].keys() if data['tests'][dev]['status'] == 0]
        dev = random.choice(devs)
        SetupDefine.SERIALNO = dev
        data['tests'][dev]['status'] = 1
        json.dump(data, open(self.JSON_FILE, "w"), indent=4)

    def clean_dev_status(self):
        data = self.load_json_data()
        data['tests'][SetupDefine.SERIALNO]['status'] = 0
        json.dump(data, open(self.JSON_FILE, "w"), indent=4)
