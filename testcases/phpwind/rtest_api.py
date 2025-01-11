import json
import random

import pytest
import requests

from commons.requests_util import RequestsUtil
from commons.yaml_util import read_testcase, write_yaml, read_yaml


class TestApi:

    @pytest.mark.parametrize("caseinfo", read_testcase('./testcases/phpwind/get_token.yaml'))
    def test_get_token(self, caseinfo):
        method = caseinfo['request']['method']
        url = caseinfo['request']['url']
        params = caseinfo['request']['params']
        res = RequestsUtil().send_all_request(method=method, url=url, params=params)
        data = {'access_token': res.json()['access_token']}
        write_yaml(data)
        print(res.json())


    # 查询标签
    def test_select_flag(self):
        url = "https://api.weixin.qq.com/cgi-bin/tags/get"
        params = {
            "access_token": read_yaml('access_token')
        }
        res = RequestsUtil().send_all_request(method="get", url=url, params=params)
        print(json.loads(json.dumps(res.json()).replace(r"\\", "\\")))



    # 编辑标签
    def test_edit_flag(self):
        url = "https://api.weixin.qq.com/cgi-bin/tags/update?access_token=" + TestApi.token
        json1 = {
            "tag": {"id": "3830", "name": "杭州" + str(random.randint(1000, 9999))}
        }
        res = RequestsUtil().send_all_request(method="post", url=url, json=json1)

    # 上传文件
    def test_upload_files(self):
        method = 'post'
        url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {'access_token': read_yaml('access_token')}
        files = {'media': 'E:\\picture\\unsave.jpg'}
        res = RequestsUtil().send_all_request(method=method, url=url, params=params, files=files)
        print(res.text)
