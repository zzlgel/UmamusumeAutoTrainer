import re
from difflib import SequenceMatcher

import cv2
import numpy

from bot.recog.image_matcher import image_match, compare_color_equal
from bot.recog.ocr import ocr_line, find_similar_text
from module.umamusume.asset.race_data import RACE_LIST
from module.umamusume.context import UmamusumeContext, SupportCardInfo
from module.umamusume.asset import *
from module.umamusume.define import *
from module.umamusume.script.cultivate_task.const import DATE_YEAR, DATE_MONTH
import bot.base.log as logger

log = logger.get_logger(__name__)


def parse_date(img, ctx: UmamusumeContext) -> int:
    # TODO 固定位置待剥离
    sub_img_date = img[35:75, 10:220]
    # 在sub_img_date图像的上下左右各添加宽度为20的白色边框。
    sub_img_date = cv2.copyMakeBorder(sub_img_date, 20, 20, 20, 20, cv2.BORDER_CONSTANT, None, (255, 255, 255))
    date_text = ocr_line(sub_img_date)

    # 因为图片识别，年月拼接在一起，所以才去包含比对方式。
    year_text = ""
    for text in DATE_YEAR:
        if date_text.__contains__(text):
            year_text = text
            break
    # 如果识别不到年份，尝试使用相似度匹配
    if year_text == "":
        year_text = find_similar_text(date_text, DATE_YEAR)

    # 如果是URA总决赛阶段，需要特殊处理。 97: URA总决赛预赛, 98: URA总决赛半决赛, 99: URA总决赛决赛
    if year_text == DATE_YEAR[3]:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if image_match(img, URA_DATE_1).find_match:
            return 97
        elif image_match(img, URA_DATE_2).find_match:
            return 98
        else:
            return 99
    # 如果依然无法匹配，则直接返回-1
    if year_text == "":
        return -1

    # 月份识别，遇到比如ocr识别出来的是“1月上半月”，也有可能是“11月上半月”，TODO 可能需要使用回合数，加以佐证。
    month_text = ""
    for text in DATE_MONTH:
        if date_text.__contains__(text):
            month_text = text
            break
    if month_text == "":
        month_text = find_similar_text(date_text, DATE_MONTH)
    # “出道前”会持续很多回合，故需要继续做比对。TODO 可以采用左上角出道前剩余回合数，计算得来
    if month_text != DATE_MONTH[0]:
        date_id = DATE_YEAR.index(year_text) * 24 + DATE_MONTH.index(month_text)
    else:
        sub_img_turn_to_race = cv2.copyMakeBorder(img[99:158, 13:140], 20, 20, 20, 20, cv2.BORDER_CONSTANT, None,
                                                  (255, 255, 255))
        turn_to_race_text = ocr_line(sub_img_turn_to_race)
        if turn_to_race_text == "比赛日":
            log.debug("出道比赛日")
            return 12
        turn_to_race_text = re.sub("\\D", "", turn_to_race_text)
        if turn_to_race_text == '':
            log.warning("出道战前日期识别异常")
            return 12 - (len(ctx.cultivate_detail.turn_info_history) + 1)
        date_id = 12 - int(turn_to_race_text)
        if date_id < 1:
            log.warning("出道战前日期识别异常")
            return 12 - (len(ctx.cultivate_detail.turn_info_history) + 1)
    return date_id


# 培育主菜单判断逻辑
def parse_cultivate_main_menu(ctx: UmamusumeContext, img):
    # 判断培育主菜单操作是否可用
    parse_train_main_menu_operations_availability(ctx, img)
    # 大致判断剩余体力
    parse_umamusume_remain_stamina_value(ctx, img)
    # 解析基础属性值
    parse_umamusume_basic_ability_value(ctx, img)
    # 解析干劲
    parse_motivation(ctx, img)
    # 解析是否打赢出道战
    parse_debut_race(ctx, img)
    ctx.cultivate_detail.turn_info.parse_main_menu_finish = True


