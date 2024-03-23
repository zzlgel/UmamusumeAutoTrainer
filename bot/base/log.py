import logging
import sys
from logging import Logger

import colorlog

# 定义不同级别日志颜色
log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


# 获取日志对象
def get_logger(name) -> Logger:
    logger = logging.getLogger(name)
    # 防止日志打印重复。这个 Logger 对象的日志信息不会传递给它的父级。
    logger.propagate = False
    # 如果 logger 没有处理器，则添加处理器
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fmt = colorlog.ColoredFormatter(
            fmt='%(log_color)s%(asctime)s  %(levelname)-8s [%(funcName)34s] %(filename)-20s: %(message)s',
            log_colors=log_colors_config
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(fmt)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
    return logger
