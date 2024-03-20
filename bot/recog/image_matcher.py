import cv2
import numpy as np

from bot.base.common import ImageMatchMode
from bot.base.resource import Template
import bot.base.log as logger

log = logger.get_logger(__name__)


class ImageMatchResult:
    # matched_area 匹配结果区域 [100, 100]
    matched_area = None
    # center_point 匹配结果的中心点
    center_point = None
    # find_match 匹配是否成功
    find_match: bool = False
    # score 匹配的相似得分（仅用于特征匹配）
    score: int = 0


def image_match(target, template: Template) -> ImageMatchResult:

    try:
        if template.image_match_config.match_mode == ImageMatchMode.IMAGE_MATCH_MODE_TEMPLATE_MATCH:
            return template_match(target, template.template_image, template.image_match_config.match_accuracy)
        else:
            log.error("unsupported match mode")
            return ImageMatchResult()
    except Exception as e:
        log.error(f"image_match failed: {e}")
        return ImageMatchResult()


# 模板匹配
def template_match(target, template, accuracy: float = 0.95) -> ImageMatchResult:
    # template是一个图像，shape是一个属性，它返回一个元组，这个元组包含了图像的高度和宽度。
    # ::是Python的切片操作符，它在这里的作用是获取元组的所有元素。
    th, tw = template.shape[::]
    # 使用matchTemplate函数进行模板匹配，返回的是一个灰度图像，每个像素值表示了此区域与模板的匹配程度。
    # cv2.TM_CCOEFF_NORMED方法计算目标图像和模板之间的归一化相关系数。相关系数是衡量模板与目标图像匹配程度的一种度量。
    # 值为1表示完全匹配，值为-1表示完全反向匹配。归一化确保结果是-1到1之间的值，无论图像的规模如何。
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    # 使用minMaxLoc函数找到result中的最小值和最大值的位置。
    # 函数会在result中找到最小和最大像素值及其位置，在模板匹配的上下文中，最大值（max_val）代表图像中最高的匹配质量
    # 最小值（min_val）通常不会用到。max_loc和min_loc分别是最大值和最小值的位置。
    # 在模板匹配的上下文中，最大值的位置（max_loc）是目标图像中与模板最匹配的区域的左上角。
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    match_result = ImageMatchResult()
    if max_val > accuracy:
        match_result.find_match = True
        match_result.center_point = (int(max_loc[0] + tw / 2), int(max_loc[1] + th / 2))
        match_result.matched_area = ((max_loc[0], max_loc[1]), (max_loc[0] + tw, max_loc[1] + th))
    else:
        match_result.find_match = False
    return match_result


def compare_color_equal(p: list, target: list, tolerance: int = 10) -> bool:
    # 比较两个颜色是否相等
    # 是计算两个点之间的欧氏距离，如果距离小于容差值，则认为两个点相等。
    # 欧氏距离的公式是：d = sqrt((x2-x1)^2 + (y2-y1)^2)
    # 这里的np.array(target)和np.array(p)是将目标点和参考点转换为NumPy数组，这样可以方便地进行向量运算。
    # (np.array(target) - np.array(p)) ** 2是计算两点在每个维度上的差的平方。这是欧氏距离公式的一部分。
    # np.sum((np.array(target) - np.array(p)) ** 2)是计算两点在每个维度上的差的平方的和。这是欧氏距离公式的另一部分。
    # np.sqrt(np.sum((np.array(target) - np.array(p)) ** 2))是计算两点之间的欧氏距离。
    distance = np.sqrt(np.sum((np.array(target) - np.array(p)) ** 2))
    return distance < tolerance