# 是否打赢出道战
def parse_debut_race(ctx: UmamusumeContext, img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if image_match(img, REF_DEBUT_RACE_NOT_WIN).find_match:
        ctx.cultivate_detail.debut_race_win = False
    else:
        ctx.cultivate_detail.debut_race_win = True


# 使用ocr模版识别干劲
def parse_motivation(ctx: UmamusumeContext, img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    for i in range(len(MOTIVATION_LIST)):
        result = image_match(img, MOTIVATION_LIST[i])
        if result.find_match:
            ctx.cultivate_detail.turn_info.motivation_level = MotivationLevel(i + 1)
            return


# ocr识别基础属性值
def parse_umamusume_basic_ability_value(ctx: UmamusumeContext, img):
    sub_img_speed = img[855:885, 70:139]
    sub_img_speed = cv2.copyMakeBorder(sub_img_speed, 20, 20, 20, 20,
                                       cv2.BORDER_CONSTANT, None, (255, 255, 255))
    speed_text = ocr_line(sub_img_speed)

    sub_img_stamina = img[855:885, 183:251]
    sub_img_stamina = cv2.copyMakeBorder(sub_img_stamina, 20, 20, 20, 20,
                                         cv2.BORDER_CONSTANT, None, (255, 255, 255))
    stamina_text = ocr_line(sub_img_stamina)

    sub_img_power = img[855:885, 289:364]
    sub_img_power = cv2.copyMakeBorder(sub_img_power, 20, 20, 20, 20,
                                       cv2.BORDER_CONSTANT, None, (255, 255, 255))
    power_text = ocr_line(sub_img_power)

    sub_img_will = img[855:885, 409:476]
    sub_img_will = cv2.copyMakeBorder(sub_img_will, 20, 20, 20, 20,
                                      cv2.BORDER_CONSTANT, None, (255, 255, 255))
    will_text = ocr_line(sub_img_will)

    sub_img_intelligence = img[855:885, 521:588]
    sub_img_intelligence = cv2.copyMakeBorder(sub_img_intelligence, 20, 20, 20,
                                              20, cv2.BORDER_CONSTANT, None, (255, 255, 255))
    intelligence_text = ocr_line(sub_img_intelligence)

    sub_img_skill = img[855:902, 602:690]
    sub_img_skill = cv2.copyMakeBorder(sub_img_skill, 20, 20, 20, 20,
                                       cv2.BORDER_CONSTANT, None, (255, 255, 255))
    skill_point_text = ocr_line(sub_img_skill)

    # 填充到上下文
    ctx.cultivate_detail.turn_info.uma_attribute.speed = trans_attribute_value(speed_text, ctx,
                                                                               TrainingType.TRAINING_TYPE_SPEED)
    ctx.cultivate_detail.turn_info.uma_attribute.stamina = trans_attribute_value(stamina_text, ctx,
                                                                                 TrainingType.TRAINING_TYPE_STAMINA)
    ctx.cultivate_detail.turn_info.uma_attribute.power = trans_attribute_value(power_text, ctx,
                                                                               TrainingType.TRAINING_TYPE_POWER)
    ctx.cultivate_detail.turn_info.uma_attribute.will = trans_attribute_value(will_text, ctx,
                                                                              TrainingType.TRAINING_TYPE_WILL)
    ctx.cultivate_detail.turn_info.uma_attribute.intelligence = trans_attribute_value(intelligence_text, ctx,
                                                                                      TrainingType.TRAINING_TYPE_INTELLIGENCE)
    ctx.cultivate_detail.turn_info.uma_attribute.skill_point = trans_attribute_value(skill_point_text, ctx)


# 对ocr容错处理
def trans_attribute_value(text: str,
                          ctx: UmamusumeContext,
                          train_type: TrainingType = TrainingType.TRAINING_TYPE_UNKNOWN) -> int:
    text = re.sub("\\D", "", text)
    if text == "":
        prev_turn_idx = len(ctx.cultivate_detail.turn_info_history)
        if prev_turn_idx != 0:
            history = ctx.cultivate_detail.turn_info_history[prev_turn_idx - 1]
            log.error("图像识别错误，使用上回合数值")
            ctx.ocr_error = True
            if train_type == TrainingType.TRAINING_TYPE_SPEED:
                return history.uma_attribute.speed
            elif train_type == TrainingType.TRAINING_TYPE_STAMINA:
                return history.uma_attribute.stamina
            elif train_type == TrainingType.TRAINING_TYPE_POWER:
                return history.uma_attribute.power
            elif train_type == TrainingType.TRAINING_TYPE_WILL:
                return history.uma_attribute.will
            elif train_type == TrainingType.TRAINING_TYPE_INTELLIGENCE:
                return history.uma_attribute.intelligence
            else:
                log.error("训练类型错误，无法给出准确训练类型数据")
                ctx.ocr_error = True
                return 0
        else:
            # 如果是第一回合，无法使用上回合数值，直接返回100?
            log.error("第一回合或者中间开始，无法获取上回合数据")
            return 100
    else:
        return int(text)


# 体力条，通过截图宽为1，长为229至505范围的体力条，遍历对比“灰色”使用过。
# TODO 很多支援卡时间都能提升体力条上限，无法保证体力条长度一定是276。会存在一些误差，但是对使用不会有太大影响
def parse_umamusume_remain_stamina_value(ctx: UmamusumeContext, img):
    sub_img_remain_stamina = img[160:161, 229:505]
    stamina_counter = 0
    for c in sub_img_remain_stamina[0]:
        if not compare_color_equal(c, [117, 117, 117]):
            stamina_counter += 1
    remain_stamina = int(stamina_counter / 276 * 100)
    ctx.cultivate_detail.turn_info.remain_stamina = remain_stamina


# 判断培育主菜单操作是否可用，由于“训练”、“休息”、“外出”、“技能”（包括合宿）都是全过程可用，所以只需判断“医务室”“赛事”
def parse_train_main_menu_operations_availability(ctx: UmamusumeContext, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # btn_rest_check_point = img[980, 60]
    # btn_train_check_point = img[990, 250]
    # btn_skill_check_point = img[980, 550]
    # btn_trip_check_point = img[1115, 305]
    btn_medic_room_check_point = img[1125, 105]
    btn_race_check_point = img[1130, 490]

    # 夏合宿期间
    if (36 < ctx.cultivate_detail.turn_info.date <= 40
            or 60 < ctx.cultivate_detail.turn_info.date <= 64):
        btn_medic_room_check_point = img[1130, 200]
        # btn_rest_check_point = img[990, 190]
        btn_race_check_point = img[1125, 395]

    # 通过rgb色值判断按钮操作是否可用
    if (btn_medic_room_check_point[0] > 200
            and btn_medic_room_check_point[1] > 200
            and btn_medic_room_check_point[2] > 200):
        medic_room_available = True
    else:
        medic_room_available = False
    race_available = btn_race_check_point[0] > 200

    ctx.cultivate_detail.turn_info.race_available = race_available
    ctx.cultivate_detail.turn_info.medic_room_available = medic_room_available


# 支援卡
def parse_training_support_card(ctx: UmamusumeContext, img, train_type: TrainingType):
    base_x = 590
    base_y = 190
    # 每个支援卡头像的高度
    inc = 120
    # TODO 为什么遍历五次，猜测支援卡同框概率太低，并且凑齐六个之前就很大概率要点这个训练项目了。
    # x 695
    # y 300
    for i in range(5):
        support_card_icon = img[base_y:base_y + 110, base_x: base_x + 105]
        # 判断友情（羁绊）等级，通过最左边一格颜色判断
        support_card_icon = cv2.cvtColor(support_card_icon, cv2.COLOR_BGR2RGB)
        # 获取图像中第96行第17列和第21列的像素值，判断支援卡的友情等级
        favor_process_check_list = [support_card_icon[95, 16], support_card_icon[95, 20]]
        support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN
        for support_card_favor_process_pos in favor_process_check_list:
            if compare_color_equal(support_card_favor_process_pos, [255, 235, 120]):
                support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_4
            elif compare_color_equal(support_card_favor_process_pos, [255, 173, 30]):
                support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_3
            elif compare_color_equal(support_card_favor_process_pos, [162, 230, 30]):
                support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_2
            elif (compare_color_equal(support_card_favor_process_pos, [42, 192, 255]) or
                  compare_color_equal(support_card_favor_process_pos, [109, 108, 117])):
                support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_1
            if support_card_favor_process != SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                break

        # 判断是否有事件，为了简单处理，直接使用rgb颜色阈值判断
        support_card_event_pos = support_card_icon[5, 83]
        support_card_event_available = False
        if (support_card_event_pos[0] >= 250
                and 55 <= support_card_event_pos[1] <= 90
                and 115 <= support_card_event_pos[2] <= 150):
            support_card_event_available = True

        # 判断支援卡类型
        support_card_type = SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN
        support_card_icon = cv2.cvtColor(support_card_icon, cv2.COLOR_RGB2GRAY)
        if image_match(support_card_icon, REF_SUPPORT_CARD_TYPE_SPEED).find_match:
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_SPEED
        elif image_match(support_card_icon, REF_SUPPORT_CARD_TYPE_STAMINA).find_match:
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_STAMINA
        elif image_match(support_card_icon, REF_SUPPORT_CARD_TYPE_POWER).find_match:
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_POWER
        elif image_match(support_card_icon, REF_SUPPORT_CARD_TYPE_WILL).find_match:
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_WILL
        elif image_match(support_card_icon, REF_SUPPORT_CARD_TYPE_INTELLIGENCE).find_match:
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_INTELLIGENCE
        elif image_match(support_card_icon, REF_SUPPORT_CARD_TYPE_FRIEND).find_match:
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_FRIEND
        if support_card_favor_process is not SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
            # TODO 如果需要更多支援卡信息，就需要“菜单”-“编成信息”找到支援卡列表，然后再找到支援卡的详细信息。在根据支援卡头像匹配
            info = SupportCardInfo(card_type=support_card_type,
                                   favor=support_card_favor_process,
                                   has_event=support_card_event_available)
            ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].support_card_info_list.append(info)
        base_y += inc


# 训练项目，根据模版匹配，也可以根据文字识别
def parse_train_type(ctx: UmamusumeContext, img) -> TrainingType:
    train_label = cv2.cvtColor(img[210:275, 0:210], cv2.COLOR_RGB2GRAY)
    train_type = TrainingType.TRAINING_TYPE_UNKNOWN
    if image_match(train_label, REF_TRAINING_TYPE_SPEED).find_match:
        train_type = TrainingType.TRAINING_TYPE_SPEED
    elif image_match(train_label, REF_TRAINING_TYPE_STAMINA).find_match:
        train_type = TrainingType.TRAINING_TYPE_STAMINA
    elif image_match(train_label, REF_TRAINING_TYPE_POWER).find_match:
        train_type = TrainingType.TRAINING_TYPE_POWER
    elif image_match(train_label, REF_TRAINING_TYPE_WILL).find_match:
        train_type = TrainingType.TRAINING_TYPE_WILL
    elif image_match(train_label, REF_TRAINING_TYPE_INTELLIGENCE).find_match:
        train_type = TrainingType.TRAINING_TYPE_INTELLIGENCE
    return train_type


# 解析训练预计结果
def parse_training_result(ctx: UmamusumeContext, img, train_type: TrainingType):
    sub_img_speed_incr = img[770:826, 30:140]
    speed_incr_text = ocr_line(sub_img_speed_incr)
    speed_incr_text = re.sub("\\D", "", speed_incr_text)

    sub_img_stamina_incr = img[770:826, 140:250]
    stamina_incr_text = ocr_line(sub_img_stamina_incr)
    stamina_incr_text = re.sub("\\D", "", stamina_incr_text)

    sub_img_power_incr = img[770:826, 250:360]
    power_incr_text = ocr_line(sub_img_power_incr)
    power_incr_text = re.sub("\\D", "", power_incr_text)

    sub_img_will_incr = img[770:826, 360:470]
    will_incr_text = ocr_line(sub_img_will_incr)
    will_incr_text = re.sub("\\D", "", will_incr_text)

    sub_img_intelligence_incr = img[770:826, 470:580]
    intelligence_incr_text = ocr_line(sub_img_intelligence_incr)
    intelligence_incr_text = re.sub("\\D", "", intelligence_incr_text)

    sub_img_skill_point_incr = img[770:826, 588:695]
    skill_point_incr_text = ocr_line(sub_img_skill_point_incr)
    skill_point_incr_text = re.sub("\\D", "", skill_point_incr_text)

    # 检查不同训练类型各项属性是否识别正常
    if train_type == TrainingType.TRAINING_TYPE_SPEED:
        if speed_incr_text == "" or power_incr_text == "" or skill_point_incr_text == "":
            ctx.ocr_error = True
            log.error("速度训练属性识别异常，速度：%s，力量：%s，技能点：%s",
                      speed_incr_text, power_incr_text, skill_point_incr_text)
    if train_type == TrainingType.TRAINING_TYPE_STAMINA:
        if stamina_incr_text == "" or will_incr_text == "" or skill_point_incr_text == "":
            ctx.ocr_error = True
            log.error("耐力训练属性识别异常，耐力：%s，毅力：%s，技能点：%s",
                      stamina_incr_text, will_incr_text, skill_point_incr_text)
    if train_type == TrainingType.TRAINING_TYPE_POWER:
        if power_incr_text == "" or stamina_incr_text == "" or skill_point_incr_text == "":
            ctx.ocr_error = True
            log.error("力量训练属性识别异常，力量：%s，耐力：%s，技能点：%s",
                      power_incr_text, stamina_incr_text, skill_point_incr_text)
    if train_type == TrainingType.TRAINING_TYPE_WILL:
        if will_incr_text == "" or speed_incr_text == "" or skill_point_incr_text == "" or power_incr_text == "":
            ctx.ocr_error = True
            log.error("毅力训练属性识别异常，毅力：%s，速度：%s，技能点：%s，力量：%s",
                      will_incr_text, speed_incr_text, skill_point_incr_text, power_incr_text)
    if train_type == TrainingType.TRAINING_TYPE_INTELLIGENCE:
        if intelligence_incr_text == "" or speed_incr_text == "" or skill_point_incr_text == "":
            ctx.ocr_error = True
            log.error("智力训练属性识别异常，智力：%s，速度：%s，技能点：%s",
                      intelligence_incr_text, speed_incr_text, skill_point_incr_text)

    # 记录训练结果
    if speed_incr_text != "":
        ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].speed_incr = int(speed_incr_text)
    if stamina_incr_text != "":
        ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].stamina_incr = int(stamina_incr_text)
    if power_incr_text != "":
        ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].power_incr = int(power_incr_text)
    if will_incr_text != "":
        ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].will_incr = int(will_incr_text)
    if intelligence_incr_text != "":
        ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].intelligence_incr = int(intelligence_incr_text)
    if skill_point_incr_text != "":
        ctx.cultivate_detail.turn_info.training_info_list[train_type.value - 1].skill_point_incr = int(skill_point_incr_text)


