from bot.base.resource import UI
import module.umamusume.asset.template as template

PRESS_START = UI("PRESS_START", [template.UI_PRESS_START], [])
MAIN_MENU = UI("MAIN_MENU", [template.UI_MAIN_MENU], [])
MAIN_MENU_CONTINUE = UI("MAIN_MENU_CONTINUE", [template.UI_MAIN_MENU_CONTINUE], [])
CULTIVATE_SCENARIO_SELECT = UI("CULTIVATE_SCENARIO_SELECT", [template.UI_CULTIVATE_SCENARIO_SELECT], [])
CULTIVATE_FOLLOW_SUPPORT_CARD_SELECT = UI("CULTIVATE_FOLLOW_SUPPORT_CARD_SELECT",
                                          [template.UI_CULTIVATE_FOLLOW_SUPPORT_CARD_SELECT], [])
CULTIVATE_UMAMUSUME_SELECT = UI("CULTIVATE_UMAMUSUME_SELECT",
                                [template.UI_CULTIVATE_UMAMUSUME_SELECT], [])
CULTIVATE_EXTEND_UMAMUSUME_SELECT = UI("CULTIVATE_EXTEND_UMAMUSUME_SELECT",
                                       [template.UI_CULTIVATE_EXTEND_UMAMUSUME_SELECT], [])
CULTIVATE_SUPPORT_CARD_SELECT = UI("CULTIVATE_SUPPORT_CARD_SELECT",
                                   [template.UI_CULTIVATE_SUPPORT_CARD_SELECT], [])

CULTIVATE_MAIN_MENU = UI("CULTIVATE_MAIN_MENU", [template.UI_CULTIVATE_MAIN_MENU], [])
CULTIVATE_TRAINING_SELECT = UI("CULTIVATE_TRAINING_SELECT", [template.UI_CULTIVATE_TRAINING_SELECT, template.UI_CULTIVATE_TRAINING_SELECT_1], [])
CULTIVATE_FINAL_CHECK = UI("CULTIVATE_FINAL_CHECK", [template.UI_CULTIVATE_FINAL_CHECK], [])
INFO = UI("INFO", [template.UI_INFO], [])
CULTIVATE_GOAL_RACE = UI("CULTIVATE_GOAL_RACE", [template.UI_CULTIVATE_GOAL_RACE_1, template.UI_CULTIVATE_GOAL_RACE_2], [])
CULTIVATE_URA_RACE_1 = UI("CULTIVATE_URA_RACE_1", [template.UI_CULTIVATE_GOAL_RACE_1, template.UI_CULTIVATE_URA_RACE_1],[])
CULTIVATE_URA_RACE_2 = UI("CULTIVATE_URA_RACE_1", [template.UI_CULTIVATE_GOAL_RACE_1, template.UI_CULTIVATE_URA_RACE_2],[])
CULTIVATE_URA_RACE_3 = UI("CULTIVATE_URA_RACE_1", [template.UI_CULTIVATE_GOAL_RACE_1, template.UI_CULTIVATE_URA_RACE_3],[])


CULTIVATE_RACE_LIST = UI("CULTIVATE_RACE_LIST", [template.UI_CULTIVATE_RACE_LIST_1, template.UI_CULTIVATE_RACE_LIST_2], [])

BEFORE_RACE = UI("BEFORE_RACE", [template.UI_BEFORE_RACE_1, template.UI_BEFORE_RACE_2], [])
IN_RACE_UMA_LIST = UI("IN_RACE_UMA_LIST", [template.UI_IN_RACE_UMA_LIST_1, template.UI_IN_RACE_UMA_LIST_2], [])
IN_RACE = UI("IN_RACE", [template.UI_IN_RACE_1, template.UI_IN_RACE_2],[])
RACE_RESULT = UI("RACE_RESULT", [template.UI_RACE_RESULT_1, template.UI_RACE_RESULT_2],[])
RACE_REWARD = UI("RACE_REWARD", [template.UI_RACE_REWARD_1, template.UI_RACE_REWARD_2],[])
GOAL_ACHIEVED = UI("GOAL_ACHIEVED", [template.UI_GOAL_ACHIEVED], [])
GOAL_FAILED = UI("GOAL_ACHIEVED", [template.UI_GOAL_FAILED], [])
NEXT_GOAL = UI("NEXT_GOAL", [template.UI_NEXT_GOAL], [])
ALL_GOAL_ACHIEVED = UI("ALL_GOAL_ACHIEVED", [template.UI_ALL_GOAL_ACHIEVED], [])
CULTIVATE_RESULT = UI("CULTIVATE_RESULT", [template.UI_CULTIVATE_RESULT], [])
CULTIVATE_RESULT_1 = UI("CULTIVATE_RESULT", [template.UI_CULTIVATE_RESULT_1], [])
CULTIVATE_RESULT_2 = UI("CULTIVATE_RESULT", [template.UI_CULTIVATE_RESULT_2], [])
CULTIVATE_CATCH_DOLL_GAME = UI("CULTIVATE_CATCH_DOLL_GAME", [template.UI_CULTIVATE_CATCH_DOLL_GAME_1,
                                                             template.UI_CULTIVATE_CATCH_DOLL_GAME_2,
                                                             template.UI_CULTIVATE_CATCH_DOLL_GAME_3],[])
