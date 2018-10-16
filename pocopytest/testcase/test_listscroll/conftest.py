# coding=utf-8

import pytest
from pocopytest.testcase.utils.util import *


@pytest.fixture(scope='module', autouse=True)
def fix_input(poco):
    clickobj(waitobj=poco('beginPanel'), obj=poco('btn_start'))
    clickobj(waitobj=poco('levelSelect'), obj=poco('list_view'), sleep_time=1)
