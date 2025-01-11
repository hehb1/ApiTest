import jsonpath
from commons.requests_util import RequestsUtil
from commons.yaml_util import write_yaml, read_yaml


class TestShopxo:

    # 首页列表
    def test_start_list(self):
        method = 'post'
        url = 'http://101.34.221.219:8010/api.php'
        params = {
            's': 'index/index',
        }
        res = RequestsUtil().send_all_request(method=method, url=url, params=params)
        print(res.json())

    # 商品详情
    def test_product_detail(self):
        method = 'post'
        url = 'http://101.34.221.219:8010/api.php'
        params = {
            's': 'goods/detail',
        }
        json = {
            'goods_id': '5071',
        }
        res = RequestsUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.text)

    # 登录shopxo
    def test_login_shopxo(self):
        method = 'post'
        url = 'http://101.34.221.219:8010/api.php'
        params = {
            's': 'user/login',
        }
        json = {
            'accounts': 'baili',
            'pwd': 'baili123',
            'verify': 'rib5',
            'type': 'username',
        }
        res = RequestsUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.json())
        data = {'token': jsonpath.jsonpath(res.json(), '$.data.token')[0]}
        write_yaml(data)

    # 订单列表
    def test_order_list(self):
        method = 'post'
        url = 'http://101.34.221.219:8010/api.php'
        params = {
            'token': read_yaml('token'),
            's': 'order/index',
        }
        json = {
            'page': '1',
            'keywords': '',
            'status': '-1',
            'is_more': '1',
        }
        res = RequestsUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.json())

    # 订单详情
    def test_order_detail(self):
        method = 'post'
        url = 'http://101.34.221.219:8010/api.php'
        params = {
            'token': read_yaml('token'),
            's': 'order/detail',
        }
        json = {
            'id': '5071',
        }
        res = RequestsUtil().send_all_request(method=method, url=url, params=params, json=json)
        print(res.json())
