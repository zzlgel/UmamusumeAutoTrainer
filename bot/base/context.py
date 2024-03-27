from abc import abstractmethod, ABCMeta

from bot.base.resource import UI
from bot.base.task import Task
from bot.conn.ctrl import AndroidController


# BotContext 这个类是所有机器人上下文的基类，它定义了机器人上下文的基本属性和方法。
class BotContext(metaclass=ABCMeta):
    # 表示当前的任务
    task: Task = None
    # 表示当前的控制器,用于控制 Android 设备
    ctrl: AndroidController = None
    # 表示当前的屏幕
    current_screen = None
    # 表示上一个用户界面
    prev_ui: UI = None
    # 表示当前用户界面
    current_ui: UI = None

    # 表示下一个用户界面
    next_ui: UI = None

    # 当前回合是否ocr错误，用来保存当前截屏，为后续优化ocr做参考。
    ocr_error: bool = False

    def __init__(self, task: Task, ctrl: AndroidController):
        self.task = task
        self.ctrl = ctrl

    # 这个方法用于判断当前任务是否完成
    @abstractmethod
    def is_task_finish(self) -> bool:
        pass
