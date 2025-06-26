from .time_sale import *

TITLE = {
    "限时特卖开售": script_time_sale_open,
    "兑换确认": script_time_sale_buy_confirm,
    "兑换成功": script_time_sale_buy_success,
    "重置确认": script_time_sale_close_confirm,
    "道具详情": lambda ctx: ctx.ctrl.click_by_point(TIME_SALE_COMMON_CONFIRM),
}
