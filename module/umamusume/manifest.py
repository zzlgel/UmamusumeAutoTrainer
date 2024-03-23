from typing import Dict

from bot.base.manifest import AppManifest
from bot.base.resource import NOT_FOUND_UI
from module.umamusume.asset.ui import *
from module.umamusume.context import build_context
from module.umamusume.hook import after_hook, before_hook
from module.umamusume.script.cultivate_task.cultivate import *
from module.umamusume.script.cultivate_task.info import script_info
from module.umamusume.task import UmamusumeTaskType, build_task

# 静态字典，赛马娘育成任务UI-脚本
script_dicts: Dict[UmamusumeTaskType, dict[UI, callable]] = {
    UmamusumeTaskType.UMAMUSUME_TASK_TYPE_CULTIVATE: {
        INFO: script_info,
        MAIN_MENU: script_main_menu,
        CULTIVATE_SCENARIO_SELECT: script_scenario_select,
        CULTIVATE_UMAMUSUME_SELECT: script_umamusume_select,
        CULTIVATE_EXTEND_UMAMUSUME_SELECT: script_extend_umamusume_select,
        CULTIVATE_SUPPORT_CARD_SELECT: script_support_card_select,
        CULTIVATE_FOLLOW_SUPPORT_CARD_SELECT: script_follow_support_card_select,
        CULTIVATE_MAIN_MENU: script_cultivate_main_menu,
        CULTIVATE_TRAINING_SELECT: script_cultivate_training_select,
        CULTIVATE_FINAL_CHECK: script_cultivate_final_check,
        CULTIVATE_EVENT_UMAMUSUME: script_cultivate_event,
        CULTIVATE_EVENT_SUPPORT_CARD: script_cultivate_event,
        CULTIVATE_EVENT_SCENARIO: script_cultivate_event,
        CULTIVATE_GOAL_RACE: script_cultivate_goal_race,
        CULTIVATE_RACE_LIST: script_cultivate_race_list,
        BEFORE_RACE: script_cultivate_before_race,
        IN_RACE_UMA_LIST: script_cultivate_in_race_uma_list,
        IN_RACE: script_in_race,
        RACE_RESULT: script_cultivate_race_result,
        RACE_REWARD: script_cultivate_race_reward,
        GOAL_ACHIEVED: script_cultivate_goal_achieved,
        ALL_GOAL_ACHIEVED: script_cultivate_goal_achieved,
        NEXT_GOAL: script_cultivate_next_goal,
        CULTIVATE_EXTEND: script_cultivate_extend,
        CULTIVATE_RESULT: script_cultivate_result,
        CULTIVATE_RESULT_1: script_cultivate_result,
        CULTIVATE_RESULT_2: script_cultivate_result,
        CULTIVATE_CATCH_DOLL_GAME: script_cultivate_catch_doll,
        CULTIVATE_CATCH_DOLL_GAME_RESULT: script_cultivate_catch_doll_result,
        CULTIVATE_LEARN_SKILL: script_cultivate_learn_skill,
        CULTIVATE_FINISH: script_cultivate_finish,
        NOT_FOUND_UI: script_not_found_ui,
        RECEIVE_CUP: script_receive_cup,
        GOAL_FAILED: script_cultivate_goal_failed,
        CULTIVATE_LEVEL_RESULT: script_cultivate_level_result,
        FACTOR_RECEIVE:script_factor_receive,
        HISTORICAL_RATING_UPDATE: script_historical_rating_update,
        SCENARIO_RATING_UPDATE: script_scenario_rating_update,
        CULTIVATE_URA_RACE_1: script_cultivate_goal_race,
        CULTIVATE_URA_RACE_2: script_cultivate_goal_race,
        CULTIVATE_URA_RACE_3: script_cultivate_goal_race,
        ACTIVITY_RESULT: script_cultivate_result,
        ACTIVITY_REWARD: script_cultivate_result
    }
}

default_script_dict: Dict[UI, callable] = {

}


def exec_script(ctx: UmamusumeContext):
    script_dicts_by_type = script_dicts[ctx.task.task_type]
    if script_dicts_by_type is not None:
        if ctx.current_ui in script_dicts_by_type:
            script_dicts_by_type[ctx.current_ui](ctx)
            return
    if ctx.current_ui in default_script_dict:
        default_script_dict[ctx.current_ui](ctx)
    else:
        print("未找到此界面对应的默认脚本")


UmamusumeManifest = AppManifest(
    app_name="umamusume",
    app_package_name="com.bilibili.umamusu",
    app_activity_name="com.uo.sdk.SplashActivity",
    build_context=build_context,
    build_task=build_task,
    ui_list=scan_ui_list,
    script=exec_script,
    before_hook=before_hook,
    after_hook=after_hook
)


