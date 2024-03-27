from types import FunctionType
from bot.base.context import BotContext
from module.umamusume.task import UmamusumeTask, UmamusumeTaskType
from module.umamusume.define import *
import bot.base.log as logger

log = logger.get_logger(__name__)


# 支援卡信息
class SupportCardInfo:
    name: str
    card_type: SupportCardType
    _favor: SupportCardFavorLevel
    favor_num: int | None
    # TODO 是否触发事件？
    has_event: bool

    def __init__(self,
                 name: str = "support_card",
                 card_type: SupportCardType = SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN,
                 favor: SupportCardFavorLevel = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN,
                 has_event: bool = False,
                 favor_num: int | None = None):
        self.name = name
        self.card_type = card_type
        self._favor = favor
        self.has_event = has_event
        self.favor_num = favor_num

    @property
    def favor(self):
        """分四段，分别是绿松石(<60)，绿(<80)，金（<100），黄绿(100)"""
        if self.favor_num is not None:
            return SupportCardFavorLevel(1 if self.favor_num < 60 else self.favor_num // 20 - 1)
        else:
            return self._favor

    @favor.setter
    def favor(self, favor: SupportCardFavorLevel):
        if self.favor_num is None:
            self._favor = favor

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
    # 体力变化
    vital_incr: int
    # 失败率
    failure_rate: int
    train_level_count: int

    def __init__(self):
        self.speed_incr = 0
        self.stamina_incr = 0
        self.power_incr = 0
        self.will_incr = 0
        self.intelligence_incr = 0
        self.skill_point_incr = 0
        self.support_card_info_list = []
        self.vital_incr = 0
        self.failure_rate = 0

    # 打印训练结果
    def log_training_info(self):
        log.info("训练结果：速度：%s, 耐力：%s, 力量：%s, 毅力：%s, 智力：%s, 技能点：%s, %s体力：%s, 失败率: %3d", self.speed_incr,
                 self.stamina_incr, self.power_incr, self.will_incr,
                 self.intelligence_incr, self.skill_point_incr,
                 "消耗" if self.vital_incr < 0 else "回复" if self.vital_incr > 0 else "",
                 abs(self.vital_incr), self.failure_rate)
        text = "此训练附带支援卡列表：["
        for c in self.support_card_info_list:
            if c.favor != SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                text += "[支援卡名称：" + str(c.name) + "支援卡类型：" + str(
                    c.card_type) + ", 支援卡羁绊阶段：" + str(c.favor) + "] "
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

    # 转换为元组
    def to_tuple(self):
        return self.speed, self.stamina, self.power, self.will, self.intelligence, self.skill_point


# 技能提示
class SkillHint:
    group_id: int
    rarity: int
    level: int

    def __init__(self, group_id=0, rarity=0, level=0, name=""):
        self.group_id = group_id
        self.rarity = rarity
        self.level = level
        self.name = name

    def __str__(self):
        return f"{{{self.name}}}{self.level}级"


# 技能信息
class LearntSkill:
    skill_id: int
    level: int
    # 是否为赛马娘固有技能
    is_inherent: bool
    name: str

    def __init__(self, skill_id=0, level=1, is_inherent=False, name=""):
        self.skill_id = skill_id
        self.level = level
        self.is_inherent = is_inherent
        self.name = name

    def __str__(self):
        name = self.name or "技能"
        return f"{name}@{self.skill_id} " + (f"等级{self.level:d}" if self.is_inherent else "")


# URA剧本信息
class UraInfo:

    # 剧本链接卡信息
    class LinkCardInfo:
        first_click: bool
        outgoing_unlocked: bool
        outgoing_refused: bool
        outgoing_used: int

        def __init__(self):
            self.first_click = False
            self.outgoing_unlocked = False
            self.outgoing_refused = False
            self.outgoing_used = 0
    ura_tsyInfo: LinkCardInfo
    ura_lmInfo: LinkCardInfo

    def __init__(self):
        self.ura_tsyInfo = UraInfo.LinkCardInfo()
        self.ura_lmInfo = UraInfo.LinkCardInfo()



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
        log.info("本回合执行操作：%s", self.turn_operation_type)
        log.info("本回合备选操作：%s", self.turn_operation_type_replace)
        if self.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_TRAINING:
            log.info("训练类型：%s", self.training_type)


# 操作信息
class TurnInfo:
    # 回合时间
    date: int

    # 分析训练信息是否结束
    parse_train_info_finish: bool
    # 训练结果信息列表
    training_info_list: list[TrainingInfo]
    # 分析育成主菜单是否结束
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

    # 赛马娘状态列表
    uma_condition_list: list[Condition]
    # 赛马娘技能提示
    skill_hint_list: list[SkillHint]
    # 已获得技能启示列表
    learnt_skill_list: list[LearntSkill]
    # 无法学习技能列表
    disable_skill_id_array: list[int]
    # 赛马娘属性训练限制列表
    uma_attribute_limit_list: list[int]
    # 最大体力
    max_vital: int
    # 训练等级次数列表
    train_level_count_list: list[int]
    # URA剧本信息
    ura_info: UraInfo
    # 外出目的地？ TODO 未知
    out_destination: int | None
    # 支援卡列表
    person_list: list[SupportCardInfo]
    # 未知
    proper_info: list[list[int]]
    # 未知
    racing: bool
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
        self.uma_condition_list = []
        self.skill_hint_list = []
        self.learnt_skill_list = []
        self.disable_skill_id_array = []
        self.uma_attribute_limit_list = [0, 0, 0, 0, 0]
        self.max_vital = 100
        self.train_level_count_list = [0, 0, 0, 0, 0]
        self.ura_info = UraInfo()
        self.out_destination = None
        self.person_list = []
        self.proper_info = [[0, 0], [0, 0, 0, 0,], [0, 0, 0, 0]]
        self.racing = False

    # 判断是否夏季合宿
    def is_summer_camp(self):
        return 36 < self.date <= 40 or 60 < self.date <= 64


def log_turn_info(self, full=True, show_skill_and_hint=False):
        log.info("当前回合时间 >" + str(self.date))
        log.info("干劲状态 " + str(self.motivation_level))
        log.info("体力剩余" + str(self.remain_stamina))
        log.info("当前属性值 速度：%s, 耐力：%s, 力量：%s, 毅力：%s, 智力：%s, 技能点：%s", self.uma_attribute.speed,
                 self.uma_attribute.stamina, self.uma_attribute.power, self.uma_attribute.will,
                 self.uma_attribute.intelligence, self.uma_attribute.skill_point)
        if full:
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
            if self.uma_condition_list:
                log.debug("当前状态：" + '，'.join(map(str, self.uma_condition_list)))
        if full or show_skill_and_hint:
            if len(self.learnt_skill_list) > 1:
                log.debug("已获得技能启示：" + '，'.join(map(str, self.learnt_skill_list)))
            if self.skill_hint_list:
                log.debug("已获得技能启示：" + '，'.join(map(str, self.skill_hint_list)))


# 培育上下文
class CultivateContextDetail:
    turn_info: TurnInfo | None
    turn_info_history: list[TurnInfo]
    # 预期养成属性
    expect_attribute: list[int] | None
    follow_support_card_name: str
    follow_support_card_level: int
    # 额外赛事列表
    extra_race_list: list[int]
    # 学习技能列表
    learn_skill_list: list[list[str]]
    learn_skill_blacklist: list[str]
    learn_skill_done: bool
    # 是否学习所选技能
    learn_skill_selected: bool
    # 是否比赛前学习技能
    learn_skill_before_race_done: bool
    # 结束养成
    cultivate_finish: bool
    # 跑法列表
    tactic_list: list[int]
    debut_race_win: bool
    clock_use_limit: int
    clock_used: int
    # 每日使用时钟限制
    clock_use_day_limit: int
    # 技能学习阈值，当超过阈值学习技能
    learn_skill_threshold: int
    # 养成中仅允许学习用户提供的技能
    learn_skill_only_user_provided: bool
    learn_skill_before_race: bool
    # 是否允许恢复体力，TP不足时自动恢复（使用药水）
    allow_recover_tp_drink: bool
    # 是否允许恢复体力，TP不足时自动恢复（使用钻石）
    allow_recover_tp_diamond: bool
    parse_factor_done: bool
    extra_weight: list
    # 抓娃娃
    catch_doll: int
    #
    sasami: bool
    # 赛马娘id
    uma_id: int
    # 赛马娘等级
    talent_level: int
    # 支援卡id列表
    card_id_list: list[int]
    # 赛马娘稀有度
    uma_rarity: int
    # 是否使用TP
    no_tp: bool
    # 是否借用
    borrowed: bool

    def __init__(self):
        self.expect_attribute = None
        self.turn_info = TurnInfo()
        self.turn_info_history = []
        self.extra_race_list = []
        self.learn_skill_list = []
        self.learn_skill_blacklist = []
        self.learn_skill_done = False
        self.learn_skill_selected = False
        self.learn_skill_before_race_done = False
        self.cultivate_finish = False
        self.tactic_list = []
        self.debut_race_win = False
        self.clock_use_limit = 0
        self.clock_used = 0
        self.clock_use_day_limit = 0
        self.allow_recover_tp_drink = False
        self.allow_recover_tp_diamond = False
        self.parse_factor_done = False
        self.extra_weight = []
        self.catch_doll = 0
        self.sasami = False
        self.uma_id = 0
        self.talent_level = 0
        self.card_id_list = []
        self.uma_rarity = 0
        self.no_tp = False
        self.borrowed = False

    def reset_skill_learn(self):
        self.learn_skill_done = False
        self.learn_skill_selected = False

#
class TimeSaleContextDetail:
    buy: list[int]
    bought: list[int]
    buying: int | None
    refresh: FunctionType

    def __init__(self):
        self.buy = []
        self.bought = []
        self.buying = None


class TimeSaleTaskContextDetail:
    time_sale: list[int]
    time_sale_detail: TimeSaleContextDetail

    def __init__(self):
        self.time_sale = []
        self.time_sale_detail = TimeSaleContextDetail()

    def refresh_time_sale(self):
        self.time_sale_detail.buy[:] = self.time_sale
        self.time_sale_detail.bought.clear()
        self.time_sale_detail.buying = None


class TeamStadiumContextDetail(TimeSaleTaskContextDetail):
    opponent_index: int | None
    opponent_stamina: int | None
    raced: bool
    off: bool

    def __init__(self):
        super().__init__()
        self.raced = False
        self.off = False


class DonateContextDetail:
    ask_shoe_type: int
    donated: bool
    asked: bool
    swiped: int

    def __init__(self):
        super().__init__()
        self.donated = False
        self.asked = False
        self.swiped = 0


class DailyRaceContextDetail(TimeSaleTaskContextDetail):
    race: int | None
    difficulty: int | None
    raced: bool

    def __init__(self):
        super().__init__()
        self.raced = False



class UmamusumeContext(BotContext):
    task: UmamusumeTask
    cultivate_detail: CultivateContextDetail
    team_stadium_detail: TeamStadiumContextDetail
    donate_detail: DonateContextDetail
    daily_race_detail: DailyRaceContextDetail
    time_sale_detail: TimeSaleContextDetail

    def __init__(self, task, ctrl):
        super().__init__(task, ctrl)

    def is_task_finish(self) -> bool:
        return False


# 赛马娘任务详情添加到赛马娘上下文中
def build_context(task: UmamusumeTask, ctrl) -> UmamusumeContext:
    ctx = UmamusumeContext(task, ctrl)
    match task.task_type:
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_CULTIVATE:
            detail = CultivateContextDetail()
            detail.expect_attribute = task.detail.expect_attribute
            detail.follow_support_card_name = task.detail.follow_support_card_name
            detail.follow_support_card_level = task.detail.follow_support_card_level
            detail.extra_race_list = task.detail.extra_race_list
            detail.learn_skill_list = task.detail.learn_skill_list
            detail.learn_skill_blacklist = task.detail.learn_skill_blacklist
            detail.tactic_list = task.detail.tactic_list
            detail.clock_use_limit = task.detail.clock_use_limit
            detail.clock_use_day_limit = task.detail.clock_use_day_limit
            detail.learn_skill_threshold = task.detail.learn_skill_threshold
            detail.learn_skill_only_user_provided = task.detail.learn_skill_only_user_provided
            detail.learn_skill_before_race = task.detail.learn_skill_before_race
            detail.allow_recover_tp_drink = task.detail.allow_recover_tp_drink
            detail.allow_recover_tp_diamond = task.detail.allow_recover_tp_diamond
            detail.extra_weight = task.detail.extra_weight
            ctx.cultivate_detail = detail
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_TEAM_STADIUM:
            detail = TeamStadiumContextDetail()
            detail.opponent_index = task.detail.opponent_index
            detail.opponent_stamina = task.detail.opponent_stamina
            detail.time_sale[:] = task.detail.time_sale
            detail.refresh_time_sale()
            ctx.team_stadium_detail = detail
            ctx.time_sale_detail = detail.time_sale_detail
            ctx.time_sale_detail.refresh = detail.refresh_time_sale
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DONATE:
            detail = DonateContextDetail()
            detail.ask_shoe_type = task.detail.ask_shoe_type
            ctx.donate_detail = detail
        case UmamusumeTaskType.UMAMUSUME_TASK_TYPE_DAILY_RACE:
            detail = DailyRaceContextDetail()
            detail.race = task.detail.daily_race_type
            detail.difficulty = task.detail.daily_race_difficulty
            detail.time_sale[:] = task.detail.time_sale
            detail.refresh_time_sale()
            ctx.daily_race_detail = detail
            ctx.time_sale_detail = detail.time_sale_detail
            ctx.time_sale_detail.refresh = detail.refresh_time_sale
    return ctx
