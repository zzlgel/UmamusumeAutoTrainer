import cv2

from bot.base.common import ImageMatchConfig


# 用于图像匹配的模板
class Template:
    # 模板名称
    template_name: str
    # 模板图像。使用cv2.imread函数从文件中读取的
    template_image: object
    # 模板图像的资源路径
    resource_path: str
    # 模板图像的匹配配置
    image_match_config: ImageMatchConfig

    def __init__(self,
                 template_name: str,
                 resource_path: str,
                 image_match_config: ImageMatchConfig = ImageMatchConfig()):
        self.resource_path = resource_path
        self.template_name = template_name
        # cv2.imread()函数是OpenCV库中的一个方法，OpenCV库在Python中用于图像处理任务。
        # 该函数的作用是读取图像文件，返回一个多维数组。该数组中包含了图像的像素值。
        # 该函数的第一个参数是图像文件的路径，第二个参数是读取图像的模式。
        # 读取图像的模式有三种，分别是cv2.IMREAD_COLOR、cv2.IMREAD_GRAYSCALE和cv2.IMREAD_UNCHANGED。
        # cv2.IMREAD_COLOR：读入一副彩色图像。图像的透明度会被忽略，这是默认参数。可用1表示。
        # cv2.IMREAD_GRAYSCALE：以灰度模式读入图像。可用0表示。
        # cv2.IMREAD_UNCHANGED：读入一幅图像，并且包括图像的 alpha 通道。可用-1表示。
        # 该函数返回的是一个多维数组，该数组中包含了图像的像素值。 如果图像读取失败，该函数返回None。
        self.template_image = cv2.imread("resource" + self.resource_path + "/" + template_name.lower() + ".png", 0)
        self.image_match_config = image_match_config


class UI:
    # UI名称
    ui_name = None
    # 需要检查存在的模板列表
    check_exist_template_list: list[Template] = None
    # 需要检查不存在的模板列表
    check_non_exist_template_list: list[Template] = None

    def __init__(self, ui_name, check_exist_template_list: list[Template],
                 check_non_exist_template_list: list[Template]):
        self.ui_name = ui_name
        self.check_exist_template_list = check_exist_template_list
        self.check_non_exist_template_list = check_non_exist_template_list


# 表示不存在的UI。用来替代游戏加载过程中无法识别的场景
NOT_FOUND_UI = UI("NOT_FOUND_UI", [], [])
