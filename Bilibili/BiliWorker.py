import json
import time
from logging import Logger

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

    def prepare_mission_info(self):
        """
        执行登录获取cookie
        确定购票信息
        """
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
            selected_screen = screenlist[input("请选择场次编号：") - 1]

        screenid = selected_screen["screen_id"]

        print(f"本场次共{len(screenlist)}票种")
        sku_list = selected_screen["sku_list"]
        for sku in sku_list:
            print(f"票种编号：{sku_list.index(sku) + 1}  票种名称：{sku['skuid']}")
        if len(sku_list) == 1:
            print("已选择第一票种")
            selected_sku = sku_list[0]
        else:
            selected_sku = sku_list[input("请选择票种编号：") - 1]

        sku_id = selected_sku["skuid"]
        price = selected_sku["price"]
        bili_api.prepare(
            {
                "project_id": project_id,
                "screen_id": str(screenid),
                "sku_id": str(sku_id),
            }
        )
        input("修改buyer_info.json,保存后按回车")
        with open("./buyer_info.json", "r", encoding="utf-8") as f:
            buyer_info = json.loads(f.read().replace(" ", ""))
        buyer_id = bili_api.create_buyer(buyer_info)
        # # proid 81605  screenid 162526 skuid 461268
        bili_api.confirm_info("82605")
        for buyer in bili_api.buyer_list:
            if str(buyer["id"]) == buyer_id:
                bili_api.buyer = buyer
        # while time.time() < 1709457600:
        while time.time() < 1709459998:
            print("等待抢购")
            time.sleep(0.5)
        while True:
            try:
                result = bili_api.createV2(
                    {
                        "projectid": project_id,
                        "screenid": str(screenid),
                        "skuid": str(sku_id),
                        "price": str(price),
                    },
                    bili_api.buyer,
                )
            except Exception as e:
                print(f"报错：{e}")
                time.sleep(0.05)
                continue
            else:
                if result:
                    print(result)
                    print("锁单成功！！！")
                    break
                else:
                    print(result)
                    if time.time() > 1709460050:
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
        if res and res['isLogin'] is True:
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
