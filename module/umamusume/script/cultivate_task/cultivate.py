import time

from bot.base.task import TaskStatus, EndTaskReason
from module.umamusume.asset.point import *
from module.umamusume.context import TurnInfo
from module.umamusume.script.cultivate_task.const import SKILL_LEARN_PRIORITY_LIST
from module.umamusume.task import EndTaskReason as UEndTaskReason
from module.umamusume.script.cultivate_task.parse import *
from module.umamusume.script.cultivate_task.event import Event
try:
    from module.umamusume.script.ura.cultivate import ura_parse_cultivate_main_menu, ura_get_event_choice_by_effect
    from module.umamusume.script.ura.skill_ai import ura_script_cultivate_learn_skill
except ImportError:
    def ura_get_event_choice_by_effect(ctx: UmamusumeContext):
        return
    ura_parse_cultivate_main_menu = parse_cultivate_main_menu

    def ura_script_cultivate_learn_skill(ctx: UmamusumeContext,
                                     learn_skill_list: list[list[str]],
                                     learn_skill_blacklist: list[str]):
        raise ImportError
    print("未找到URA相关组件")

log = logger.get_logger(__name__)


# 培养主界面，与游戏主界面区分
def script_cultivate_main_menu(ctx: UmamusumeContext):
    img = ctx.current_screen
    current_date = parse_date(img, ctx)
    if current_date == -1:
        log.warning("解析日期失败")
        return
    # 如果进入新的一回合，记录旧的回合信息并创建新的
    if ctx.cultivate_detail.turn_info is None or current_date != ctx.cultivate_detail.turn_info.date:
        if ctx.cultivate_detail.turn_info is not None:
            ctx.cultivate_detail.turn_info_history.append(ctx.cultivate_detail.turn_info)
        ctx.cultivate_detail.turn_info = TurnInfo()
        ctx.cultivate_detail.turn_info.date = current_date
        log.debug("进入新回合，日期：" + str(current_date))
        ctx.cultivate_detail.reset_skill_learn()

    # 解析主界面
    if not ctx.cultivate_detail.turn_info.parse_main_menu_finish:
        ura_parse_cultivate_main_menu(ctx, img)
    if not ctx.cultivate_detail.turn_info.parse_main_menu_finish:
        parse_cultivate_main_menu(ctx, img)

    # 通过比赛id前两位判断是否有额外赛事
    has_extra_race = len([i for i in ctx.cultivate_detail.extra_race_list
                          if str(i)[:2] == str(ctx.cultivate_detail.turn_info.date)]) != 0

    # 意外情况处理，当前回合没有学习技能，但是技能学习已经完成
    if not ctx.cultivate_detail.turn_info.turn_learn_skill_done and ctx.cultivate_detail.learn_skill_done:
        ctx.cultivate_detail.reset_skill_learn()

    # 当前技能pt点数超过阈值且未学习技能
    if (ctx.cultivate_detail.turn_info.uma_attribute.skill_point > ctx.cultivate_detail.learn_skill_threshold
            and not ctx.cultivate_detail.turn_info.turn_learn_skill_done):
        if len(ctx.cultivate_detail.learn_skill_list) > 0 or not ctx.cultivate_detail.learn_skill_only_user_provided:
            ctx.ctrl.click_by_point(CULTIVATE_SKILL_LEARN)
        elif has_extra_race and ctx.cultivate_detail.learn_skill_before_race \
             and not ctx.cultivate_detail.learn_skill_before_race_done:
            ctx.cultivate_detail.turn_info.racing = True
            ctx.ctrl.click_by_point(CULTIVATE_SKILL_LEARN)
        else:
            ctx.cultivate_detail.learn_skill_done = True
            ctx.cultivate_detail.turn_info.turn_learn_skill_done = True
        ctx.cultivate_detail.turn_info.parse_main_menu_finish = False
        return
    else:
        ctx.cultivate_detail.reset_skill_learn()

    # 判断是否需要进入训练界面。TODO 失败率无法准确判断，使用体力代替比较失控
    if not ctx.cultivate_detail.turn_info.parse_train_info_finish:
        if has_extra_race or ctx.cultivate_detail.turn_info.remain_stamina < 48:
            ctx.cultivate_detail.turn_info.parse_train_info_finish = True
            return
        else:
            ctx.ctrl.click_by_point(TO_TRAINING_SELECT)
            return

    turn_operation = ctx.cultivate_detail.turn_info.turn_operation
    if turn_operation is not None:
        if turn_operation.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_TRAINING:
            ctx.ctrl.click_by_point(TO_TRAINING_SELECT)
        elif turn_operation.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_REST:
            ctx.ctrl.click_by_point(CULTIVATE_REST)
        elif turn_operation.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_MEDIC:
            if ctx.cultivate_detail.turn_info.is_summer_camp():
                ctx.ctrl.click_by_point(CULTIVATE_MEDIC_SUMMER)
            else:
                ctx.ctrl.click_by_point(CULTIVATE_MEDIC)
        elif turn_operation.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_TRIP:
            ctx.ctrl.click_by_point(CULTIVATE_TRIP)
        elif turn_operation.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_RACE:
            if ctx.cultivate_detail.turn_info.is_summer_camp():
                ctx.ctrl.click_by_point(CULTIVATE_RACE_SUMMER)
            else:
                ctx.ctrl.click_by_point(CULTIVATE_RACE)


