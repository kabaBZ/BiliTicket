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

    token = ""

    def login(self):
        """
        执行登录获取cookie
        """
        session_cookie = BiliLogin().run()
        return session_cookie

    def init_token(self, ticket_info=None):
        """
        获取订单确认页面的token,2024-3-21,不同订单token可以混用
        #     {
        #         "project_id": project_id,
        #         "screen_id": str(screen_id),
        #         "sku_id": str(sku_id),
        #     }
        """
        try:
            self.token = self.bili_api.prepare(
                ticket_info
                or {
                    "project_id": "81422",
                    "screen_id": "162292",
                    "sku_id": "460143",
                }
            )
            if ticket_info:
                print(f"抢票token: {self.token}")
            else:
                print(f"临时token: {self.token}")
        except:
            self.token = ""

    def selected_buyer(self, buyer_info):
        """
        选择购票人信息
        """
        # 获取用户列表
        exist_buyer_list = self.bili_api.get_added_buyer_list()
        for exist_buyer in exist_buyer_list:
            if all(
                [
                    exist_buyer["name"] == buyer_info["name"],
                    exist_buyer["tel"] == buyer_info["tel"],
                    exist_buyer["personal_id"] == buyer_info["personal_id"],
                ]
            ):
                return exist_buyer
        else:
            # 添加用户
            buyer_id = self.bili_api.create_buyer(buyer_info)
            # 获取用户列表
            exist_buyer_list = self.bili_api.get_added_buyer_list()
            for exist_buyer in exist_buyer_list:
                if exist_buyer["id"] == buyer_id:
                    return exist_buyer

    def prepare_mission_info(self, session_cookie=None):
        """
        执行登录获取cookie(传入cookie时不进行登录)

        确定购票信息
        """
        if not session_cookie:
            session_cookie = self.login()
        self.bili_api = BiliApi(session_cookie)
        project_id = input("输入演出id(按回车结束):")  # 81605
        # 获取演出场次及票务信息
        screenlist = self.bili_api.getV2(project_id)
        print(f"本演出共{len(screenlist)}场次")
        for screen in screenlist:
            print(
                f"场次编号：{screenlist.index(screen) + 1}  场次名称：{screen['screen_name']}  screen_id: {screen['screen_id']}"
            )
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

        # token = bili_api.prepare(
        #     {
        #         "project_id": project_id,
        #         "screen_id": str(screen_id),
        #         "sku_id": str(sku_id),
        #     }
        # )
        # 购票人信息
        buyer_info = self.selected_buyer(buyer_info)

        # 根据提前写死的票据信息注册token
        self.init_token()

        start_time_stamp = datetime_to_timestamp(start_time)
        stop_time_stamp = start_time_stamp + 80
        while time.time() < start_time_stamp:
            print("等待抢购")
            time.sleep(0.5)
        if not self.token:
            # 根据抢票信息注册token
            self.init_token(
                {
                    "project_id": project_id,
                    "screen_id": str(screen_id),
                    "sku_id": str(sku_id),
                }
            )
        while True:
            try:
                result = self.bili_api.createV2(
                    {
                        "projectid": project_id,
                        "screenid": str(screen_id),
                        "skuid": str(sku_id),
                        "price": str(price),
                    },
                    buyer_info,
                    self.token,
                )
            except Exception as e:
                print(f"报错：{e}")
                if time.time() > stop_time_stamp:
                    print("时间到")
                    break
                time.sleep(0.1)
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
                    time.sleep(0.1)
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
