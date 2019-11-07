#!/use/bin/env python
# coding: utf-8

import os
import re
import time
from pprint import pformat

import requests
from airtest.utils.logger import get_logger

logger = get_logger(__name__)


class AtxServer2:
    def __init__(self):
        self.server_url = os.getenv('ATX_SERVER2_URL')
        self.token = os.getenv('ATX_SERVER2_TOKEN')

    def make_url(self, path):
        if re.match(r"^https?://", path):
            return path
        return self.server_url + path

    def request_api(self, path, method="GET", **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + self.token}
        r = requests.request(method, self.make_url(path), **kwargs)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            logger.debug(pformat(r.text))
            raise
        return r.json()

    def get_usable_device_list(self, timeout=60):
        ret = self.request_api("/api/v1/devices", params={"usable": "true"})
        if not ret['devices']:
            ret_colding = self.request_api("/api/v1/devices", params={"using": "false", "colding": "true"})
            if not ret_colding['devices']:
                raise EnvironmentError("No usable devices on atx-server2")
            else:
                start_time = time.time()
                while True:
                    ret = self.request_api("/api/v1/devices", params={"usable": "true"})
                    if ret['devices']:
                        break
                    time.sleep(1.5)
                    if time.time() - start_time > timeout:
                        raise EnvironmentError("No usable devices on atx-server2, after wait")
        logger.debug(f"Device count: {ret['count']}")
        return ret['devices']

    def get_usable_device_info(self):
        device = self.get_usable_device_list()[0]
        udid = device['udid']
        logger.info(f"Choose device: \"{device['properties']['name']}\", udid={udid}")
        ret = self.request_api("/api/v1/user/devices",
                               method="post",
                               json={"udid": udid})
        logger.debug(ret)
        ret = self.request_api("/api/v1/user/devices/" + udid)
        ret['device']['udid'] = udid
        device_info = ret['device']
        # logger.debug(f"atx-server2 device info:\n{pformat(device_info)}")
        return device_info

    def release_device(self, udid):
        ret = self.request_api("/api/v1/user/devices/" + udid, method="delete")
        logger.debug(ret)
