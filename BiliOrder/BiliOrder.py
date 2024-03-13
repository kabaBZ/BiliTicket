import json
import time
import re

from BiliOrder.BiliBrowser import BiliBrowser


class BiliApi(object):
    def __init__(self, cookies):
        self.seession = BiliBrowser(cookies)
        self.userid = None
        self.init_login_info()

    def init_login_info(self):
        login_info = self.get_login_info()
        self.username = login_info.get("uname")
        self.userid = login_info.get("mid")

    def parse_response(self, response):
        response_dict = json.loads(response.text)
        if response_dict.get("errno") == 0 or response_dict.get("code") == 0:
            return response_dict["data"]
        else:
            msg = response_dict.get("message", "") or response_dict.get("msg", "")
            print("error!!!:" + msg)
            if "已超过购买数量" in msg or "存在待付款订单" in msg:
                print(f"{msg},锁单成功")
                return True
            return False

    def create_buyer(self, buyerInfo) -> str:
        """
        buyerInfo = {
            "name": "郭江斌",
            "tel": "18100176722",
            "id_type": "0",
            "personal_id": "130102199604160311",
            "is_default": "0",
            "src": "ticket",
        }
        """
        self.seession.headers.update(
            {
                "authority": "show.bilibili.com",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://show.bilibili.com",
                "pragma": "no-cache",
            }
        )
        res = self.seession.postRequest(
            "https://show.bilibili.com/api/ticket/buyer/create", data=buyerInfo
        )
        res = self.parse_response(res)
        if res:
            self.buyerid = res["id"]
            print("创建购买人成功")
            return self.buyerid

    def get_login_info(self):
        self.seession.headers.update(
            {
                "origin": "https://t.bilibili.com",
                "pragma": "no-cache",
                "referer": "https://t.bilibili.com/",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            }
        )
        res = self.seession.getRequest("https://api.bilibili.com/x/web-interface/nav")
        res = self.parse_response(res)
        return res

    def getV2(self, projectid):
        """
        获取skuid
        """
        params = {
            "version": "134",
            "id": projectid,
            "project_id": projectid,
            "requestSource": "pc-new",
        }
        self.seession.headers.update(
            {
                "authority": "show.bilibili.com",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "referer": f"https://show.bilibili.com/platform/detail.html?id={projectid}&from=pc_search_sug",
            }
        )
        response = self.seession.getRequest(
            "https://show.bilibili.com/api/ticket/project/getV2",
            params=params,
        )
        res = self.parse_response(response)
        screen_list = []
        for screen in res["screen_list"]:
            sku_list = []
            for sku in res["screen_list"][0]["ticket_list"]:
                sku_list.append(
                    {
                        "skuid": sku["id"],
                        "name": sku["desc"],
                        "price": sku["price"],
                        "startTime": sku["sale_start"],
                        "endTime": sku["sale_end"],
                    }
                )
            screen_list.append(
                {
                    "screen_id": screen["id"],
                    "screen_name": screen["name"],
                    "sku_list": sku_list,
                }
            )

        return screen_list

    def confirm_order(self, project_id):
        """
        提交订单前的确认页面,响应数据中存在buyerid
        """
        self.seession.headers.update(
            {
                "authority": "show.bilibili.com",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            }
        )
        params = {
            "token": self.token,
            "voucher": "",
            "project_id": project_id,
            "requestSource": "pc-new",
        }
        response = self.seession.getRequest(
            "https://show.bilibili.com/api/ticket/order/confirmInfo", params=params
        )
        res = self.parse_response(response)
        self.buyer_list = res["buyerList"]["list"]
        return self.buyer_list

    def createV2(self, tikect_info, buyer_Info):
        """
        创建订单
        """
        self.encoded_deviceId = re.findall(
            "buvid3=(.*?); b_nut", self.seession.cookies
        )[0]

        if "feSign" in self.seession.cookies:
            self.decoded_deviceId = re.findall(
                "feSign=(.*?); payParams", self.seession.cookies
            )[0]
        else:
            self.decoded_deviceId = re.findall(
                "deviceFingerprint=(.*?); from", self.seession.cookies
            )[0]

        self.seession.headers.update(
            {
                "authority": "show.bilibili.com",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/x-www-form-urlencoded",
                "x-risk-header": f"platform/pc uid/{self.userid} deviceId/{self.encoded_deviceId}",
            }
        )
        params = {
            "project_id": tikect_info["projectid"],
        }
        timestamp = time.time() * 1000
        origin = timestamp - 4000
        data = {
            "project_id": tikect_info["projectid"],
            "screen_id": tikect_info["screenid"],
            "sku_id": tikect_info["skuid"],
            "count": "1",
            "pay_money": tikect_info["price"],
            "order_type": "1",
            "timestamp": timestamp,
            "buyer_info": json.dumps([buyer_Info], separators=(",", ":")),
            "token": self.token,
            # todo 将deviceId换成从cookie中取deviceFingerprint
            "deviceId": self.decoded_deviceId,
            "clickPosition": f'{{"x":1337,"y":364,"origin":{origin},"now":{timestamp}}}',
            "newRisk": "true",
            "requestSource": "pc-new",
        }
        response = self.seession.postRequest(
            "https://show.bilibili.com/api/ticket/order/createV2",
            params=params,
            data=data,
            time_out=0.3,
        )
        res = self.parse_response(response)
        return res
