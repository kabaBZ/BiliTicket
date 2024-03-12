import time

import requests
from qrcode.main import QRCode
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.sessions import Session

# 在请求前,加入以下代码
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

Bili_session = Session()


# 获取二维码
url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
headers = {
    "User-Agent": "PostmanRuntime-ApipostRuntime/1.1.0",
}
res = Bili_session.get(url, headers=headers, verify=False).json()

if res["code"] != 0:
    print("获取二维码失败")
    exit(1)



start = time.time()
key = res["data"]["qrcode_key"]
# 构建二维码
data = res["data"]["url"]
qrcode = QRCode()
qrcode.add_data(data)
qrcode.print_ascii()

# 获取扫码结果
poll_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"

while time.time() - start < 140:
    res = Bili_session.get(
        poll_url, params={"qrcode_key": key}, headers=headers, verify=False
    ).json()
    if res["code"] == 0 and res["data"]["code"] == 0:
        break
    # print(res["data"]['message'])
    time.sleep(1)

print(Bili_session.cookies)