# 开始培育时，查找好友支援卡
def find_support_card(ctx: UmamusumeContext, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    while True:
        match_result = image_match(img, REF_FOLLOW_SUPPORT_CARD_DETECT_LABEL)
        if not match_result.find_match:
            break

        # pos[0]是左上角的坐标，pos[1]是右下角的坐标
        pos = match_result.matched_area
        support_card_info = img[pos[0][1] - 125:pos[1][1] + 10, pos[0][0] - 140: pos[1][0] + 380]
        # 将原始图像中匹配区域的部分设置为0，也就是将这部分区域变为黑色。为了在后续的图像处理中忽略这部分已经处理过的区域。
        img[pos[0][1]:pos[1][1], pos[0][0]: pos[1][0]] = 0
        support_card_level_img = support_card_info[125:145, 68:111]
        support_card_name_img = support_card_info[63:94, 132:439]

        support_card_level_img = cv2.copyMakeBorder(support_card_level_img, 20, 20, 20, 20, cv2.BORDER_CONSTANT,
                                                    None,
                                                    (255, 255, 255))
        support_card_name_img = cv2.copyMakeBorder(support_card_name_img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, None,
                                                   (255, 255, 255))
        support_card_level_text = ocr_line(support_card_level_img)
        if support_card_level_text == "":
            continue
        support_card_level = int(re.sub("\\D", "", support_card_level_text))
        if support_card_level < ctx.cultivate_detail.follow_support_card_level:
            continue
        support_card_text = ocr_line(support_card_name_img)
        s = SequenceMatcher(None, support_card_text, ctx.cultivate_detail.follow_support_card_name)
        if s.ratio() > 0.7:
            ctx.ctrl.click(match_result.center_point[0], match_result.center_point[1] - 75,
                           "选择支援卡：" + ctx.cultivate_detail.follow_support_card_name + "<" + str(
                               support_card_level) + ">")
            return True
    return False


# 培育事件，包括支援卡和马娘事件
# 111 237 480 283
def parse_cultivate_event(ctx: UmamusumeContext, img) -> (str, list[int]):
    event_name_img = img[237:283, 111:480]
    event_name = ocr_line(event_name_img)
    event_selector_list = []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    while True:
        match_result = image_match(img, REF_SELECTOR)
        if not match_result.find_match:
            break
        event_selector_list.append(match_result.center_point)
        pos = match_result.matched_area
        img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]] = 0

    # 将 event_selector_list 列表中的元素按照x[1]也就是中心点纵坐标进行排序
    event_selector_list.sort(key=lambda x: x[1])
    return event_name, event_selector_list


