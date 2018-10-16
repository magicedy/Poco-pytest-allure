# coding=utf-8

import pytest
from pocopytest.testcase.utils.util import *


@pytest.mark.skip()
@allure.title('测试RPC')
def test_sample1(poco):
    print(rpc(poco, method_name='Dump'))
