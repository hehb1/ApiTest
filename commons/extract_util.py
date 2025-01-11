import copy
import re
from string import Template

import jsonpath
import yaml

from commons.yaml_util import write_yaml
from hotload.debug_talk import DebugTalk


class ExtractUtil:
    def extract(self, res, var_name, attr_name, expr: str, index):
        '''提取变量'''
        # access_token: [json, '$.access_token', 0]
        new_res = copy.deepcopy(res)  # 深拷贝一个响应对象
        try:
            new_res.json = new_res.json()  # 新建一个json属性，指向json()返回
        except:
            new_res.json = {'msg': 'response not json data'}
        # 通过反射获取响应对象的属性
        data = getattr(new_res, attr_name)
        if expr.startswith('$'):  # 如果表达式expr已$开头，则表示使用jsonpath提取
            arr = jsonpath.jsonpath(dict(data), expr)
        else:  # 否则使用正则提取
            arr = re.findall(expr, data)
        if arr:  # 将提取到的变量写入extract.yaml文件中
            write_yaml({var_name: arr[index]})

    def change(self, request_data: dict):
        '''使用变量的值'''
        # 把字典转为字符串
        data_str = yaml.safe_dump(request_data)
        # 使用Template对象的方法替换data_str中所有的变量，此种方法yaml中引用变量的格式${val}
        # new_request_str = Template(data_str).safe_substitute(read_all())
        # 使用自定义的热加载方法替换data_str中所有的变量，此种方法yaml中引用变量的格式为${func(arg1, arg2..)}
        new_request_str = self.hotload_replace(data_str)
        # 将字符串还原为字典并返回
        return yaml.safe_load(new_request_str)

    def hotload_replace(self, data_str: str):
        # 定义一个正则来匹配正则表达式
        regexp = '\\$\\{(.*?)\\((.*?)\\)\\}'
        # fun_list为一个列表，如[('read_yaml', 'token'),('add', '1,2'),('get_random_number','')]
        fun_list = re.findall(regexp, data_str)
        # f为一个元组，第一个元素为方法名，第二个元素为参数，参数使用逗号分隔，也可以为空
        for f in fun_list:
            if f[1] == '':  # 没有参数
                new_value = getattr(DebugTalk(), f[0])()
            else:  # 有参数
                new_value = getattr(DebugTalk(), f[0])(*f[1].split(','))
            # 如果value是数字格式的字符串，加上单引号
            if isinstance(new_value, str) and new_value.isdigit():
                new_value = "'" + new_value + "'"
            # 替换掉字符串中的热加载数据
            old_value = '${'+f[0]+'('+f[1]+')}'
            data_str = data_str.replace(old_value, str(new_value))
        return data_str




if __name__ == '__main__':
    str1 = {'a':'${read_yaml(access_token)}', 'b':'${get_random_number()}'}
    aa = yaml.safe_dump(str1)
    aa = ExtractUtil().hotload_replace(aa)
    bb = yaml.safe_load(aa)
    print(type(bb['a']))


