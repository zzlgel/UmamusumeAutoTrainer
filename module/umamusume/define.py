from enum import Enum


# 赛马娘育成剧本
class ScenarioType(Enum):
    SCENARIO_TYPE_UNKNOWN = 0
    SCENARIO_TYPE_URA = 1

# 支援卡类型
class SupportCardType(Enum):
    SUPPORT_CARD_TYPE_UNKNOWN = 0
    SUPPORT_CARD_TYPE_SPEED = 1
    # 耐力
    SUPPORT_CARD_TYPE_STAMINA = 2
    SUPPORT_CARD_TYPE_POWER = 3
    # 毅力
    SUPPORT_CARD_TYPE_WILL = 4
    SUPPORT_CARD_TYPE_INTELLIGENCE = 5
    SUPPORT_CARD_TYPE_FRIEND = 6
    # 群?
    SUPPORT_CARD_TYPE_GROUP = 7
    # npc?
    SUPPORT_CARD_TYPE_NPC = 10


# 支援卡羁绊阶段
class SupportCardFavorLevel(Enum):
    SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN = 0
    SUPPORT_CARD_FAVOR_LEVEL_1 = 1
    SUPPORT_CARD_FAVOR_LEVEL_2 = 2
    SUPPORT_CARD_FAVOR_LEVEL_3 = 3
    SUPPORT_CARD_FAVOR_LEVEL_4 = 4


# 训练项目
class TrainingType(Enum):
    TRAINING_TYPE_UNKNOWN = 0
    TRAINING_TYPE_SPEED = 1
    TRAINING_TYPE_STAMINA = 2
    TRAINING_TYPE_POWER = 3
    TRAINING_TYPE_WILL = 4
    TRAINING_TYPE_INTELLIGENCE = 5


# 干劲状态，从低到高
class MotivationLevel(Enum):
    MOTIVATION_LEVEL_UNKNOWN = 0
    # 极差
    MOTIVATION_LEVEL_1 = 1
    # 不佳
    MOTIVATION_LEVEL_2 = 2
    # 普通
    MOTIVATION_LEVEL_3 = 3
    # 上佳
    MOTIVATION_LEVEL_4 = 4
    # 极佳
    MOTIVATION_LEVEL_5 = 5


# 操作类型
class TurnOperationType(Enum):
    TURN_OPERATION_TYPE_UNKNOWN = 0
    # 训练
    TURN_OPERATION_TYPE_TRAINING = 1
    # 休息
    TURN_OPERATION_TYPE_REST = 2
    # 医务室
    TURN_OPERATION_TYPE_MEDIC = 3
    # 外出
    TURN_OPERATION_TYPE_TRIP = 4
    # 比赛
    TURN_OPERATION_TYPE_RACE = 5


# Uma剧本支援NPC
class SupportCardUma(Enum):
    SUPPORT_CARD_UMA_UNKNOWN = 0
    # 理事长
    SUPPORT_CARD_UMA_AKIKAWA = 1
    # 记者
    SUPPORT_CARD_UMA_REPORTER = 2


# 比赛战术
class RaceTacticType(Enum):
    RACE_TACTIC_TYPE_UNKNOWN = 0
    # 后追
    RACE_TACTIC_TYPE_BACK = 1
    # 居中
    RACE_TACTIC_TYPE_MIDDLE = 2
    # 跟前
    RACE_TACTIC_TYPE_FRONT = 3
    # 领跑
    RACE_TACTIC_TYPE_ESCAPE = 4
