from requests.sessions import Session


class BiliBrowser(object):
    def __init__(self, cookies):
        self.seession = Session()
        self.seession.cookies = cookies
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0."
        self.headers = {
            "User-Agent": self.ua,
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
        }

    def get_cookie_str(self):
        return ";".join(
            [f"{key}={value}" for key, value in self.seession.cookies.items()]
        )

    def getRequest(self, url: str, data: dict = {}, params: dict = {}) -> str:
        self.seession.headers = self.headers
        response = self.seession.get(url, params=params, data=data)
        return response

    def postRequest(
        self, url: str, data: dict = {}, params: dict = {}, time_out=3
    ) -> str:
        self.seession.headers = self.headers
        response = self.seession.post(url, params=params, data=data, timeout=time_out)
        return response
