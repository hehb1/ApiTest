import yaml

from commons.requests_util import logger


# 读取测试数据
def read_testcase(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        case_list = yaml.safe_load(f)
        if len(case_list) > 1:
            print('流程用例')
            return [case_list]   # [[{},{}...]]
        else:
            if 'parametrize' in dict(*case_list).keys():
                print('数据驱动用例')
                new_caseinfo = ddts(*case_list, yaml_path.name)
                return new_caseinfo  # [{},{}...]
            else:
                print('单接口用例')
                return case_list


def ddts(caseinfo: dict, yaml_name):
    '''将含有parametrize的字典{}转化为列表中嵌套字典的数据[{},{}...]'''
    # parametrize:
    # - ['account', 'pwd']
    # - ['baili', 'baili123']
    # - ['baili', 'baili']
    # - ['baili123', 'baili123']
    data_list = caseinfo['parametrize']  # [[],[]...]
    len_flag = True
    name_len = len(data_list[0])  # 第一个列表的长度['account', 'pwd']
    for data in data_list:
        if len(data) != name_len:  # 如果每个列表的长度不一致
            len_flag = False
            logger.error(yaml_name+':parametrize数据长度不一致! \n')
            break
    # str_caseinfo = yaml.safe_dump(caseinfo)
    str_caseinfo = yaml.dump(caseinfo)  # 将caseinfo字典转为字符串
    new_caseinfo = []
    if len_flag:
        for x in range(1, len(data_list)):  # x表示行的索引，从1开始，剔掉第一行
            row_caseinfo = str_caseinfo
            for y in range(0, name_len):   # y表示列索引，从0开始
                # 数字格式的字符串需要加上单引号
                if isinstance(data_list[x][y], str) and data_list[x][y].isdigit():
                    data_list[x][y] = "'"+data_list[x][y]+"'"
                row_caseinfo = row_caseinfo.replace('$ddt{'+data_list[0][y]+'}', str(data_list[x][y]))
            case_dict = yaml.safe_load(row_caseinfo)
            case_dict.pop('parametrize')
            new_caseinfo.append(case_dict)
    return new_caseinfo
