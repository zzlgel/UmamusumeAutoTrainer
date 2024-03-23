from enum import Enum


class Area:
    # 左上角坐标
    x1: int = None
    y1: int = None
    # 右下角坐标
    x2: int = None
    y2: int = None

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class ImageMatchMode(Enum):
    # 模板匹配
    IMAGE_MATCH_MODE_TEMPLATE_MATCH = 0
    # 特征点匹配
    IMAGE_MATCH_MODE_FEATURE_MATCH = 1


class ImageMatchConfig:
    # 匹配区域
    match_area: Area
    # 匹配模式
    match_mode: ImageMatchMode
    # 匹配精度
    match_accuracy: float

    def __init__(self, match_area: Area = Area(0, 0, 720, 1280),
                 match_mode: ImageMatchMode = ImageMatchMode.IMAGE_MATCH_MODE_TEMPLATE_MATCH,
                 match_accuracy: float = 0.9):
        self.match_area = match_area
        self.match_mode = match_mode
        self.match_accuracy = match_accuracy


# 坐标
class Coordinate:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y


# 定时任务设置
class CronJobConfig:
    cron = None
    next_time = None
    last_time = None


# 定时设置
class CronConfig:
    cron = None
    times = None

    def __init__(self, cron, times):
        self.cron = cron
        self.times = times
