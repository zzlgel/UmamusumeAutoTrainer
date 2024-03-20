from bot.base.context import BotContext
from module.umamusume.task import UmamusumeTask, UmamusumeTaskType
from module.umamusume.define import *
import bot.base.log as logger

log = logger.get_logger(__name__)


# 支援卡信息
class SupportCardInfo:
    name: str
    card_type: SupportCardType
    favor: SupportCardFavorLevel
    # TODO 是否触发事件？
    has_event: bool

    def __init__(self,
                 name: str = "support_card",
                 card_type: SupportCardType = SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN,
                 favor: SupportCardFavorLevel = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN,
                 has_event: bool = False):
        self.name = name
        self.card_type = card_type
        self.favor = favor
        self.has_event = has_event


# 训练结果信息
class TrainingInfo:
    # 支援卡列表
    support_card_info_list: list[SupportCardInfo]
    speed_incr: int
    stamina_incr: int
    power_incr: int
    will_incr: int
    intelligence_incr: int
    # 技能pt点数
    skill_point_incr: int

    def __init__(self):
        self.speed_incr = 0
        self.stamina_incr = 0
        self.power_incr = 0
        self.will_incr = 0
        self.intelligence_incr = 0
        self.skill_point_incr = 0
        self.support_card_info_list = []

    # 打印训练结果
    def log_training_info(self):
        log.info("训练结果：速度：%s, 耐力：%s, 力量：%s, 毅力：%s, 智力：%s, 技能点：%s", self.speed_incr,
                 self.stamina_incr, self.power_incr, self.will_incr,
                 self.intelligence_incr, self.skill_point_incr)
        text = "此训练附带支援卡列表：["
        for c in self.support_card_info_list:
            if c.favor != SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                text += "[支援卡名称：" + str(c.name) + "支援卡类型：" + str(c.card_type.name) + ", 支援卡羁绊阶段：" + str(c.favor.name) + "] "
        text += "]"
        log.info(text)


# 赛马娘属性
class UmaAttribute:
    speed: int
    stamina: int
    power: int
    will: int
    intelligence: int
    skill_point: int

    def __init__(self):
        self.speed = 0
        self.stamina = 0
        self.power = 0
        self.will = 0
        self.intelligence = 0
        self.skill_point = 0


# 玩家育成操作
class TurnOperation:
    # 执行操作
    turn_operation_type: TurnOperationType
    # 备选操作
    turn_operation_type_replace: TurnOperationType
    # 训练类型
    training_type: TrainingType
    # 比赛id
    race_id: int

    def __init__(self):
        self.turn_operation_type = TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN
        self.turn_operation_type_replace = TurnOperationType.TURN_OPERATION_TYPE_UNKNOWN
        self.training_type = TrainingType.TRAINING_TYPE_UNKNOWN
        self.race_id = 0

    def log_turn_operation(self):
        log.info("本回合执行操作：%s", self.turn_operation_type.name)
        log.info("本回合备选操作：%s", self.turn_operation_type_replace.name)
        if self.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_TRAINING:
            log.info("训练类型：%s", self.training_type.name)


