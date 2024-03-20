import os
import pickle

from Bilibili.BiliLogin import BiliLogin
from Bilibili.BiliWorker import BiliWorker

if __name__ == "__main__":
    if os.path.exists("session_cookie"):
        with open("session_cookie", "rb") as f:
            cookie = pickle.loads(f.read())
        valid = BiliWorker.cookie_is_valid(cookie)
    if not os.path.exists("session_cookie") or not valid:
        cookie = BiliLogin().run()
        with open("session_cookie", "wb") as f:
            f.write(pickle.dumps(cookie))
    BiliWorker().prepare_mission_info(cookie)