# 查找比赛
def find_race(ctx: UmamusumeContext, img, race_id: int = 0) -> bool:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    target_race_template = RACE_LIST[race_id][2]
    while True:
        # 以粉丝数图标为锚点匹配.存在即为进入选择比赛界面
        match_result = image_match(img, REF_RACE_LIST_DETECT_LABEL)
        if not match_result.find_match:
            break

        pos = match_result.matched_area
        pos_center = match_result.center_point
        if 685 < pos_center[1] < 1110:
            race_name_img = img[pos[0][1] - 60:pos[1][1] + 25, pos[0][0] - 250: pos[1][0] + 400]
            if target_race_template is not None:
                if image_match(race_name_img, target_race_template).find_match:
                    ctx.ctrl.click(pos_center[0], pos_center[1], "选择比赛：" + str(RACE_LIST[race_id][1]))
                    return True
        img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]] = 0
    return False


# 查找并准备学习技能列表
def find_skill(ctx: UmamusumeContext, img, skill: list[str], learn_any_skill: bool) -> bool:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    find = False
    while True:
        match_result = image_match(img, REF_SKILL_LIST_DETECT_LABEL)
        if not match_result.find_match:
            break

        pos = match_result.matched_area
        pos_center = match_result.center_point
        if 460 < pos_center[0] < 560 and 450 < pos_center[1] < 1050:
            skill_info_img = img[pos[0][1] - 65:pos[1][1] + 75, pos[0][0] - 470: pos[1][0] + 150]
            if not image_match(skill_info_img, REF_SKILL_LEARNED).find_match:
                skill_name_img = skill_info_img[10: 47, 100: 445]
                text = ocr_line(skill_name_img)
                result = find_similar_text(text, skill, 0.7)
                # print(text + "->" + result)
                if result != "" or learn_any_skill:
                    tmp_img = ctx.ctrl.get_screen()
                    pt_text = re.sub("\\D", "", ocr_line(tmp_img[400: 440, 490: 665]))
                    skill_pt_cost_text = re.sub("\\D", "", ocr_line(skill_info_img[69: 99, 525: 588]))
                    if pt_text != "" and skill_pt_cost_text != "":
                        pt = int(pt_text)
                        skill_pt_cost = int(skill_pt_cost_text)
                        if pt >= skill_pt_cost:
                            ctx.ctrl.click(pos_center[0] + 128, pos_center[1], "加点技能：" + text)
                            if result in skill:
                                skill.remove(result)
                            ctx.cultivate_detail.learn_skill_selected = True
                            find = True

        img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]] = 0

    return find


