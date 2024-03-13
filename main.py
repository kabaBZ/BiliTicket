from Bilibili.BiliApi import BiliApi
from Bilibili.BiliLogin import BiliLogin
import json
import time

if __name__ == "__main__":
    cookie = BiliLogin().run()

    Order = BiliApi(cookie)
