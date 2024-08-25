from abc import abstractmethod


class BaseWorker(object):
    @abstractmethod
    def prepare_mission_info(self):
        """
        准备cookie
        确定购票信息
        """
        pass

    @abstractmethod
    def cookie_is_valid(self, cookie):
        """
        判断cookie是否有效
        """
        pass

    @abstractmethod
    def act(self, cookie, mission_info):
        """
        判断cookie存活状态
        轮询等待抢票时间
        轮询接口抢票
        返回抢购结果
        第三方推送抢购结果信息
        """
        pass