# 获得技能列表
def get_skill_list(img, skill: list[list[str]], skill_blacklist: list[str]) -> list:
    origin_img = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = []
    while True:
        all_skill_scanned = True
        match_result = image_match(img, REF_SKILL_LIST_DETECT_LABEL)
        if match_result.find_match:
            all_skill_scanned = False
            pos = match_result.matched_area
            pos_center = match_result.center_point
            if 460 < pos_center[0] < 560 and 450 < pos_center[1] < 1050:
                skill_info_img = img[pos[0][1] - 65:pos[1][1] + 75, pos[0][0] - 470: pos[1][0] + 150]
                skill_info_cp = origin_img[pos[0][1] - 65:pos[1][1] + 75, pos[0][0] - 470: pos[1][0] + 150]

                skill_name_img = skill_info_img[10: 47, 100: 445]
                skill_cost_img = skill_info_img[69: 99, 525: 588]
                text = ocr_line(skill_name_img)
                cost = re.sub("\\D", "", ocr_line(skill_cost_img))

                # 这段代码是在使用OpenCV库的inRange函数来进行颜色过滤，并判断是否为金色技能。
                # cv2.inRange(src, lowerb, upperb)函数的参数解释如下：
                # src：源图像，这里是skill_info_cp。
                # lowerb：表示BGR颜色空间颜色范围的下界，这里是numpy.array([40, 180, 240])。
                # upperb：表示BGR颜色空间颜色范围的上界，这里是numpy.array([100, 210, 255])。
                # cv2.inRange函数会返回一个与源图像同样大小的二值图像（binary image），
                # 在这个图像中，源图像中在颜色范围内的像素会被设置为255（白色），不在颜色范围内的像素会被设置为0（黑色）。
                # 所以，这行代码的意思是生成一个新的二值图像mask，在这个图像中，skill_info_cp图像中颜色在蓝色40-100，绿色180-210，
                # 红色240-255范围内的像素被设置为白色，其他像素被设置为黑色。
                # 接下来，is_gold = True if mask[120, 600] == 255 else False
                # 这行代码是在判断mask图像中第121行第601列的像素是否为255（白色）。
                # 如果是，那么is_gold被设置为True，表示这是一个金色技能；如果不是，那么is_gold被设置为False，表示这不是一个金色技能。
                mask = cv2.inRange(skill_info_cp, numpy.array([40, 180, 240]), numpy.array([100, 210, 255]))
                is_gold = True if mask[120, 600] == 255 else False

                skill_in_priority_list = False
                # 保存原始技能名字, 以防ocr产生偏差
                skill_name_raw = ""
                priority = 99
                for i in range(len(skill)):
                    found_similar_blacklist = find_similar_text(text, skill_blacklist, 0.7)
                    found_similar_prioritylist = find_similar_text(text, skill[i], 0.7)
                    if found_similar_blacklist != "":  # 排除出现在黑名单中的技能
                        priority = -1
                        skill_name_raw = found_similar_blacklist
                        skill_in_priority_list = True
                        break
                    elif found_similar_prioritylist != "":
                        priority = i
                        skill_name_raw = found_similar_prioritylist
                        skill_in_priority_list = True
                        break
                if not skill_in_priority_list:
                    priority = len(skill)

                available = not image_match(skill_info_img, REF_SKILL_LEARNED).find_match

                if priority != -1:  # 排除出现在黑名单中的技能
                    res.append({"skill_name": text,
                                "skill_name_raw": skill_name_raw,
                                "skill_cost": int(cost),
                                "priority": priority,
                                "gold": is_gold,
                                "subsequent_skill": "",
                                "available": available,
                                "y_pos": int(pos_center[1])})
            img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]] = 0

        # 解析曾经获得过的技能
        match_result = image_match(img, REF_SKILL_LEARNED)
        if match_result.find_match:
            all_skill_scanned = False
            pos = match_result.matched_area
            pos_center = match_result.center_point
            if 550 < pos_center[0] < 640 and 450 < pos_center[1] < 1050:
                skill_info_img = img[pos[0][1] - 65:pos[1][1] + 75, pos[0][0] - 520: pos[1][0] + 150]
                skill_info_cp = origin_img[pos[0][1] - 65:pos[1][1] + 75, pos[0][0] - 470: pos[1][0] + 150]

                # 检查是不是金色技能
                mask = cv2.inRange(skill_info_cp, numpy.array([40, 180, 240]), numpy.array([100, 210, 255]))
                is_gold = True if mask[120, 600] == 255 else False
                skill_name_img = skill_info_img[10: 47, 100: 445]
                text = ocr_line(skill_name_img)
                res.append({"skill_name": text,
                            "skill_name_raw": text,
                            "skill_cost": 0,
                            "priority": -1,
                            "gold": is_gold,
                            "subsequent_skill": "",
                            "available": False,
                            "y_pos": int(pos_center[1])})
            img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]] = 0
        if all_skill_scanned:
            break

    res = sorted(res, key=lambda x: x["y_pos"])
    # 没有精确计算过，但是大约y轴小于540就会导致技能名显示不全。暂时没测试出问题。
    # for r in res if r["y_pos"] >= 540 过滤掉res列表中"y_pos"值小于540的元素。
    # 由于y轴坐标是从上到下递增的，所以过滤掉y轴坐标小于540的元素，就是过滤掉屏幕上半部分的元素。
    # {k: v for k, v in r.items() if k != "y_pos"}：r是一个字典，r.items()会返回一个包含r的所有键值对的列表。
    # 生成一个新的字典，这个字典包含r的所有键值对，除了键为"y_pos"的键值对。
    return [{k: v for k, v in r.items() if k != "y_pos"} for r in res if r["y_pos"] >= 540]