# 选择训练项目或执行或解析训练
def script_cultivate_training_select(ctx: UmamusumeContext):
    if ctx.cultivate_detail.turn_info is None:
        log.warning("回合信息未初始化")
        ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)
        return
    # 如果训练主界面没有解析完成，返回
    if not ctx.cultivate_detail.turn_info.parse_main_menu_finish:
        ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)
        return

    # 根据上下文直接执行对应训练项目
    if ctx.cultivate_detail.turn_info.turn_operation is not None:
        if (ctx.cultivate_detail.turn_info.turn_operation.turn_operation_type ==
                TurnOperationType.TURN_OPERATION_TYPE_TRAINING):
            ctx.ctrl.click_by_point(
                TRAINING_POINT_LIST[ctx.cultivate_detail.turn_info.turn_operation.training_type.value - 1])
            time.sleep(0.5)
            ctx.ctrl.click_by_point(
                TRAINING_POINT_LIST[ctx.cultivate_detail.turn_info.turn_operation.training_type.value - 1])
            # 有时训练完一回合，并没有任何事件触发，会耽误玩家时间，改为1秒后返回，执行其他逻辑
            time.sleep(1)
            return
        else:
            ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)
            return

    # 解析训练项目
    if not ctx.cultivate_detail.turn_info.parse_train_info_finish:
        img = ctx.current_screen
        train_type = parse_train_type(ctx, img)
        if train_type == TrainingType.TRAINING_TYPE_UNKNOWN:
            return
        parse_training_result(ctx, img, train_type)
        parse_training_support_card(ctx, img, train_type)
        viewed = train_type.value
        for i in range(5):
            if i != (viewed - 1):
                retry = 0
                max_retry = 3
                ctx.ctrl.click_by_point(TRAINING_POINT_LIST[i])
                img = ctx.ctrl.get_screen()
                # 防止网络延迟等外部问题导致解析失败，做重试
                while parse_train_type(ctx, img) != TrainingType(i + 1) and retry < max_retry:
                    if retry > 2:
                        ctx.ctrl.click_by_point(TRAINING_POINT_LIST[i])
                    time.sleep(0.2)
                    img = ctx.ctrl.get_screen()
                    retry += 1
                if retry == max_retry:
                    return
                parse_training_result(ctx, img, TrainingType(i + 1))
                parse_training_support_card(ctx, img, TrainingType(i + 1))
        ctx.cultivate_detail.turn_info.parse_train_info_finish = True
        return


# 训练结果确认
def script_main_menu(ctx: UmamusumeContext):
    if ctx.cultivate_detail.cultivate_finish:
        ctx.task.end_task(TaskStatus.TASK_STATUS_SUCCESS, EndTaskReason.COMPLETE)
        return
    if ctx.cultivate_detail.no_tp or (time.time() - ctx.task.detail.
            timestamp['no_tp'].get(ctx.task.device_name or "default", 0) < 300):
        ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.TP_NOT_ENOUGH)
        return
    if ts := ctx.task.detail.timestamp['borrowed'].get(ctx.task.device_name or "default", 0):
        import croniter
        import datetime
        if time.time() < croniter.croniter("0 5 * * *", ts).get_next(datetime.datetime).timestamp():
            ctx.task.end_task(TaskStatus.TASK_STATUS_FAILED, UEndTaskReason.BORROWED)
            return
    ctx.ctrl.click_by_point(TO_CULTIVATE_SCENARIO_CHOOSE)


