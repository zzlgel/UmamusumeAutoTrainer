from .donate import (script_donate_requests,
                     script_donate_confirm,
                     script_donate_success,
                     )
from ..common.info import common_script_info

TITLE = {
    "道具捐赠请求": script_donate_requests,
    "捐赠确认": script_donate_confirm,
    "捐赠成功": script_donate_success,
}


def d_script_info(ctx):
    return common_script_info(ctx, __name__, TITLE)
