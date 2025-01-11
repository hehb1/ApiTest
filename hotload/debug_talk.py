import base64
import hashlib
import time

import rsa
import yaml

from commons.base_url import read_ini
from config import settings


class DebugTalk:
    def read_yaml(self, key):
        """读取extract.yaml中指定的值"""
        with open(settings.extract_name, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)[key]

    def get_random_number(self):
        '''获取时间戳'''
        return str(int(time.time()))

    def md5_encode(self, data):
        '''md5加密'''
        data = str(data).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(data)
        return md5.hexdigest()

    def base64_encode(self, data):
        '''base64加密'''
        data = str(data).encode('utf-8')
        b64 = base64.b64encode(data)
        return b64.decode('utf-8')

    # def create_key(self):
    #     '''创建公钥和私钥，主要是生成格式'''
    #     public_key, private_key = rsa.newkeys(1024)
    #     with open('./public.pem', 'w+') as f:
    #         f.write(public_key.save_pkcs1().decode())
    #     with open('./private.pem', 'w+') as f:
    #         f.write(private_key.save_pkcs1().decode())

    def rsa_decode(self, data):
        '''rsa非对称加密，通过公钥加密 '''
        data = str(data).encode('utf-8')  # 把data转化为utf-8编码格式
        with open('./hotload/public.pem') as f:  # 读取公钥
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        byte_value = rsa.encrypt(data, pubkey)  # 将字符串加密成byte类型
        return base64.b64encode(byte_value).decode('utf-8')  # 将字节转为字符串并返回

    def env(self, key):
        '''从pytest.ini中获取基础路径'''
        return read_ini()[key]
