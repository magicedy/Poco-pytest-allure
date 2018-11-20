# coding=utf-8

import allure
from airtest.core.api import *
from poco.exceptions import *
from poco.utils.simplerpc.utils import sync_wrapper


# 截图作为allure图片附件
def allure_snap(switch=True):
    if switch:
        allure.attach.file(snapshot(), attachment_type=allure.attachment_type.JPG)


# 等待waitobj出现(timeout超时)，再点击obj，再等待sleep_time
def clickobj(waitobj, obj, obj_focus=[0.5, 0.5], timeout=1, sleep_time=0.3, show_error=False):
    try:
        waitobj.wait_for_appearance(timeout)
        with allure.step('点击: {0},{1}'.format(obj.attr('name'), obj.attr('text'))):
            allure_snap()
            obj.focus(obj_focus).click()
            sleep(sleep_time)
            return obj.get_position()
    except PocoTargetTimeout as e:
        if show_error:
            print('PocoTargetTimeout:', timeout, e)
    except PocoNoSuchNodeException as e:
        if show_error:
            print('PocoNoSuchNodeException:', e)


# 测试RPC
@allure.step('测试dump')
@sync_wrapper
def rpc(poco, method_name):
    return poco.agent.c.call(method_name, True)
