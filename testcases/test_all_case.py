from pathlib import Path
import os

import allure
import pytest

from commons.ddt_util import read_testcase
from commons.extract_util import ExtractUtil
from commons.main_util import stand_case_flow
from commons.model_util import verify_yaml
from commons.requests_util import logger
from config import settings

eu = ExtractUtil()


@allure.epic(settings.allure_project_name)
class TestAllCase:
    pass


# 根据yaml的路径创建测试用例函数并返回
def create_testcase(yaml_path):
    @pytest.mark.parametrize("caseinfo", read_testcase(yaml_path))
    def func(self, caseinfo):
        global case_obj
        if isinstance(caseinfo, list):  # 流程案例
            for case in caseinfo:
                logger.info('YAML文件名:{}'.format(yaml_path.name))
                # 校验caseinfo中的信息，new_caseinfo为一个对象，需要通过'.'来取其属性
                case_obj = verify_yaml(case, yaml_path.name)
                # 用例的标准化流程
                stand_case_flow(case_obj)
        else:
            logger.info('YAML文件名:{}'.format(yaml_path.name))
            # 校验caseinfo中的信息，new_caseinfo为一个对象，需要通过'.'来取其属性
            case_obj = verify_yaml(caseinfo, yaml_path.name)
            # 用例的标准化流程
            stand_case_flow(case_obj)
        # 定制allure报告
        allure.dynamic.feature(case_obj.feature)
        allure.dynamic.story(case_obj.story)
        allure.dynamic.title(case_obj.title)

    return func


testcase_path = Path(__file__).parent  # 获取testcase的路径
yaml_case_list = testcase_path.glob("**/*.yaml")  # 获取testcase下所有yaml文件路径，返回一个生成器对象
# 如果生成的方法顺序有问题，可以执行如下方法
# yaml_case_list = list(yaml_case_list)
# yaml_case_list.sort()
for yaml_path in yaml_case_list:  # 遍历获取yaml文件路径
    # 通过反射原理，每循环一次，在测试类中添加一个测试函数，yaml_path为绝对路径，yaml_case.stem为不带后缀的yaml文件名
    setattr(TestAllCase, 'test_' + yaml_path.stem, create_testcase(yaml_path))


