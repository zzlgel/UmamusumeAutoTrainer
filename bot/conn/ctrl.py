from abc import ABCMeta

from bot.base.point import ClickPoint


# 这是一个抽象类，用于定义AndroidController的接口
class AndroidController(metaclass=ABCMeta):

    def init_env(self):
        pass

    # 通过坐标点击
    def click_by_point(self, point: ClickPoint):
        pass

    def click(self, x, y, name):
        pass

    # 滑动
    def swipe(self, x1, y1, x2, y2, duration, name):
        pass

    def destroy(self):
        pass

    def start_app(self, name):
        pass

    def stop_app(self, name):
        pass

    def get_screen(self, to_gray=False):
        pass