# 因子
def parse_factor(ctx: UmamusumeContext):
    origin_img = ctx.ctrl.get_screen()
    img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)
    factor_list = []
    while True:
        match_result = image_match(img, REF_FACTOR_DETECT_LABEL)
        if match_result.find_match:
            factor_info = ['unknown', 0]
            pos = match_result.matched_area
            factor_info_img_gray = img[pos[0][1] - 20:pos[1][1] + 25, pos[0][0] - 630: pos[1][0] - 25]
            factor_name_sub_img = factor_info_img_gray[15: 60, 45:320]
            factor_name = ocr_line(factor_name_sub_img)

            factor_level = 0
            factor_info_img = origin_img[pos[0][1] - 20:pos[1][1] + 25, pos[0][0] - 630: pos[1][0] - 25]
            factor_level_check_point = [factor_info_img[35, 535], factor_info_img[35, 565], factor_info_img[35, 595]]
            for i in range(len(factor_level_check_point)):
                if not compare_color_equal(factor_level_check_point[i], [223, 227, 237]):
                    factor_level += 1
                else:
                    break
            img[pos[0][1]:pos[1][1], pos[0][0]:pos[1][0]] = 0
            factor_info[0] = factor_name
            factor_info[1] = factor_level
            factor_list.append(factor_info)
        else:
            break
    ctx.cultivate_detail.parse_factor_done = True
    ctx.task.detail.cultivate_result['factor_list'] = factor_list