CULTIVATE_CATCH_DOLL_GAME_RESULT = UI("CULTIVATE_CATCH_DOLL_GAME", [template.UI_CULTIVATE_CATCH_DOLL_GAME_RESULT_1, template.UI_CULTIVATE_CATCH_DOLL_GAME_RESULT_2], [])
CULTIVATE_FINISH = UI("CULTIVATE_FINISH", [template.UI_CULTIVATE_FINISH], [])

CULTIVATE_EXTEND = UI("CULTIVATE_EXTEND", [template.UI_CULTIVATE_EXTEND], [])

CULTIVATE_EVENT_UMAMUSUME = UI("CULTIVATE_EVENT_UMAMUSUME", [template.UI_CULTIVATE_EVENT_UMAMUSUME], [])
CULTIVATE_EVENT_SUPPORT_CARD = UI("CULTIVATE_EVENT_SUPPORT_CARD", [template.UI_CULTIVATE_EVENT_SUPPORT_CARD], [])
CULTIVATE_EVENT_SCENARIO = UI("CULTIVATE_EVENT_SCENARIO", [template.UI_CULTIVATE_EVENT_SCENARIO], [])

CULTIVATE_LEARN_SKILL = UI("CULTIVATE_LEARN_SKILL",
                           [template.UI_CULTIVATE_LEARN_SKILL_1, template.UI_CULTIVATE_LEARN_SKILL_2], [])

RECEIVE_CUP = UI("CULTIVATE_RECEIVE_CUP",[template.UI_RECEIVE_CUP], [])

CULTIVATE_LEVEL_RESULT = UI("CULTIVATE_LEVEL_RESULT", [template.UI_CULTIVATE_LEVEL_RESULT], [])
FACTOR_RECEIVE = UI("FACTOR_RECEIVE", [template.UI_FACTOR_RECEIVE], [])
HISTORICAL_RATING_UPDATE = UI("HISTORICAL_RATING_UPDATE", [template.UI_HISTORICAL_RATING_UPDATE], [])
SCENARIO_RATING_UPDATE = UI("HISTORICAL_RATING_UPDATE", [template.UI_SCENARIO_RATING_UPDATE], [])
ACTIVITY_RESULT = UI("ACTIVITY_RESULT", [template.UI_ACTIVITY_RESULT], [])
ACTIVITY_REWARD = UI("ACTIVITY_REWARD", [template.UI_ACTIVITY_REWARD], [])

RACE_HOME = UI("RACE_HOME", [template.UI_TEAM_STADIUM_RACE_1, template.UI_TEAM_STADIUM_RACE_1], [])
TEAM_STADIUM_HOME = UI("TEAM_STADIUM_HOME", [template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_MAIN_1, template.UI_TEAM_STADIUM_MAIN_2], [])
TEAM_STADIUM_HOME_NA = UI("TEAM_STADIUM_HOME_NA", [template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_MAIN_2], [template.UI_TEAM_STADIUM_MAIN_1])
TEAM_STADIUM_SELECT_OPPONENT = UI("TEAM_STADIUM_SELECT_OPPONENT", [template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_SELECT_OPPONENT], [])
TEAM_STADIUM_BEFORE_RACE = UI("TEAM_STADIUM_BEFORE_RACE", [template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_BEFORE_RACE], [])
TEAM_STADIUM_CHECK_ALL_RESULTS = UI("TEAM_STADIUM_CHECK_ALL_RESULTS",[template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_CHECK_ALL_RESULTS], [])
TEAM_STADIUM_CHECK_RESULT = UI("TEAM_STADIUM_CHECK_RESULT",[template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_CHECK_RESULT], [])
TEAM_STADIUM_RESULTS = UI("TEAM_STADIUM_RESULTS",[template.UI_TEAM_STADIUM_RESULTS], [])
TEAM_STADIUM_REWARD = UI("TEAM_STADIUM_REWARD",[template.UI_TEAM_STADIUM_REWARD], [])
TEAM_STADIUM_BEFORE_REWARD = UI("TEAM_STADIUM_BEFORE_REWARD", [template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_END], [template.UI_TEAM_STADIUM_ALL_RESULTS])
TEAM_STADIUM_END = UI("TEAM_STADIUM_END", [template.UI_TEAM_STADIUM_TITLE, template.UI_TEAM_STADIUM_END, template.UI_TEAM_STADIUM_ALL_RESULTS], [])
TEAM_STADIUM_HIGH_SCORE = UI("TEAM_STADIUM_HIGH_SCORE", [template.UI_TEAM_STADIUM_HIGH_SCORE], [])
TEAM_STADIUM_LEVEL_RESULT = UI("TEAM_STADIUM_LEVEL_RESULT", [template.UI_TEAM_STADIUM_LEVEL, template.UI_TEAM_STADIUM_CONTINUE], [])

