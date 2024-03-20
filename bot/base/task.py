import time
from enum import Enum
from abc import abstractmethod, ABCMeta
import random

import bot.base.log as logger
from bot.base.common import CronJobConfig
from bot.base.const import ALPHA

log = logger.get_logger(__name__)


# 任务执行模式
class TaskExecuteMode(Enum):
    # 无效
    TASK_EXECUTE_MODE_INVALID = 0
    # 一次性任务
    TASK_EXECUTE_MODE_ONE_TIME = 1
    # 定时任务
    TASK_EXECUTE_MODE_CRON_JOB = 2


# 任务状态
class TaskStatus(Enum):
    # 无效
    TASK_STATUS_INVALID = 0
    # 待执行
    TASK_STATUS_PENDING = 1
    # 执行中
    TASK_STATUS_RUNNING = 2
    # 被中断
    TASK_STATUS_INTERRUPT = 3
    # 成功
    TASK_STATUS_SUCCESS = 4
    # 失败
    TASK_STATUS_FAILED = 5
    # 已调度
    TASK_STATUS_SCHEDULED = 6
    # 已取消
    TASK_STATUS_CANCELED = 7


# 任务结束原因
class EndTaskReason(Enum):
    COMPLETE = "任务已完成"
    MANUAL_ABORTED = "任务被手动中止"
    SYSTEM_ERROR = "系统异常"


# 任务基类
class Task(metaclass=ABCMeta):
    # 任务ID
    task_id: str = None
    # 应用名称
    app_name: str = None
    # 任务执行模式
    task_execute_mode: TaskExecuteMode = None
    # 定时任务配置
    cron_job_config: CronJobConfig = None
    # 任务类型
    task_type = None
    # 任务状态
    task_status: TaskStatus = None
    # 任务描述
    task_desc: str = None
    # 任务开始时间
    task_start_time: int = None
    # 任务结束时间
    task_end_time: int = None
    # 任务结束原因
    end_task_reason: EndTaskReason = None

    def __init__(self, app_name: str, task_execute_mode: TaskExecuteMode, task_type,
                 task_desc: str, cron_job_config: CronJobConfig = None):
        # 任务ID = 随机字母5位 + 时间戳
        self.task_id = "".join(random.sample(ALPHA, 5)) + str(int(time.time()))
        self.app_name = app_name
        self.task_execute_mode = task_execute_mode
        self.task_type = task_type
        # 任务执行模式为定时任务时，任务状态为已调度；否则为待执行
        if task_execute_mode == TaskExecuteMode.TASK_EXECUTE_MODE_CRON_JOB:
            self.task_status = TaskStatus.TASK_STATUS_SCHEDULED
        else:
            self.task_status = TaskStatus.TASK_STATUS_PENDING
        self.task_desc = task_desc
        self.cron_job_config = cron_job_config

    @abstractmethod
    def end_task(self, status, reason) -> None:
        log.info("任务结束：" + self.task_status.name + "->" + status.name)
        self.task_status = status
        self.end_task_reason = reason

    @abstractmethod
    def start_task(self) -> None:
        pass

    def running(self) -> bool:
        return self.task_status == TaskStatus.TASK_STATUS_RUNNING