# 剧本选择，育成准备-前往下一步
def script_scenario_select(ctx: UmamusumeContext):
    if ctx.cultivate_detail.no_tp or ctx.cultivate_detail.borrowed:
        ctx.ctrl.click(360, 1220, "返回主界面")
        return
    ctx.ctrl.click_by_point(TO_CULTIVATE_PREPARE_NEXT)


# 赛马娘选择，育成准备-前往下一步
def script_umamusume_select(ctx: UmamusumeContext):
    if ctx.cultivate_detail.no_tp or ctx.cultivate_detail.borrowed:
        ctx.ctrl.click(360, 1220, "返回主界面")
        return
    ctx.ctrl.click_by_point(TO_CULTIVATE_PREPARE_NEXT)


# TODO ？？？
def script_extend_umamusume_select(ctx: UmamusumeContext):
    if ctx.cultivate_detail.no_tp or ctx.cultivate_detail.borrowed:
        ctx.ctrl.click(360, 1220, "返回主界面")
        return
    img = ctx.ctrl.get_screen(to_gray=True)[700:900, 50:550]
    if image_match(img, REF_CULTIVATE_SUPPORT_CARD_EMPTY).find_match:
        ctx.cultivate_detail.borrowed = True
        ctx.task.detail.timestamp['borrowed'][ctx.task.device_name or "default"] = time.time()
        return
    ctx.ctrl.click_by_point(TO_CULTIVATE_PREPARE_NEXT)


# 支援卡选择
def script_support_card_select(ctx: UmamusumeContext):
    if ctx.cultivate_detail.no_tp:
        ctx.ctrl.click(360, 1220, "返回主界面")
        return
    img = ctx.ctrl.get_screen(to_gray=True)
    if image_match(img, REF_CULTIVATE_SUPPORT_CARD_EMPTY).find_match:
        ctx.ctrl.click_by_point(TO_FOLLOW_SUPPORT_CARD_SELECT)
        return
    ctx.ctrl.click_by_point(TO_CULTIVATE_PREPARE_NEXT)


# TODO 被打断之后继续后面逻辑的能力
def script_follow_support_card_select(ctx: UmamusumeContext):
    img = ctx.ctrl.get_screen()
    while True:
        selected = find_support_card(ctx, img)
        if selected:
            break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if compare_color_equal(img[1096, 693], [125, 120, 142]):
            while True:
                img = cv2.cvtColor(ctx.ctrl.get_screen(), cv2.COLOR_BGR2RGB)
                if compare_color_equal(img[127, 697], [211, 209, 219]):
                    ctx.ctrl.swipe(x1=350, y1=400, x2=350, y2=1000, duration=200, name="")
                else:
                    break
            ctx.ctrl.click_by_point(FOLLOW_SUPPORT_CARD_SELECT_REFRESH)
            return
        ctx.ctrl.swipe(x1=350, y1=1000, x2=350, y2=400, duration=1000, name="")
        time.sleep(1)
        img = ctx.ctrl.get_screen()


