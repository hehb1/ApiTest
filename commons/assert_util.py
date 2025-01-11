import copy

import pymysql

from config import settings


class AssertUtil:

    def conn_database(self):
        '''连接数据库'''
        conn = pymysql.connect(
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            database=settings.db_database,
            port=settings.db_port,
        )
        return conn

    def exec_sql(self, sql):
        '''执行sql'''
        conn = self.conn_database()
        cur = conn.cursor()
        cur.execute(sql)
        value = cur.fetchone()
        cur.close()
        conn.close()
        return value

    def assert_all_case(self, res, assert_type, value):
        '''断言封装'''
        new_res = copy.deepcopy(res)    # 深拷贝一个res
        try:
            new_res.json = new_res.json()     # 把json()的返回赋给json属性
        except Exception:
            new_res.json = {'msg': 'response not json data'}
        # 循环判断断言
        # equal {'断言状态码为200': [200, 'status_code']}
        for msg, yq_and_sj in value.items():
            yq, sj = yq_and_sj[0], yq_and_sj[1]

            # 通过反射获取属性的值
            try:
                sj_value = getattr(new_res, sj)
            except Exception:
                sj_value = sj
            # print(assert_type, msg, yq, sj_value)
            # 进行断言
            match assert_type:
                case 'equals':
                    assert yq == sj_value, msg
                case 'contains':
                    assert yq in sj_value, msg
                case 'db_equals':
                    assert self.exec_sql(yq)[0] == sj_value, msg
                case 'db_contains':
                    assert self.exec_sql(yq)[0] in sj_value, msg