# 操作信息
class TurnInfo:
    # 回合时间
    date: int

    # 分析训练信息是否结束
    parse_train_info_finish: bool
    # 训练结果信息列表
    training_info_list: list[TrainingInfo]
    # 分析主菜单是否结束
    parse_main_menu_finish: bool
    # 赛马娘属性
    uma_attribute: UmaAttribute

    # 剩余体力
    remain_stamina: int
    # 干劲状态
    motivation_level: MotivationLevel
    # 医疗室是否可用
    medic_room_available: bool
    # 赛程是否可用
    race_available: bool

    # 玩家育成操作
    turn_operation: TurnOperation | None
    # 是否记录操作日志
    turn_info_logged: bool
    # 是否学习完技能
    turn_learn_skill_done: bool

    def __init__(self):
        self.date = -1
        self.parse_train_info_finish = False
        self.training_info_list = [TrainingInfo(), TrainingInfo(), TrainingInfo(), TrainingInfo(), TrainingInfo()]
        self.parse_main_menu_finish = False
        self.uma_attribute = UmaAttribute()
        self.remain_stamina = -1
        self.motivation_level = MotivationLevel.MOTIVATION_LEVEL_UNKNOWN
        self.medic_room_available = False
        self.race_available = False
        self.turn_operation = None
        self.turn_info_logged = False
        self.turn_learn_skill_done = False

    def log_turn_info(self):
        log.info("当前回合时间 >" + str(self.date))
        log.info("干劲状态 " + str(self.motivation_level.name))
        log.info("体力剩余" + str(self.remain_stamina))
        log.info("当前属性值 速度：%s, 耐力：%s, 力量：%s, 毅力：%s, 智力：%s, 技能点：%s", self.uma_attribute.speed,
                 self.uma_attribute.stamina, self.uma_attribute.power, self.uma_attribute.will, self.uma_attribute.intelligence, self.uma_attribute.skill_point)
        log.info("速度训练结果：")
        self.training_info_list[0].log_training_info()
        log.info("耐力训练结果：")
        self.training_info_list[1].log_training_info()
        log.info("力量训练结果：")
        self.training_info_list[2].log_training_info()
        log.info("毅力训练结果：")
        self.training_info_list[3].log_training_info()
        log.info("智力训练结果：")
        self.training_info_list[4].log_training_info()


# 培育上下文
class CultivateContextDetail:
    turn_info: TurnInfo | None
    turn_info_history: list[TurnInfo]
    expect_attribute: list[int] | None
    follow_support_card_name: str
    follow_support_card_level: int
    extra_race_list: list[int]
    learn_skill_list: list[list[str]]
    learn_skill_blacklist: list[str]
    learn_skill_done: bool
    learn_skill_selected: bool
    cultivate_finish: bool
    # 跑法列表
    tactic_list: list[int]
    debut_race_win: bool
    clock_use_limit: int
    clock_used: int
    learn_skill_threshold: int
    # 育成中仅允许学习用户提供的技能
    learn_skill_only_user_provided: bool
    learn_skill_before_race: bool
    allow_recover_tp: bool
    parse_factor_done: bool
    extra_weight: list

    def __init__(self):
        self.expect_attribute = None
        self.turn_info = TurnInfo()
        self.turn_info_history = []
        self.extra_race_list = []
        self.learn_skill_list = []
        self.learn_skill_blacklist = []
        self.learn_skill_done = False
        self.learn_skill_selected = False
        self.cultivate_finish = False
        self.tactic_list = []
        self.debut_race_win = False
        self.clock_use_limit = 0
        self.clock_used = 0
        self.allow_recover_tp = False
        self.parse_factor_done = False
        self.extra_weight = []

    def reset_skill_learn(self):
        self.learn_skill_done = False
        self.learn_skill_selected = False


class UmamusumeContext(BotContext):
    task: UmamusumeTask
    cultivate_detail: CultivateContextDetail

    def __init__(self, task, ctrl):
        super().__init__(task, ctrl)

    def is_task_finish(self) -> bool:
        return False


# 赛马娘任务详情添加到赛马娘上下文中
def build_context(task: UmamusumeTask, ctrl) -> UmamusumeContext:
    ctx = UmamusumeContext(task, ctrl)
    if task.task_type == UmamusumeTaskType.UMAMUSUME_TASK_TYPE_CULTIVATE:
        detail = CultivateContextDetail()
        detail.expect_attribute = task.detail.expect_attribute
        detail.follow_support_card_name = task.detail.follow_support_card_name
        detail.follow_support_card_level = task.detail.follow_support_card_level
        detail.extra_race_list = task.detail.extra_race_list
        detail.learn_skill_list = task.detail.learn_skill_list
        detail.learn_skill_blacklist = task.detail.learn_skill_blacklist
        detail.tactic_list = task.detail.tactic_list
        detail.clock_use_limit = task.detail.clock_use_limit
        detail.learn_skill_threshold = task.detail.learn_skill_threshold
        detail.learn_skill_only_user_provided = task.detail.learn_skill_only_user_provided
        detail.allow_recover_tp = task.detail.allow_recover_tp
        detail.extra_weight = task.detail.extra_weight
        ctx.cultivate_detail = detail
    return ctx





