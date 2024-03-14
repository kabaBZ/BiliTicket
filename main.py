from Bilibili.BiliWorker import BiliWorker
import pickle

if __name__ == "__main__":
    # BiliWorker().prepare_mission_info()
    # cookie = BiliLogin().run()
    with open('session_cookie', 'rb') as f:
        cookie = pickle.loads(f.read())
    res = BiliWorker.cookie_is_valid(cookie)
    print(res)