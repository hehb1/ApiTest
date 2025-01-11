import traceback

from commons.assert_util import AssertUtil
from commons.extract_util import ExtractUtil
from commons.model_util import CaseInfo
from commons.requests_util import RequestsUtil, logger

eu = ExtractUtil()
ru = RequestsUtil()
au = AssertUtil()


def stand_case_flow(case_obj: CaseInfo):
    # 把模块>接口>用例写入日志
    logger.info('模块>接口>用例:'+str(case_obj.feature)+'>'+str(case_obj.story)+'>'+str(case_obj.title))
    # 替换请求数据中的变量,${func()}替换成具体的值
    new_request = eu.change(case_obj.request)
    # 处理数据后统一发送请求
    res = ru.send_all_request(**new_request)
    # 如果yaml文件中有extract关键字，则进行变量提取
    if case_obj.extract:
        for key, value in case_obj.extract.items():
            eu.extract(res, key, *value)
    # 请求之后validate如果不为None，则需要进行断言
    try:
        if case_obj.validate:
            for assert_key, value in eu.change(case_obj.validate).items():
                au.assert_all_case(res, assert_key, value)
            logger.info('断言成功! \n')
        else:
            logger.warning('此用例没有断言! \n')
    except Exception as e:
        logger.error('断言失败! %s', str(traceback.format_exc()))
        raise e
