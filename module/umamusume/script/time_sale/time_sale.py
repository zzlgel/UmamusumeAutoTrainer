import time
import cv2
from bot.recog.ocr import ocr_line, find_similar_text
from bot.recog.image_matcher import image_match
from module.umamusume.context import UmamusumeContext
from module.umamusume.asset.point import *


def script_time_sale_open(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TO_TIME_SALE)
    ctx.time_sale_detail.refresh()


def script_time_sale_main(ctx: UmamusumeContext):
    detail = ctx.time_sale_detail
    if not (buy := detail.buy):
        ctx.ctrl.click_by_point(TIME_SALE_CLOSE)
        return
    # 有时候点快了看不到确认就点掉了
    img = cv2.cvtColor(ctx.current_screen, cv2.COLOR_BGR2GRAY)
    if image_match(img, REF_TIME_SALE_BOUGHT).find_match:
        if detail.buying is not None:
            detail.bought.append(detail.buying)
            detail.buy.remove(detail.buying)
            detail.buying = None
            return
    item = {"泥地跑鞋": 9, "长距离跑鞋": 8, "中距离跑鞋": 7, "英里跑鞋": 6, "短距离跑鞋": 5}
    point = {0: TIME_SALE_ITEM_1,
             1: TIME_SALE_ITEM_2,
             2: TIME_SALE_ITEM_3,
             3: TIME_SALE_ITEM_4}
    for i in range(4):
        if i in buy:
            ctx.ctrl.click_by_point(point[i])
            detail.buying = i
            return
    ctx.ctrl.swipe(x1=360, y1=950, x2=360, y2=200, duration=600, name="翻页")
    time.sleep(0.5)
    if 4 in buy:
        ctx.ctrl.click_by_point(TIME_SALE_ITEM_6)
        detail.buying = 4
        return
    img = cv2.cvtColor(ctx.ctrl.get_screen(), cv2.COLOR_RGB2GRAY)
    result = find_similar_text(ocr_line(img[760:793, 146:257]), item, 0.9)
    if result:
        for i in buy.copy():
            if i == item[result]:
                ctx.ctrl.click_by_point(TIME_SALE_ITEM_5)
                detail.buying = item[result]
            else:
                buy.remove(i)


def script_shop_main(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TIME_SALE_RETURN)


def script_time_sale_buy_confirm(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TIME_SALE_BUY_CONFIRM)
    time.sleep(1)


def script_time_sale_buy_success(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TIME_SALE_BUY_SUCCESS)
    if (detail := ctx.time_sale_detail).buying is not None:
        detail.bought.append(detail.buying)
        detail.buy.remove(detail.buying)
        detail.buying = None


def script_time_sale_close_confirm(ctx: UmamusumeContext):
    ctx.ctrl.click_by_point(TIME_SALE_CLOSE_CONFIRM)
    if bought := ctx.time_sale_detail.bought:
        ctx.task.detail.time_sale_bought.append(bought.copy())
        ctx.time_sale_detail.refresh()