# 开始育成
def script_cultivate_final_check(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(CULTIVATE_FINAL_CHECK_START)


# 事件选择，TODO 这里处理有些粗糙
def script_cultivate_event(ctx: UmamusumeContext):
    img = ctx.ctrl.get_screen()
    event_name, selector_list = parse_cultivate_event(ctx, img)
    log.debug("当前事件：%s", event_name)
    if len(selector_list) != 0 and len(selector_list) != 1:
        time.sleep(0.5)
        # 避免出现选项残缺的情况，这里重新解析一次
        img = ctx.ctrl.get_screen()
        event_name, selector_list = parse_cultivate_event(ctx, img)
        choice_index = ura_get_event_choice_by_effect(ctx) or Event(event_name)(ctx)
        # 意外情况容错
        if choice_index > len(selector_list):
            choice_index = 1
        ctx.ctrl.click(selector_list[choice_index - 1][0], selector_list[choice_index - 1][1],
                       "事件选项-" + str(choice_index))
    else:
        log.debug("未出现选项")


# TODO 雾水
def script_cultivate_goal_race(ctx: UmamusumeContext):
    img = ctx.current_screen
    current_date = parse_date(img, ctx)
    if current_date == -1:
        log.warning("解析日期失败")
        return
    # 如果进入新的一回合，记录旧的回合信息并创建新的
    if ctx.cultivate_detail.turn_info is None or current_date != ctx.cultivate_detail.turn_info.date:
        if ctx.cultivate_detail.turn_info is not None:
            ctx.cultivate_detail.turn_info_history.append(ctx.cultivate_detail.turn_info)
        ctx.cultivate_detail.turn_info = TurnInfo()
        ctx.cultivate_detail.turn_info.date = current_date
    ctx.cultivate_detail.turn_info.racing = True
    if ctx.cultivate_detail.learn_skill_before_race and not ctx.cultivate_detail.turn_info.turn_learn_skill_done \
            and not ctx.cultivate_detail.learn_skill_before_race_done:
        ctx.ctrl.click(205, 1080, "技能")
        return
    ctx.ctrl.click_by_point(CULTIVATE_GOAL_RACE_INTER_1)
    # 避免赛后直接育成结束不学技能了
    ctx.cultivate_detail.reset_skill_learn()
    ctx.cultivate_detail.turn_info.turn_learn_skill_done = False


# 选择比赛 TODO 这几个数字什么意思
def script_cultivate_race_list(ctx: UmamusumeContext):
    time.sleep(2)
    if ctx.cultivate_detail.turn_info is None:
        log.warning("回合信息未初始化")
        ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)
        return
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if image_match(img, REF_RACE_LIST_GOAL_RACE).find_match:
        ctx.ctrl.click_by_point(CULTIVATE_GOAL_RACE_INTER_2)
    elif image_match(img, REF_RACE_LIST_URA_RACE).find_match:
        ctx.ctrl.click_by_point(CULTIVATE_GOAL_RACE_INTER_2)
    else:
        if ctx.cultivate_detail.turn_info.turn_operation is None:
            ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)
            return
        if ctx.cultivate_detail.turn_info.turn_operation.turn_operation_type == TurnOperationType.TURN_OPERATION_TYPE_RACE:
            swiped = False
            while True:
                img = cv2.cvtColor(ctx.ctrl.get_screen(), cv2.COLOR_BGR2RGB)
                if not compare_color_equal(img[705, 701], [211, 209, 219]):
                    if swiped is True:
                        time.sleep(1.5)
                    break
                ctx.ctrl.swipe(x1=20, y1=850, x2=20, y2=1000, duration=200, name="")
                swiped = True
            img = ctx.ctrl.get_screen()
            while True:
                selected = find_race(ctx, img, ctx.cultivate_detail.turn_info.turn_operation.race_id)
                if selected:
                    time.sleep(1)
                    ctx.ctrl.click_by_point(CULTIVATE_GOAL_RACE_INTER_2)
                    time.sleep(1)
                    return
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if not compare_color_equal(img[1006, 701], [211, 209, 219]):
                    log.warning("未找到目标赛事")
                    # 没有合适的赛事就使用备用的操作
                    if ctx.cultivate_detail.turn_info.turn_operation.race_id == 0:
                        ctx.cultivate_detail.turn_info.turn_operation.turn_operation_type = ctx.cultivate_detail.turn_info.turn_operation.turn_operation_type_replace
                    ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)
                    break
                ctx.ctrl.swipe(x1=20, y1=1000, x2=20, y2=850, duration=1000, name="")
                time.sleep(1)
                img = ctx.ctrl.get_screen()
        else:
            ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_MAIN_MENU)


# 比赛前-更改战术
def script_cultivate_before_race(ctx: UmamusumeContext):
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2RGB)
    p_check_skip = img[1175, 330]

    date = ctx.cultivate_detail.turn_info.date
    if date != -1:
        tactic_check_point_list = [img[668, 480], img[668, 542], img[668, 600], img[668, 670]]
        if date <= 72:
            p_check_tactic = tactic_check_point_list[ctx.cultivate_detail.tactic_list[int((date - 1) / 24)] - 1]
        else:
            p_check_tactic = tactic_check_point_list[ctx.cultivate_detail.tactic_list[2] - 1]
        if compare_color_equal(p_check_tactic, [170, 170, 170]):
            ctx.ctrl.click_by_point(BEFORE_RACE_CHANGE_TACTIC)
            return

    if p_check_skip[0] < 200 and p_check_skip[1] < 200 and p_check_skip[2] < 200:
        ctx.ctrl.click_by_point(BEFORE_RACE_START)
    else:
        ctx.ctrl.click_by_point(BEFORE_RACE_SKIP)


