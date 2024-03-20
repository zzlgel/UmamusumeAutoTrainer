from enum import Enum
from bot.base.task import Task, TaskExecuteMode


# 赛马娘任务详情，详看文档 /userdata/umamusume/presets/中预存的文档
class TaskDetail:
    # 剧本名称
    scenario_name: str
    # 期望属性
    expect_attribute: list[int]
    # 借用支援卡名称
    follow_support_card_name: str
    # 借用支援卡等级
    follow_support_card_level: int
    # 额外比赛列表
    extra_race_list: list[int]
    # 学习技能列表
    learn_skill_list: list[list[str]]
    # 学习技能黑名单
    learn_skill_blacklist: list[str]
    # 跑法列表
    tactic_list: list[int]
    # 时钟使用限制
    clock_use_limit: int
    # 育成过程中超过该PT点数阈值后学习技能
    learn_skill_threshold: int
    # 是否仅学习用户提供的技能
    learn_skill_only_user_provided: bool
    # 是否允许恢复TP
    allow_recover_tp: bool
    # 育成结果
    cultivate_result: dict
    cultivate_progress_info: dict
    # 额外权重
    # 调整ai对训练的倾向, 不影响最终目标属性, 一般用于提前完成某一种训练的目标属性。
    # 建议权重范围 [-1.0 ~ 1.0], 0即为不使用额外权重;
    # 支援卡或种马强度低时, 建议增加在一个属性权重的同时减少其他属性同样数值的权重
    extra_weight: list


# 任务结束原因
class EndTaskReason(Enum):
    TP_NOT_ENOUGH = "训练值不足"


# 赛马娘任务
class UmamusumeTask(Task):
    detail: TaskDetail

    def end_task(self, status, reason) -> None:
        super().end_task(status, reason)

    def start_task(self) -> None:
        pass


# 赛马娘任务类型
class UmamusumeTaskType(Enum):
    UMAMUSUME_TASK_TYPE_UNKNOWN = 0
    # 育成
    UMAMUSUME_TASK_TYPE_CULTIVATE = 1


def build_task(task_execute_mode: TaskExecuteMode, task_type: int,
               task_desc: str, cron_job_config: dict, attachment_data: dict) -> UmamusumeTask:
    td = TaskDetail()
    ut = UmamusumeTask(task_execute_mode=task_execute_mode,
                       task_type=UmamusumeTaskType(task_type), task_desc=task_desc, app_name="umamusume")
    ut.cron_job_config = cron_job_config
    td.expect_attribute = attachment_data['expect_attribute']
    td.follow_support_card_level = int(attachment_data['follow_support_card_level'])
    td.follow_support_card_name = attachment_data['follow_support_card_name']
    td.extra_race_list = attachment_data['extra_race_list']
    td.learn_skill_list = attachment_data['learn_skill_list']
    td.learn_skill_blacklist = attachment_data['learn_skill_blacklist']
    td.tactic_list = attachment_data['tactic_list']
    td.clock_use_limit = attachment_data['clock_use_limit']
    td.learn_skill_threshold = attachment_data['learn_skill_threshold']
    td.learn_skill_only_user_provided = attachment_data['learn_skill_only_user_provided']
    td.allow_recover_tp = attachment_data['allow_recover_tp']
    td.extra_weight = attachment_data['extra_weight']
    td.cultivate_result = {}
    # td.scenario_name = attachment_data['scenario_name']
    ut.detail = td
    return ut