TIME_SALE_MAIN = UI("TIME_SALE_MAIN", [template.UI_TIME_SALE_1, template.UI_TIME_SALE_2], [])
SHOP_MAIN = UI("SHOP_MAIN", [template.UI_TIME_SALE_1, template.UI_TIME_SALE_3], [])

GUILD_MAIN = UI("GUILD_MAIN", [template.UI_GUILD_MAIN], [])
GUILD_MAIN_2 = UI("GUILD_MAIN_2", [template.UI_GUILD_MAIN_2], [])

DAILY_RACE_HOME = UI("DAILY_RACE_HOME", [template.UI_DAILY_RACE_TITLE], [])
DAILY_RACE_SELECT_RACER = UI("DAILY_RACE_SELECT_RACER", [template.UI_DAILY_RACE_SELECT_RACER], [])

scan_ui_list = [PRESS_START, MAIN_MENU, MAIN_MENU_CONTINUE,
                CULTIVATE_SCENARIO_SELECT, CULTIVATE_UMAMUSUME_SELECT, CULTIVATE_EXTEND_UMAMUSUME_SELECT,
                CULTIVATE_SUPPORT_CARD_SELECT, CULTIVATE_FOLLOW_SUPPORT_CARD_SELECT, CULTIVATE_FINAL_CHECK, INFO,
                CULTIVATE_MAIN_MENU, CULTIVATE_TRAINING_SELECT, CULTIVATE_EXTEND, CULTIVATE_CATCH_DOLL_GAME,
                CULTIVATE_CATCH_DOLL_GAME_RESULT, CULTIVATE_LEVEL_RESULT,
                CULTIVATE_GOAL_RACE, CULTIVATE_RACE_LIST, CULTIVATE_RESULT, CULTIVATE_RESULT_1, CULTIVATE_RESULT_2,
                CULTIVATE_LEARN_SKILL, RECEIVE_CUP,
                CULTIVATE_URA_RACE_1, CULTIVATE_URA_RACE_2,CULTIVATE_URA_RACE_3,
                BEFORE_RACE, IN_RACE_UMA_LIST, IN_RACE, RACE_RESULT, RACE_REWARD,
                GOAL_ACHIEVED, NEXT_GOAL, ALL_GOAL_ACHIEVED, CULTIVATE_FINISH, GOAL_FAILED,
                FACTOR_RECEIVE, HISTORICAL_RATING_UPDATE, SCENARIO_RATING_UPDATE,
                CULTIVATE_EVENT_UMAMUSUME, CULTIVATE_EVENT_SUPPORT_CARD, CULTIVATE_EVENT_SCENARIO, ACTIVITY_RESULT,
                ACTIVITY_REWARD, RACE_HOME, TEAM_STADIUM_HOME, TEAM_STADIUM_HOME_NA, TEAM_STADIUM_SELECT_OPPONENT,
                TEAM_STADIUM_BEFORE_RACE, TEAM_STADIUM_CHECK_ALL_RESULTS, TEAM_STADIUM_LEVEL_RESULT,
                TEAM_STADIUM_CHECK_RESULT, TEAM_STADIUM_RESULTS, TEAM_STADIUM_REWARD, TEAM_STADIUM_BEFORE_REWARD,
                TEAM_STADIUM_END, TEAM_STADIUM_HIGH_SCORE, TIME_SALE_MAIN, SHOP_MAIN,
                GUILD_MAIN, GUILD_MAIN_2, DAILY_RACE_HOME, DAILY_RACE_SELECT_RACER,
                ]