# 比赛马娘列表-确认
def script_cultivate_in_race_uma_list(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(IN_RACE_UMA_LIST_CONFIRM)


# 比赛中-跳过
def script_in_race(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(IN_RACE_SKIP)


# 比赛结果-确认
def script_cultivate_race_result(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(RACE_RESULT_CONFIRM)


# 比赛奖励-确认
def script_cultivate_race_reward(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(RACE_REWARD_CONFIRM)


# 目标达成-确认
def script_cultivate_goal_achieved(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(GOAL_ACHIEVE_CONFIRM)


# 目标未达成-确认
def script_cultivate_goal_failed(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(GOAL_FAIL_CONFIRM)


# 下一个目标-确认
def script_cultivate_next_goal(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(NEXT_GOAL_CONFIRM)


# 因子继承-确认
def script_cultivate_extend(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(CULTIVATE_EXTEND_CONFIRM)


# 育成结果-确认
def script_cultivate_result(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(CULTIVATE_RESULT_CONFIRM)


# 抓娃娃机-开始
# 1.878s 2s 0.649s
def script_cultivate_catch_doll(ctx: UmamusumeContext):
    match ctx.cultivate_detail.catch_doll:
        case 0:
            ctx.ctrl.swipe(x1=365, y1=1117, x2=370, y2=1110, duration=1878, name="抓娃娃第一次")
        case 1:
            ctx.ctrl.swipe(x1=365, y1=1117, x2=370, y2=1110, duration=2000, name="抓娃娃第二次")
        case 2:
            ctx.ctrl.swipe(x1=365, y1=1117, x2=370, y2=1110, duration=649, name="抓娃娃第三次")
        case _:
            ctx.ctrl.click_by_point(CULTIVATE_CATCH_DOLL_START)
    ctx.cultivate_detail.catch_doll += 1



# 抓娃娃机-结果确认
def script_cultivate_catch_doll_result(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(CULTIVATE_CATCH_DOLL_RESULT_CONFIRM)


# 结束养成 TODO 什么时候触发
def script_cultivate_finish(ctx: UmamusumeContext):
    if not ctx.cultivate_detail.learn_skill_done or not ctx.cultivate_detail.cultivate_finish:
        ctx.cultivate_detail.cultivate_finish = True
        ctx.ctrl.click_by_point(CULTIVATE_FINISH_LEARN_SKILL)
    else:
        ctx.ctrl.click_by_point(CULTIVATE_FINISH_CONFIRM)


# 学习技能
def script_cultivate_learn_skill(ctx: UmamusumeContext):
    if ctx.cultivate_detail.learn_skill_done:
        "如果确定按钮点不动（G通道=130），就点返回"
        img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2RGB)[1080, 360][1]
        if ctx.cultivate_detail.learn_skill_selected and img > 160:
            ctx.ctrl.click_by_point(CULTIVATE_LEARN_SKILL_CONFIRM)
        else:
            ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_FINISH)
        return
    learn_skill_list: list[list[str]]
    learn_skill_blacklist: list[str] = ctx.cultivate_detail.learn_skill_blacklist
    if ctx.cultivate_detail.cultivate_finish or not ctx.cultivate_detail.learn_skill_only_user_provided:
        if len(ctx.cultivate_detail.learn_skill_list) == 0:
            learn_skill_list = SKILL_LEARN_PRIORITY_LIST
        else:
            #如果用户自定义了技能优先级，那么不再采用预设的优先级
            learn_skill_list = ctx.cultivate_detail.learn_skill_list
    else:
        if len(ctx.cultivate_detail.learn_skill_list) == 0:
            ctx.ctrl.click_by_point(RETURN_TO_CULTIVATE_FINISH)
            ctx.cultivate_detail.learn_skill_done = True
            ctx.cultivate_detail.turn_info.turn_learn_skill_done = True
            return
        else:
            learn_skill_list = ctx.cultivate_detail.learn_skill_list

    try:
        ura_script_cultivate_learn_skill(ctx, learn_skill_list, learn_skill_blacklist)
    except (ImportError, Exception) as e:
        print("出问题了", e)
    else:
        return

    # 遍历整页, 找出所有可点的技能
    skill_list = []
    while ctx.task.running():
        img = ctx.ctrl.get_screen()
        current_screen_skill_list = get_skill_list(img, learn_skill_list, learn_skill_blacklist)
        # 避免重复统计(会出现在页末翻页不完全的情况)
        for i in current_screen_skill_list:
            if i not in skill_list:
                skill_list.append(i)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if not compare_color_equal(img[1006, 701], [211, 209, 219]):
            break
        ctx.ctrl.swipe(x1=23, y1=1000, x2=23, y2=636, duration=1000, name="")
        time.sleep(1)

    log.debug("当前技能状态：" + str(skill_list))

    # 将金色技能和其后面的技能绑定
    for i in range(len(skill_list)):
        if i != (len(skill_list) - 1) and skill_list[i]["gold"] is True:
            skill_list[i]["subsequent_skill"] = skill_list[i + 1]["skill_name"]

    # 按照优先级排列
    skill_list = sorted(skill_list, key=lambda x: x["priority"])
    # TODO: 暂时没办法处理一个技能可以点多次的情况
    img = ctx.ctrl.get_screen()
    total_skill_point_text = re.sub("\\D", "", ocr_line(img[400: 440, 490: 665]))
    if total_skill_point_text == "":
        total_skill_point = 0
    else:
        total_skill_point = int(total_skill_point_text)
    target_skill_list = []
    target_skill_list_raw = []
    curr_point = 0
    for i in range(len(learn_skill_list) + 1):
        if (i > 0 and ctx.cultivate_detail.learn_skill_only_user_provided is True and
                not ctx.cultivate_detail.cultivate_finish):
            break
        for j in range(len(skill_list)):
            if skill_list[j]["priority"] != i or skill_list[j]["available"] is False:
                continue
            if curr_point + skill_list[j]["skill_cost"] <= total_skill_point:
                curr_point += skill_list[j]["skill_cost"]
                target_skill_list.append(skill_list[j]["skill_name"])
                target_skill_list_raw.append(skill_list[j]["skill_name_raw"])
                # 如果点的是金色技能, 就将其绑定的下位技能设置为不可点
                if skill_list[j]["gold"] is True and skill_list[j]["subsequent_skill"] != '':
                    for k in range(len(skill_list)):
                        if skill_list[k]["skill_name"] == skill_list[j]["subsequent_skill"]:
                            skill_list[k]["available"] = False

    # 向上移动至对齐
    ctx.ctrl.swipe(x1=23, y1=950, x2=23, y2=968, duration=100, name="")
    time.sleep(1)

    # 删除已经学会的技能
    for skill in target_skill_list_raw:
        for prioritylist in ctx.cultivate_detail.learn_skill_list:
            if prioritylist.__contains__(skill):
                prioritylist.remove(skill)
    for skill in skill_list:
        for prioritylist in ctx.cultivate_detail.learn_skill_list:
            if skill['available'] is False and prioritylist.__contains__(skill['skill_name_raw']):
                prioritylist.remove(skill['skill_name_raw'])
    # 如果一个优先级全为空，则直接将其删除
    ctx.cultivate_detail.learn_skill_list = [x for x in ctx.cultivate_detail.learn_skill_list if x != []]

    # 点技能
    while True:
        img = ctx.ctrl.get_screen()
        find_skill(ctx, img, target_skill_list, learn_any_skill=False)
        if len(target_skill_list) == 0:
            # 防止有技能pt浪费的情况， TODO 需要根据马娘跑法来判断是否需要学习哪些技能
            find_skill(ctx, img, target_skill_list, learn_any_skill=True)
            break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if not compare_color_equal(img[488, 701], [211, 209, 219]):
            break
        ctx.ctrl.swipe(x1=23, y1=636, x2=23, y2=1000, duration=1000, name="")
        time.sleep(1)

    log.debug("当前待学习的技能：" + str(ctx.cultivate_detail.learn_skill_list))
    log.debug("当前已学习的技能：" + str([skill['skill_name'] for skill in skill_list if not skill['available']]))

    ctx.cultivate_detail.learn_skill_done = True
    ctx.cultivate_detail.turn_info.turn_learn_skill_done = True


# 为匹配ui，默认点击位置
def script_not_found_ui(ctx: UmamusumeContext):
    ctx.ctrl.click(719, 1, "")


# 获得奖杯-关闭
def script_receive_cup(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(CULTIVATE_RECEIVE_CUP_CLOSE)


# 养成等级-下一页
def script_cultivate_level_result(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(CULTIVATE_LEVEL_RESULT_CONFIRM)


# 因子获取-下一页
def script_factor_receive(ctx: UmamusumeContext):
    if ctx.cultivate_detail.parse_factor_done:
        ctx.ctrl.click_by_point(CULTIVATE_FACTOR_RECEIVE_CONFIRM)
    else:
        time.sleep(2)
        parse_factor(ctx)


# 历代评分更新-下一页
def script_historical_rating_update(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(HISTORICAL_RATING_UPDATE_CONFIRM)


# 剧本评分更新-下一页
def script_scenario_rating_update(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(SCENARIO_RATING_UPDATE_CONFIRM)
