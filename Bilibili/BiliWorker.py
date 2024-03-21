import json
import time
from logging import Logger
from Common.Utils import datetime_to_timestamp

from Bilibili.BiliApi import BiliApi
from Bilibili.BiliLogin import BiliLogin
from Common.BaseWorker import BaseWorker


class BiliWorker(BaseWorker):
    """
    B站抢票器任务类
    """

    def login(self):
        """
        执行登录获取cookie
        """
        session_cookie = BiliLogin().run()
        return session_cookie

    def prepare_mission_info(self, session_cookie=None):
        """
        执行登录获取cookie(传入cookie时不进行登录)

        确定购票信息
        """
        if not session_cookie:
            session_cookie = self.login()
        bili_api = BiliApi(session_cookie)
        project_id = input("输入演出id(按回车结束):")  # 81605
        # 获取演出场次及票务信息
        screenlist = bili_api.getV2(project_id)
        print(f"本演出共{len(screenlist)}场次")
        for screen in screenlist:
            print(f"场次编号：{screenlist.index(screen) + 1}  场次名称：{screen['screen_name']}")
        if len(screenlist) == 1:
            print("已选择第一场次")
            selected_screen = screenlist[0]
        else:
            selected_screen = screenlist[int(input("请选择场次编号：")) - 1]

        screen_id = selected_screen["screen_id"]

        print(f"本场次共{len(screenlist)}票种")
        sku_list = selected_screen["sku_list"]
        for sku in sku_list:
            print(
                f"票种编号：{sku_list.index(sku) + 1}  票种名称：{sku['name']} - ￥{sku['price']/100}  票种SKUid：{sku['skuid']}"
            )
        if len(sku_list) == 1:
            print("已选择第一票种")
            selected_sku = sku_list[0]
        else:
            selected_sku = sku_list[int(input("请选择票种编号：")) - 1]

        sku_id = selected_sku["skuid"]
        start_time = selected_sku["startTime"]
        price = selected_sku["price"]

        input("修改buyer_info.json,保存后按回车")
        with open("./buyer_info.json", "r", encoding="utf-8") as f:
            buyer_info = json.loads(f.read().replace(" ", ""))

        token = bili_api.prepare(
            {
                "project_id": project_id,
                "screen_id": str(screen_id),
                "sku_id": str(sku_id),
            }
        )
        buyer_id = bili_api.create_buyer(buyer_info)
        buyer_list = bili_api.confirm_info("81422", token)

        for buyer in buyer_list:
            if str(buyer["id"]) == buyer_id:
                bili_api.buyer = buyer
        start_time_stamp = datetime_to_timestamp(start_time)
        stop_time_stamp = start_time_stamp + 80
        while time.time() < start_time_stamp:
            print("等待抢购")
            time.sleep(0.5)
        while True:
            try:
                result = bili_api.createV2(
                    {
                        "projectid": project_id,
                        "screenid": str(screen_id),
                        "skuid": str(sku_id),
                        "price": str(price),
                    },
                    bili_api.buyer,
                    token,
                )
            except Exception as e:
                print(f"报错：{e}")
                if time.time() > stop_time_stamp:
                    print("时间到")
                    break
                time.sleep(0.05)
                continue
            else:
                if result:
                    print(result)
                    print("锁单成功！！！")
                    break
                else:
                    print(result)
                    if time.time() > stop_time_stamp:
                        print("时间到")
                        break
                    time.sleep(0.05)
                    continue

    @staticmethod
    def cookie_is_valid(cookie):
        """
        判断cookie是否有效
        """
        api = BiliApi(cookie)
        res = api.get_login_info()
        if res and res["isLogin"] is True:
            return True
        return False

    def act(self, cookie, mission_info):
        """
        判断cookie存活状态
        轮询等待抢票时间
        轮询接口抢票
        返回抢购结果
        第三方推送抢购结果信息
        """
        if not self.cookie_is_valid(cookie):
            return False
        pass
