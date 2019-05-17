# coding=utf-8

import os

import pytest
from airtest.core.android.adb import ADB


def del_json_file():
    json_file = os.path.join(os.path.dirname(__file__), 'data.json')
    if os.path.isfile(json_file):
        os.remove(json_file)


if __name__ == '__main__':
    devices = [tmp[0] for tmp in ADB().devices()]
    if len(devices) > 0:
        del_json_file()
        pytest.main(['-n {}'.format(len(devices))])
        del_json_file()
    else:
        print('no devices')
