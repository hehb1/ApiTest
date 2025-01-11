import yaml

from config import settings


# 写入
def write_yaml(data):
    with open(settings.extract_name, 'a+', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


# 读取
def read_yaml(key):
    with open(settings.extract_name, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)[key]


# 读取extract.yaml中所有的值
def read_all():
    with open(settings.extract_name, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# 清空
def truncate_yaml():
    with open(settings.extract_name, 'w', encoding='utf-8') as f:
        f.truncate()



