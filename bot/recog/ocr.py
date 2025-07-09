# 飞桨相关ocr改动文档：https://paddlepaddle.github.io/PaddleOCR/main/version3.x/pipeline_usage/OCR.html#22-python
import cv2
import paddleocr
from difflib import SequenceMatcher
import bot.base.log as logger

log = logger.get_logger(__name__)

OCR_CH = paddleocr.PaddleOCR(lang="ch", 
                             use_doc_orientation_classify=False, 
                             use_doc_unwarping=False, 
                             use_textline_orientation=False,
                             device="gpu:0")


# ocr 文字识别图片
def ocr(img, lang="ch"):
    if lang == "ch":
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # 转换为三通道彩色图像
        return OCR_CH.predict(img)


# ocr_line 文字识别图片，返回所有出现的文字
# # 飞桨相关ocr改动文档：https://paddlepaddle.github.io/PaddleOCR/main/version3.x/pipeline_usage/OCR.html#22-python
def ocr_line(img, lang="ch"):
    ocr_result = ocr(img, lang)
    text = ""
    
    for text_info in ocr_result:
        if len(text_info["rec_texts"]) > 0:
            text += ', '.join(text_info["rec_texts"])
    return text

# TODO 暂且这么改，其实本质没有太大变化。
def ocr_digits(img, lang="ch"):
    ocr_result = ocr(img, lang)
    text = ""
    
    for text_info in ocr_result:
        if len(text_info["rec_texts"]) > 0:
            text += ', '.join(text_info["rec_texts"])
    return text


# find_text_pos 查找目标文字在图片中的位置
def find_text_pos(ocr_result, target):
    threshold = 0.6
    result = None
    for text_info in ocr_result:
        if len(text_info["rec_texts"]) > 0:
            for index, text in enumerate(text_info["rec_texts"]):
                s = SequenceMatcher(None, target, text)
                if s.ratio() > threshold:
                    result = text_info["rec_polys"][index]
                    threshold = s.ratio()
    return result


# TODO 为何不返回列表索引和匹配文本呢
def find_similar_text(target_text, ref_text_list, threshold=0):
    result = ""
    for ref_text in ref_text_list:
        s = SequenceMatcher(None, target_text, ref_text)
        if s.ratio() > threshold:
            result = ref_text
            threshold = s.ratio()
    return result

