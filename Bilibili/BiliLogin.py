import time
from typing import Union

import requests
from qrcode.main import QRCode
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.sessions import Session

# 在请求前,加入以下代码
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BiliLogin(object):
    def __init__(self):
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0."
        }

    def get_qr_code(self) -> Union[str, str]:
        """获取二维码信息"""
        url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
        res = self.session.get(url, verify=False).json()
        if res["code"] != 0:
            print("获取二维码失败")
            exit(1)
        data = res["data"]["url"]
        key = res["data"]["qrcode_key"]
        return key, data

    def generate_and_show_qr_code(self, data):
        """生成二维码"""
        qrcode = QRCode()
        qrcode.add_data(data)
        qrcode.print_ascii()

    def get_login_status(self, key):
        """获取扫码结果"""
        poll_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
        res = self.session.get(
            poll_url, params={"qrcode_key": key}, verify=False
        ).json()
        return res

    def run(self):
        """登录流程"""
        key, data = self.get_qr_code()
        self.generate_and_show_qr_code(data)
        start = time.time()
        while time.time() - start < 140:
            res = self.get_login_status(key)
            if res["code"] == 0 and res["data"]["code"] == 0:
                break
            time.sleep(1)
        return self.session.cookies
