from enum import Enum

from bot.base.common import Coordinate
from bot.base.resource import Template


# ClickPointType 是一个点击点类型枚举
class ClickPointType(Enum):
    # COORDINATE 表示点击点是一个坐标
    CLICK_POINT_TYPE_COORDINATE = 0
    # TEMPLATE 表示点击点是一个模板
    CLICK_POINT_TYPE_TEMPLATE = 1


# ClickPoint 是一个点击点，用于描述一个点击点的信息
class ClickPoint:
    # target_type 是一个点击点类型
    target_type: ClickPointType = None
    # template 是一个模板
    template: Template | None = None
    # coordinate 是一个坐标
    coordinate: Coordinate = None
    # desc 是一个描述
    desc: str = None
    # template_check_list 是一个模板列表 TODO 这里检查什么呢？
    template_check_list: list[Template] = None

    def __init__(self, target_type: ClickPointType, template: Template = None, coordinate: Coordinate = None,
                 desc: str = "", template_check_list: list[Template] = None):
        self.target_type = target_type
        self.desc = desc
        self.template_check_list = template_check_list
        self.coordinate = coordinate
        self.template = template







