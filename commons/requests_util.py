import logging

import requests

from config import settings

# 生成日志对象
logger = logging.getLogger(__name__)


class RequestsUtil:
    session = requests.session()

    def send_all_request(self, **kwargs):
        total_params = settings.global_args  # 公共参数
        for key, value in kwargs.items():
            if key == 'params':
                # kwargs['params'].update(total_params)
                value.update(total_params)
            if key == 'files':
                try:
                    for file_key, file_value in value.items():
                        value[file_key] = open(file_value, 'rb')
                except Exception:
                    logger.error('文件路径错误!')
            # 将请求数据写入日志
            logger.info('请求{}参数:{}'.format(key, value))

        res = RequestsUtil.session.request(**kwargs)
        if 'json' in res.headers.get('Content-Type'):
            logger.info('响应数据: %s' % res.json())
        else:
            logger.info('响应数据: %s' % res.text)
        return res
