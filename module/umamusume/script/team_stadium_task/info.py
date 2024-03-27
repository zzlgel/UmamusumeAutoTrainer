from .race import (script_team_stadium_no_rp,
                   script_team_stadium_select_item,
                   )
from ..common.info import common_script_info
from ..time_sale.info import TITLE as TS_TITLE

TITLE = {
    "选择道具": script_team_stadium_select_item,
    "确认": script_team_stadium_no_rp,
}


def ts_script_info(ctx):
    return common_script_info(ctx, __name__, TITLE, TS_TITLE)
