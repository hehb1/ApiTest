from dataclasses import dataclass

from commons.requests_util import logger


@dataclass
class CaseInfo:
    feature: str  # 模块
    story: str  # 接口
    title: str  # 标题
    request: dict  # 请求数据
    validate: dict  # 断言
    extract: dict = None  # 提取内容(选填)
    parametrize: list = None  # 参数化


def verify_yaml(caseinfo: dict, yaml_name):
    try:
        new_caseinfo = CaseInfo(**caseinfo)
        return new_caseinfo
    except Exception:
        logger.error(yaml_name + ':YAML格式不规范!'+'\n')
        raise Exception('YAML格式不规范!')
